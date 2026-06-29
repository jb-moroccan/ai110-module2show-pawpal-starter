from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional


@dataclass
class Pet:
    name: str
    type: str
    tasks: List["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        """Add a task to this pet's task list."""
        if not any(existing is task for existing in self.tasks):
            self.tasks.append(task)

    def remove_task(self, task: "Task") -> None:
        """Remove a task from this pet's task list."""
        self.tasks = [existing for existing in self.tasks if existing is not task]

    def set_name(self, name: str) -> None:
        """Set the pet's name."""
        self.name = name

    def set_type(self, type: str) -> None:
        """Set the pet's type."""
        self.type = type


@dataclass
class Task:
    name: str
    status: str = "pending"
    priority: int = 5
    recurrence: Optional[str] = None
    due_date: Optional[str] = None
    duration_minutes: int = 0

    def mark_complete(self) -> None:
        """Mark the task as complete."""
        self.status = "complete"

    def update_priority(self, priority: int) -> None:
        """Update the task's priority value."""
        self.priority = priority

    def set_recurrence(self, recurrence: str) -> None:
        """Set how often the task repeats."""
        self.recurrence = recurrence

    def due_datetime(self) -> datetime:
        """Return the task's due date/time as a datetime object."""
        if self.due_date is None:
            return datetime.max.replace(tzinfo=None)  # fallback for missing due dates

        try:
            return datetime.fromisoformat(self.due_date)
        except ValueError:
            today = datetime.today()
            hour, minute = map(int, self.due_date.split(":"))
            return datetime(
                year=today.year,
                month=today.month,
                day=today.day,
                hour=hour,
                minute=minute,
            )

    def next_occurrence(self) -> Optional["Task"]:
        """Create the next task occurrence for repeating tasks."""
        if self.recurrence not in {"daily", "weekly"}:
            return None

        current_due = self.due_datetime()
        interval = timedelta(days=1 if self.recurrence == "daily" else 7)
        next_due = current_due + interval

        return Task(
            name=self.name,
            status="pending",
            priority=self.priority,
            recurrence=self.recurrence,
            due_date=next_due.isoformat(timespec="minutes"),
            duration_minutes=self.duration_minutes,
        )


class Owner:
    def __init__(self, name: str, availability: Optional[Dict[str, int]] = None) -> None:
        self.name = name
        self.pets: List[Pet] = []
        self.availability: Dict[str, int] = availability or {}

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner's pet list."""
        if pet in self.pets:
            self.pets.remove(pet)

    def set_name(self, name: str) -> None:
        """Set the owner's name."""
        self.name = name

    def set_availability(self, day: str, hours: int) -> None:
        """Set the owner's available hours for a day."""
        self.availability[day] = hours

    def get_pet_for_task(self, task: "Task") -> Optional["Pet"]:
        """Return the pet that owns the given task using object identity."""
        for pet in self.pets:
            if any(existing is task for existing in pet.tasks):
                return pet
        return None


class Scheduler:
    def __init__(self) -> None:
        self.daily_task_list: List[Task] = []
        self.earliest_start_time: Optional[datetime] = None

    def build_schedule(self, owner: Owner) -> List[Task]:
        """Build a daily task list from an owner's pets using backwards deadline scheduling.

        Algorithm: Schedules tasks by working backwards from their deadlines. Each task
        is placed as late as possible (anchored to its due time) while ensuring no task
        ends after `next_start` (the start time of the previously-scheduled task in
        reverse order).

        Parallelization: Tasks can run simultaneously if and only if:
        - They have the same task name (e.g., both "Fetch")
        - The pets have the same type (e.g., both Dogs)
        - They have the same due datetime
        Otherwise, tasks are scheduled sequentially (one after another).

        Time Complexity: O(n² + n log n) where n is the number of tasks.
        - O(n log n) for sorting tasks by deadline
        - O(n²) for the backwards loop with matching task lookup

        Args:
            owner: The Owner instance containing all pets and their tasks

        Returns:
            A list of pending, non-complete tasks sorted by scheduled start time.
            Each task has `scheduled_start` and `scheduled_end` datetime attributes
            attached and will finish by its due_datetime().

        Side Effects:
            - Sets `self.earliest_start_time` to the start of the first task
            - Attaches `scheduled_start` and `scheduled_end` to each task
            - Updates `self.daily_task_list` with the final schedule
        """
        # Collect pending tasks with due datetimes, durations, and pet info
        items: List[tuple[Pet, Task, datetime, timedelta]] = []
        for pet in owner.pets:
            for task in pet.tasks:
                if task.status == "complete" or task.due_date is None:
                    continue
                items.append((pet, task, task.due_datetime(), timedelta(minutes=task.duration_minutes)))

        # Sort by deadline (earliest first), then by priority (lower number = higher priority)
        items.sort(key=lambda it: (it[2], it[1].priority))

        # Schedule tasks backwards from their deadlines to avoid overlaps.
        # Tasks can run simultaneously if they have the same name, same pet type,
        # and same due time. Otherwise they must be sequential.
        scheduled: List[Task] = []
        next_start: Optional[datetime] = None

        for pet, task, due_dt, duration in reversed(items):
            # Look for a matching task already scheduled that we can run in parallel with
            matching_task = None
            for scheduled_task in scheduled:
                scheduled_pet = owner.get_pet_for_task(scheduled_task)
                if (
                    scheduled_pet
                    and scheduled_task.name == task.name
                    and scheduled_pet.type == pet.type
                    and scheduled_task.due_datetime() == due_dt
                ):
                    matching_task = scheduled_task
                    break

            if matching_task:
                # Run at the same time as the matching task (same pet type, same task, same due time)
                task.scheduled_start = matching_task.scheduled_start
                task.scheduled_end = matching_task.scheduled_end
            else:
                # Schedule sequentially: finish no later than deadline and no later than next_start
                end = due_dt if (next_start is None or due_dt <= next_start) else next_start
                start = end - duration

                task.scheduled_start = start
                task.scheduled_end = end
                next_start = start

            scheduled.insert(0, task)

        self.daily_task_list = scheduled
        # The earliest start time is when the first task should begin
        self.earliest_start_time = next_start if scheduled else None
        self.sort_tasks()
        return self.daily_task_list

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler's daily task list."""
        if not any(existing is task for existing in self.daily_task_list):
            self.daily_task_list.append(task)

    def complete_task(self, task: Task, owner: Optional[Owner] = None) -> Optional[Task]:
        """Mark a task complete and create the next occurrence if it repeats.

        Algorithm: Transitions a task from "pending" to "complete", removes it from
        the scheduler's daily list, and if the task has a recurrence pattern (daily
        or weekly), creates the next occurrence using `task.next_occurrence()` and
        registers it with the owner's pet.

        Recurrence Handling:
        - Tasks with recurrence "daily" are rescheduled for the same time tomorrow
        - Tasks with recurrence "weekly" are rescheduled for the same time next week
        - Non-recurring tasks (or those with invalid recurrence) produce no next task

        Args:
            task: The Task instance to mark complete
            owner: The Owner instance (required if task has recurrence, to add next_task to the pet)

        Returns:
            The next Task instance if recurrence is enabled, None otherwise

        Raises:
            ValueError: Not raised, but owner should be provided if recurrence is expected,
                       else next tasks won't be linked to their pets
        """
        task.mark_complete()
        self.daily_task_list = [existing for existing in self.daily_task_list if existing is not task]

        next_task = task.next_occurrence()
        if next_task is not None:
            if owner is not None:
                for pet in owner.pets:
                    if task in pet.tasks:
                        pet.add_task(next_task)
                        break
            self.add_task(next_task)
        return next_task

    def filter_tasks(
        self,
        status: Optional[str] = None,
        pet_name: Optional[str] = None,
        owner: Optional[Owner] = None,
    ) -> List[Task]:
        """Return tasks filtered by completion status and/or pet name.

        Filtering: Applies filters in order (status first, then pet_name). Both filters
        are optional; if neither is provided, returns all tasks in daily_task_list.

        Time Complexity: O(n) for status filtering + O(n*m) for pet_name filtering,
        where n is the number of tasks and m is the number of pets.

        Args:
            status: Optional filter by task status (e.g., "pending", "complete").
                   Returns only tasks with this exact status.
            pet_name: Optional filter by pet name. Returns only tasks belonging
                     to the pet with this name.
            owner: Required if pet_name is specified; provides access to pet list
                  for name matching.

        Returns:
            A filtered list of tasks. Empty list if no tasks match all filters.

        Raises:
            ValueError: If pet_name is provided but owner is None.
        """
        filtered = self.daily_task_list

        if status is not None:
            filtered = [task for task in filtered if task.status == status]

        if pet_name is not None:
            if owner is None:
                raise ValueError("owner is required when filtering by pet_name")
            filtered = [
                task
                for task in filtered
                if any(
                    pet.name == pet_name and any(existing is task for existing in pet.tasks)
                    for pet in owner.pets
                )
            ]

        return filtered

    def detect_conflicts(self, owner: Owner, tasks: Optional[List[Task]] = None) -> List[str]:
        """Detect actual schedule conflicts where incompatible tasks overlap in time.

        Conflict Detection Logic:
        1. For each pair of non-complete tasks, check if their scheduled time slots overlap
           using: `task1_end <= task2_start or task2_end <= task1_start` (no overlap)
        2. If no overlap → no conflict (even if due times match)
        3. If overlap exists → classify the conflict:
           a. Same pet, different task names → CONFLICT (one pet can't do two tasks at once)
           b. Same task name, same pet type → NO CONFLICT (multiple pets of same breed can
                                              do the same task simultaneously, e.g., two Dogs fetching)
           c. Same task name, different pet types → CONFLICT (owner can't do task for different
                                                    species simultaneously, e.g., Dog groom + Cat groom)
           d. Different task names, different pets → CONFLICT (owner doing two tasks at once)

        Time Complexity: O(n²) where n is the total number of non-complete tasks across all pets.

        Args:
            owner: The Owner instance containing pets and their task associations
            tasks: Optional filter to check conflicts only for these tasks. If None,
                  checks all non-complete tasks from all pets.

        Returns:
            A list of warning strings describing each conflict found. Empty list if no conflicts.
            Strings are human-readable: "Conflict: Groom for Buddy (Dog) and Mittens (Cat) overlap in time."

        Note:
            Uses `getattr(task, "scheduled_start", task.due_datetime())` to gracefully handle
            tasks without scheduled times (falls back to due_datetime). This allows conflict
            detection to work on schedules before and after `build_schedule()`.
        """
        warnings: List[str] = []
        scheduled = [
            (pet, task)
            for pet in owner.pets
            for task in pet.tasks
            if task.status != "complete" and task.due_date is not None
            and (tasks is None or any(existing is task for existing in tasks))
        ]

        for index, (pet1, task1) in enumerate(scheduled):
            for pet2, task2 in scheduled[index + 1 :]:
                # Check if tasks actually overlap in scheduled time
                task1_start = getattr(task1, "scheduled_start", task1.due_datetime())
                task1_end = getattr(task1, "scheduled_end", task1.due_datetime())
                task2_start = getattr(task2, "scheduled_start", task2.due_datetime())
                task2_end = getattr(task2, "scheduled_end", task2.due_datetime())

                # No overlap if one task ends before the other starts
                if task1_end <= task2_start or task2_end <= task1_start:
                    continue

                # Tasks overlap - check if this is actually a conflict
                if pet1 is pet2:
                    if task1.name != task2.name:
                        warnings.append(
                            f"Conflict: {pet1.name} has overlapping tasks {task1.name} and {task2.name}."
                        )
                    continue

                if task1.name == task2.name:
                    if pet1.type != pet2.type:
                        warnings.append(
                            f"Conflict: {task1.name} for {pet1.name} ({pet1.type}) and {pet2.name} ({pet2.type}) overlap in time."
                        )
                else:
                    warnings.append(
                        f"Conflict: {task1.name} for {pet1.name} and {task2.name} for {pet2.name} overlap in time."
                    )

        return warnings

    def sort_tasks(self) -> None:
        """Sort the daily task list by scheduled start time, then by priority.

        Sorting Strategy: Prioritizes `scheduled_start` (set by `build_schedule()`) when
        available, falling back to `due_datetime()` for tasks without scheduled times.
        For tasks at the same start time, sorts by priority (lower number = higher priority).
        This ensures the task list is always in chronological execution order with high-priority
        tasks first within each time slot.

        Time Complexity: O(n log n) due to Python's Timsort implementation.

        Side Effects:
            Modifies `self.daily_task_list` in-place (does not return a value).
        """
        # Sort by scheduled start time, then by priority (lower number = higher priority)
        # Use negative priority to reverse the order so 1 (high) comes before 3 (low)
        def key_fn(task: Task):
            start_time = getattr(task, "scheduled_start", task.due_datetime())
            return (start_time, -task.priority)

        self.daily_task_list.sort(key=key_fn)

    def get_earliest_start_time(self) -> Optional[datetime]:
        """Return the earliest datetime the owner must start to complete all tasks on time.

        The earliest start time is calculated by `build_schedule()` and represents the
        start of the first task in the backwards-scheduled sequence. This is the latest
        time the owner can sleep in while guaranteeing all tasks complete by their deadlines.

        Time Complexity: O(1) — simple attribute access.

        Returns:
            A datetime object representing the required start time, or None if no tasks
            are scheduled. Returns None even if `build_schedule()` was not called.
        """
        return self.earliest_start_time

    def get_earliest_start_time_str(self) -> str:
        """Return the earliest start time as a formatted string (HH:MM format).

        Provides a human-readable representation of the owner's required wake-up time.
        Useful for display purposes and logging.

        Time Complexity: O(1) — simple formatting operation.

        Returns:
            A string in "HH:MM" format (e.g., "08:50"), or the message
            "No tasks to schedule." if earliest_start_time is None.
        """
        if self.earliest_start_time is None:
            return "No tasks to schedule."
        return self.earliest_start_time.strftime("%H:%M")

    def explain_schedule(self) -> str:
        """Return a human-readable explanation of the complete daily schedule.

        Format: Outputs the required start time followed by each task with:
        - Scheduled execution window [HH:MM–HH:MM]
        - Task name, priority, and duration
        - Due time for reference

        Example Output:
            Owner must start at 08:50 to complete all tasks on time.

            Feed (priority 1, duration 15 min) - scheduled 08:50–09:00, due 09:00
            Walk (priority 3, duration 30 min) - scheduled 12:00–12:30, due 12:30

        Time Complexity: O(n) where n is the number of tasks in daily_task_list.

        Returns:
            A multi-line string suitable for console output or logging. Returns
            "No tasks scheduled." if daily_task_list is empty.
        """
        if not self.daily_task_list:
            return "No tasks scheduled."

        lines = []
        if self.earliest_start_time:
            lines.append(f"Owner must start at {self.earliest_start_time.strftime('%H:%M')} to complete all tasks on time.\n")

        for task in self.daily_task_list:
            if hasattr(task, "scheduled_start") and hasattr(task, "scheduled_end"):
                start_str = task.scheduled_start.strftime("%H:%M")
                end_str = task.scheduled_end.strftime("%H:%M")
                lines.append(
                    f"{task.name} (priority {task.priority}, duration {task.duration_minutes} min) - scheduled {start_str}–{end_str}, due {task.due_date}"
                )
            else:
                lines.append(
                    f"{task.name} (priority {task.priority}, duration {task.duration_minutes} min, due {task.due_date})"
                )
        return "\n".join(lines)
