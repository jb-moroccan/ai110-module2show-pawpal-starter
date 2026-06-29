
from pawpal_system import Owner, Pet, Task, Scheduler


def get_pet_for_task(owner: Owner, task: Task) -> Pet | None:
    return owner.get_pet_for_task(task)


def get_conflict_free_schedule(owner: Owner, tasks: list[Task]) -> list[Task]:
    filtered_tasks: list[Task] = []

    for task in tasks:
        pet = get_pet_for_task(owner, task)
        if pet is None:
            filtered_tasks.append(task)
            continue

        has_conflict = any(
            existing is not task
            and existing.due_datetime() == task.due_datetime()
            and existing.name == task.name
            and get_pet_for_task(owner, existing) is not None
            and get_pet_for_task(owner, existing).type != pet.type
            for existing in filtered_tasks
        )
        if not has_conflict:
            filtered_tasks.append(task)

    return filtered_tasks


def main():
    owner = Owner(name="Alex", availability={"Monday": 8, "Tuesday": 6})
    owner.set_availability("Wednesday", 7)

    # Create original pets
    pet1 = Pet(name="Buddy", type="Dog")
    pet2 = Pet(name="Mittens", type="Cat")

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # Create original tasks (without pet names in task titles)
    feed_buddy = Task(
        name="Feed",
        status="pending",
        priority=1,
        recurrence="daily",
        due_date="08:00",
        duration_minutes=15,
    )
    walk_buddy = Task(
        name="Walk",
        status="pending",
        priority=2,
        recurrence="daily",
        due_date="12:30",
        duration_minutes=30,
    )
    feed_mittens = Task(
        name="Feed",
        status="pending",
        priority=1,
        recurrence="weekly",
        due_date="09:00",
        duration_minutes=10,
    )

    # Create conflict demo tasks upfront
    fetch_buddy = Task(
        name="Fetch",
        status="pending",
        priority=2,
        recurrence="daily",
        due_date="10:00",
        duration_minutes=20,
    )
    fetch_max = Task(
        name="Fetch",
        status="pending",
        priority=2,
        recurrence="daily",
        due_date="10:00",
        duration_minutes=20,
    )
    groom_buddy = Task(
        name="Groom",
        status="pending",
        priority=1,
        recurrence="weekly",
        due_date="11:00",
        duration_minutes=30,
    )
    groom_mittens = Task(
        name="Groom",
        status="pending",
        priority=1,
        recurrence="weekly",
        due_date="11:00",
        duration_minutes=30,
    )

    # Create additional pet upfront
    max_dog = Pet(name="Max", type="Dog")
    owner.add_pet(max_dog)

    # Add tasks to pets
    pet1.add_task(walk_buddy)
    pet2.add_task(feed_mittens)
    pet1.add_task(feed_buddy)
    pet1.add_task(fetch_buddy)
    max_dog.add_task(fetch_max)
    pet1.add_task(groom_buddy)
    pet2.add_task(groom_mittens)

    # Mark task1 as complete for demonstration
    feed_buddy.mark_complete()
    walk_buddy.update_priority(3)
    feed_mittens.set_recurrence("weekly")

    # Build main scheduler with original tasks + conflict demo tasks
    scheduler = Scheduler()
    scheduler.add_task(walk_buddy)
    scheduler.add_task(feed_buddy)
    scheduler.add_task(feed_mittens)
    scheduler.add_task(fetch_buddy)
    scheduler.add_task(fetch_max)
    scheduler.add_task(groom_buddy)
    scheduler.add_task(groom_mittens)
    scheduler.sort_tasks()

    print(f"All tasks after out-of-order add — Owner: {owner.name}")
    print("------------------")
    for task in scheduler.daily_task_list:
        pet = get_pet_for_task(owner, task)
        pet_name = pet.name if pet else "Unknown"
        print(f"{task.due_date or ''} — {task.name} ({pet_name}) ({task.duration_minutes} min) [priority: {task.priority}] [{task.status}]")

    print("\nPending tasks:")
    for task in scheduler.filter_tasks(status="pending"):
        pet = get_pet_for_task(owner, task)
        pet_name = pet.name if pet else "Unknown"
        print(f"{task.due_date or ''} — {task.name} ({pet_name}) ({task.duration_minutes} min) [priority: {task.priority}] [{task.status}]")

    print("\nCompleted tasks:")
    for task in scheduler.filter_tasks(status="complete"):
        pet = get_pet_for_task(owner, task)
        pet_name = pet.name if pet else "Unknown"
        print(f"{task.due_date or ''} — {task.name} ({pet_name}) ({task.duration_minutes} min) [priority: {task.priority}] [{task.status}]")

    print("\nBuddy's tasks:")
    for task in scheduler.filter_tasks(pet_name="Buddy", owner=owner):
        pet = get_pet_for_task(owner, task)
        pet_name = pet.name if pet else "Unknown"
        print(f"{task.due_date or ''} — {task.name} ({pet_name}) ({task.duration_minutes} min) [priority: {task.priority}] [{task.status}]")

    # Build the daily schedule with scheduled times
    scheduler.build_schedule(owner)

    print("\nFinal daily schedule from owner (with scheduled times):")
    print(f"Owner must start at: {scheduler.get_earliest_start_time_str()}")
    print("-" * 80)
    for task in scheduler.daily_task_list:
        if task.status == "complete":
            continue
        pet = get_pet_for_task(owner, task)
        pet_name = pet.name if pet else "Unknown"

        # Show scheduled times if available
        if hasattr(task, "scheduled_start") and hasattr(task, "scheduled_end"):
            start_time = task.scheduled_start.strftime("%H:%M")
            end_time = task.scheduled_end.strftime("%H:%M")
            scheduled_info = f"[{start_time}-{end_time}]"
        else:
            scheduled_info = "[not scheduled]"

        print(f"{scheduled_info} {task.name:20s} ({pet_name:10s}) due {task.due_date or 'N/A':5s} ({task.duration_minutes} min) [priority: {task.priority}]")

    print("\n" + "=" * 60)
    print("CONFLICT DETECTION DEMO")
    print("=" * 60)

    # Scenario 1: No conflict - same task at same time, same breed (both Dogs)
    print("\nScenario 1: No Conflict (same breed, same task)")
    print("-" * 60)
    print("Buddy (Dog) and Max (Dog) both performing Fetch at 10:00")

    scheduler_same_breed = Scheduler()
    scheduler_same_breed.add_task(fetch_buddy)
    scheduler_same_breed.add_task(fetch_max)

    conflicts_scenario1 = scheduler_same_breed.detect_conflicts(owner, tasks=[fetch_buddy, fetch_max])
    if conflicts_scenario1:
        print("WARNING: Conflicts detected:")
        for warning in conflicts_scenario1:
            print(f"   {warning}")
    else:
        print("OK: No conflicts detected")

    print("\nTasks in Scenario 1:")
    for task in [fetch_buddy, fetch_max]:
        pet = get_pet_for_task(owner, task)
        pet_name = pet.name if pet else "Unknown"
        print(f"  {task.due_date or ''} — {task.name} ({pet_name}) ({task.duration_minutes} min) [priority: {task.priority}] [{task.status}]")

    # Scenario 2: Conflict - same task at same time, different breeds
    print("\nScenario 2: Conflict (different breeds, same task)")
    print("-" * 60)
    print("Buddy (Dog) and Mittens (Cat) both performing Groom at 11:00")

    scheduler_diff_breed = Scheduler()
    scheduler_diff_breed.add_task(groom_buddy)
    scheduler_diff_breed.add_task(groom_mittens)

    conflicts_scenario2 = scheduler_diff_breed.detect_conflicts(owner, tasks=[groom_buddy, groom_mittens])
    if conflicts_scenario2:
        print("WARNING: CONFLICTS DETECTED:")
        for warning in conflicts_scenario2:
            print(f"   {warning}")
    else:
        print("OK: No conflicts detected")

    print("\nTasks in Scenario 2:")
    for task in [groom_buddy, groom_mittens]:
        pet = get_pet_for_task(owner, task)
        pet_name = pet.name if pet else "Unknown"
        print(f"  {task.due_date or ''} — {task.name} ({pet_name}) ({task.duration_minutes} min) [priority: {task.priority}] [{task.status}]")


if __name__ == "__main__":
    main()
