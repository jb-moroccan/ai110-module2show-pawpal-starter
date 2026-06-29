from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_task_status():
    task = Task(
        name="Feed",
        status="pending",
        priority=1,
        recurrence="daily",
        due_date="08:00",
        duration_minutes=15,
    )
    assert task.status != "complete"

    task.mark_complete()

    assert task.status == "complete"


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Fido", type="Dog")
    task = Task(
        name="Walk",
        status="pending",
        priority=2,
        recurrence="daily",
        due_date="12:30",
        duration_minutes=30,
    )

    initial_count = len(pet.tasks)

    pet.add_task(task)

    assert len(pet.tasks) == initial_count + 1


def test_daily_task_completion_creates_next_occurrence():
    owner = Owner(name="Alex")
    pet = Pet(name="Buddy", type="Dog")
    owner.add_pet(pet)

    task = Task(
        name="Feed Buddy",
        status="pending",
        priority=1,
        recurrence="daily",
        due_date="08:00",
        duration_minutes=15,
    )
    pet.add_task(task)

    scheduler = Scheduler()
    scheduler.add_task(task)

    next_task = scheduler.complete_task(task, owner=owner)

    assert task.status == "complete"
    assert next_task is not None
    assert next_task.status == "pending"
    assert next_task.recurrence == "daily"

    expected_due = (datetime.today() + timedelta(days=1)).replace(
        hour=8, minute=0, second=0, microsecond=0
    )
    assert datetime.fromisoformat(next_task.due_date) == expected_due

    active_schedule = scheduler.build_schedule(owner)
    assert len(active_schedule) == 1
    assert active_schedule[0].status == "pending"
    assert active_schedule[0].due_date == next_task.due_date


def test_owner_resolves_pet_by_identity_for_duplicate_task_values():
    owner = Owner(name="Alex")
    buddy = Pet(name="Buddy", type="Dog")
    max_pet = Pet(name="Max", type="Dog")
    owner.add_pet(buddy)
    owner.add_pet(max_pet)

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

    buddy.add_task(fetch_buddy)
    max_pet.add_task(fetch_max)

    assert owner.get_pet_for_task(fetch_buddy) is buddy
    assert owner.get_pet_for_task(fetch_max) is max_pet


def test_detect_conflicts_can_scope_to_specific_tasks():
    owner = Owner(name="Alex")
    buddy = Pet(name="Buddy", type="Dog")
    max_pet = Pet(name="Max", type="Dog")
    owner.add_pet(buddy)
    owner.add_pet(max_pet)

    fetch_buddy = Task(name="Fetch", due_date="10:00", duration_minutes=20)
    fetch_max = Task(name="Fetch", due_date="10:00", duration_minutes=20)
    groom_buddy = Task(name="Groom", due_date="11:00", duration_minutes=30)
    groom_max = Task(name="Groom", due_date="11:00", duration_minutes=30)

    buddy.add_task(fetch_buddy)
    max_pet.add_task(fetch_max)
    buddy.add_task(groom_buddy)
    max_pet.add_task(groom_max)

    warnings = Scheduler().detect_conflicts(owner, tasks=[fetch_buddy, fetch_max])

    assert warnings == []


def test_build_schedule_excludes_conflicting_same_time_tasks_for_different_breeds():
    owner = Owner(name="Alex")
    buddy = Pet(name="Buddy", type="Dog")
    mittens = Pet(name="Mittens", type="Cat")
    owner.add_pet(buddy)
    owner.add_pet(mittens)

    groom_buddy = Task(name="Groom", due_date="11:00", duration_minutes=30)
    groom_mittens = Task(name="Groom", due_date="11:00", duration_minutes=30)

    buddy.add_task(groom_buddy)
    mittens.add_task(groom_mittens)

    scheduler = Scheduler()
    scheduler.add_task(groom_buddy)
    scheduler.add_task(groom_mittens)

    schedule = scheduler.build_schedule(owner)

    # Both tasks should be scheduled, but they must not overlap and must finish by their due times.
    assert len(schedule) == 2
    a, b = schedule
    # Ensure scheduled_start/end were attached
    assert hasattr(a, "scheduled_start") and hasattr(a, "scheduled_end")
    assert hasattr(b, "scheduled_start") and hasattr(b, "scheduled_end")

    # Both must finish by or at their due datetime
    assert a.scheduled_end <= a.due_datetime()
    assert b.scheduled_end <= b.due_datetime()

    # They must not overlap
    assert a.scheduled_end <= b.scheduled_start or b.scheduled_end <= a.scheduled_start


def test_detect_conflicts_uses_scheduled_times_not_due_times():
    """Tasks scheduled at different times don't conflict even if same due time."""
    owner = Owner(name="Alex")
    buddy = Pet(name="Buddy", type="Dog")
    mittens = Pet(name="Mittens", type="Cat")
    owner.add_pet(buddy)
    owner.add_pet(mittens)

    # Both tasks due at 11:00 but different durations
    groom_buddy = Task(
        name="Groom",
        status="pending",
        recurrence="weekly",
        due_date="11:00",
        duration_minutes=30,
    )
    groom_mittens = Task(
        name="Groom",
        status="pending",
        recurrence="weekly",
        due_date="11:00",
        duration_minutes=30,
    )

    buddy.add_task(groom_buddy)
    mittens.add_task(groom_mittens)

    scheduler = Scheduler()
    scheduler.add_task(groom_buddy)
    scheduler.add_task(groom_mittens)
    schedule = scheduler.build_schedule(owner)

    # After scheduling, tasks should not overlap
    conflicts = scheduler.detect_conflicts(owner)
    assert len(conflicts) == 0

    # Verify they are scheduled sequentially
    assert groom_buddy.scheduled_end <= groom_mittens.scheduled_start or groom_mittens.scheduled_end <= groom_buddy.scheduled_start


def test_mixed_daily_and_weekly_tasks_scheduled_without_conflict():
    """Daily and weekly tasks can coexist in schedule if no actual time overlap."""
    owner = Owner(name="Alex")
    buddy = Pet(name="Buddy", type="Dog")
    owner.add_pet(buddy)

    feed_daily = Task(
        name="Feed",
        status="pending",
        priority=1,
        recurrence="daily",
        due_date="09:00",
        duration_minutes=15,
    )
    groom_weekly = Task(
        name="Groom",
        status="pending",
        priority=2,
        recurrence="weekly",
        due_date="10:00",
        duration_minutes=30,
    )

    buddy.add_task(feed_daily)
    buddy.add_task(groom_weekly)

    scheduler = Scheduler()
    scheduler.add_task(feed_daily)
    scheduler.add_task(groom_weekly)
    scheduler.build_schedule(owner)

    assert len(scheduler.daily_task_list) == 2
    # Both should be scheduled
    assert feed_daily.status == "pending"
    assert groom_weekly.status == "pending"
    # No conflicts - they execute at different times
    conflicts = scheduler.detect_conflicts(owner)
    assert len(conflicts) == 0


def test_same_task_same_breed_runs_in_parallel():
    """Same task on same breed pets can run at the same time."""
    owner = Owner(name="Alex")
    buddy = Pet(name="Buddy", type="Dog")
    max_dog = Pet(name="Max", type="Dog")
    owner.add_pet(buddy)
    owner.add_pet(max_dog)

    fetch_buddy = Task(
        name="Fetch",
        status="pending",
        priority=2,
        due_date="10:00",
        duration_minutes=20,
    )
    fetch_max = Task(
        name="Fetch",
        status="pending",
        priority=2,
        due_date="10:00",
        duration_minutes=20,
    )

    buddy.add_task(fetch_buddy)
    max_dog.add_task(fetch_max)

    scheduler = Scheduler()
    scheduler.add_task(fetch_buddy)
    scheduler.add_task(fetch_max)
    scheduler.build_schedule(owner)

    # Both tasks should have the same scheduled time
    assert fetch_buddy.scheduled_start == fetch_max.scheduled_start
    assert fetch_buddy.scheduled_end == fetch_max.scheduled_end
    # Both should finish by due time
    assert fetch_buddy.scheduled_end <= fetch_buddy.due_datetime()
    assert fetch_max.scheduled_end <= fetch_max.due_datetime()


def test_same_task_different_breed_runs_sequentially():
    """Same task on different breed pets must run sequentially."""
    owner = Owner(name="Alex")
    buddy = Pet(name="Buddy", type="Dog")
    mittens = Pet(name="Mittens", type="Cat")
    owner.add_pet(buddy)
    owner.add_pet(mittens)

    groom_buddy = Task(
        name="Groom",
        status="pending",
        priority=1,
        due_date="11:00",
        duration_minutes=30,
    )
    groom_mittens = Task(
        name="Groom",
        status="pending",
        priority=1,
        due_date="11:00",
        duration_minutes=30,
    )

    buddy.add_task(groom_buddy)
    mittens.add_task(groom_mittens)

    scheduler = Scheduler()
    scheduler.add_task(groom_buddy)
    scheduler.add_task(groom_mittens)
    scheduler.build_schedule(owner)

    # Tasks should have different scheduled times (sequential)
    assert groom_buddy.scheduled_end <= groom_mittens.scheduled_start or groom_mittens.scheduled_end <= groom_buddy.scheduled_start
    # Both should finish by due time
    assert groom_buddy.scheduled_end <= groom_buddy.due_datetime()
    assert groom_mittens.scheduled_end <= groom_mittens.due_datetime()
