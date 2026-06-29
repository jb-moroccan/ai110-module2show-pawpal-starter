from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Pet:
    name: str
    type: str
    tasks: List["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        """Add a task to this pet's task list."""
        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task: "Task") -> None:
        """Remove a task from this pet's task list."""
        if task in self.tasks:
            self.tasks.remove(task)

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


class Scheduler:
    def __init__(self) -> None:
        self.daily_task_list: List[Task] = []

    def build_schedule(self, owner: Owner) -> List[Task]:
        """Build a daily task list from an owner's pets."""
        self.daily_task_list = []
        for pet in owner.pets:
            self.daily_task_list.extend(pet.tasks)
        self.sort_tasks()
        return self.daily_task_list

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler's daily task list."""
        if task not in self.daily_task_list:
            self.daily_task_list.append(task)

    def sort_tasks(self) -> None:
        """Sort the daily task list by priority."""
        self.daily_task_list.sort(key=lambda task: task.priority)

    def explain_schedule(self) -> str:
        """Return a readable explanation of the scheduled tasks."""
        if not self.daily_task_list:
            return "No tasks scheduled."

        lines = [
            f"{task.name} (priority {task.priority}, duration {task.duration_minutes} min, due {task.due_date})"
            for task in self.daily_task_list
        ]
        return "\n".join(lines)
