from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Pet:
    name: str
    type: str
    tasks: List["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task: "Task") -> None:
        if task in self.tasks:
            self.tasks.remove(task)

    def set_name(self, name: str) -> None:
        self.name = name

    def set_type(self, type: str) -> None:
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
        self.status = "completed"

    def update_priority(self, priority: int) -> None:
        self.priority = priority

    def set_recurrence(self, recurrence: str) -> None:
        self.recurrence = recurrence


class Owner:
    def __init__(self, name: str, availability: Optional[Dict[str, int]] = None) -> None:
        self.name = name
        self.pets: List[Pet] = []
        self.availability: Dict[str, int] = availability or {}

    def add_pet(self, pet: Pet) -> None:
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        if pet in self.pets:
            self.pets.remove(pet)

    def set_name(self, name: str) -> None:
        self.name = name

    def set_availability(self, day: str, hours: int) -> None:
        self.availability[day] = hours


class Scheduler:
    def __init__(self) -> None:
        self.daily_task_list: List[Task] = []

    def build_schedule(self, owner: Owner) -> List[Task]:
        self.daily_task_list = []
        for pet in owner.pets:
            self.daily_task_list.extend(pet.tasks)
        self.sort_tasks()
        return self.daily_task_list

    def add_task(self, task: Task) -> None:
        if task not in self.daily_task_list:
            self.daily_task_list.append(task)

    def sort_tasks(self) -> None:
        self.daily_task_list.sort(key=lambda task: task.priority)

    def explain_schedule(self) -> str:
        if not self.daily_task_list:
            return "No tasks scheduled."

        lines = [
            f"{task.name} (priority {task.priority}, duration {task.duration_minutes} min, due {task.due_date})"
            for task in self.daily_task_list
        ]
        return "\n".join(lines)
