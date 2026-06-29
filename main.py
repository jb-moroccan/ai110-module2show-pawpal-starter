
from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    owner = Owner(name="Alex", availability={"Monday": 8, "Tuesday": 6})
    owner.set_availability("Wednesday", 7)

    pet1 = Pet(name="Buddy", type="Dog")
    pet2 = Pet(name="Mittens", type="Cat")
    pet1.set_name("Buddy")
    pet1.set_type("Dog")
    pet2.set_name("Mittens")
    pet2.set_type("Cat")

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    task1 = Task(
        name="Feed Buddy",
        status="pending",
        priority=1,
        recurrence="daily",
        due_date="08:00",
        duration_minutes=15,
    )
    task2 = Task(
        name="Walk Buddy",
        status="pending",
        priority=2,
        recurrence="daily",
        due_date="12:30",
        duration_minutes=30,
    )
    task3 = Task(
        name="Feed Mittens",
        status="pending",
        priority=1,
        recurrence="weekly",
        due_date="09:00",
        duration_minutes=10,
    )

    pet1.add_task(task1)
    pet1.add_task(task2)
    pet2.add_task(task3)

    task2.update_priority(3)
    task3.set_recurrence("weekly")
    task1.mark_complete()

    scheduler = Scheduler()
    scheduler.add_task(task1)
    scheduler.add_task(task2)
    scheduler.add_task(task3)
    scheduler.build_schedule(owner)

    print(f"Today's Schedule — Owner: {owner.name}")
    print("------------------")
    for task in sorted(scheduler.daily_task_list, key=lambda task: task.due_date or ""):
        pet_name = next((pet.name for pet in owner.pets if task in pet.tasks), "Unknown")
        print(f"{task.due_date or ''} — {task.name} ({task.duration_minutes} min) [priority: {task.priority}]")


if __name__ == "__main__":
    main()
