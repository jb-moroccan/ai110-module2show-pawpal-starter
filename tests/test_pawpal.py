from pawpal_system import Pet, Task


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
