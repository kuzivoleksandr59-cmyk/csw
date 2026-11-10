from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
import uuid


class TaskStatus(Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


@dataclass
class Task:
    description: str
    schedule_for: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    status: TaskStatus = TaskStatus.TODO


class TaskModel:
    def __init__(self) -> None:
        self._tasks: Dict[uuid.UUID, Task] = {}

    def create_task(self, description: str, schedule_for: datetime) -> Task:
        task = Task(description=description, schedule_for=schedule_for)
        self._tasks[task.id] = task
        return task

    def get_all_tasks(self) -> List[Task]:
        return list(self._tasks.values())

    def get_task_by_id(self, task_id: uuid.UUID) -> Optional[Task]:
        return self._tasks.get(task_id)

    def filter_by_status(self, status: TaskStatus) -> List[Task]:
        return [task for task in self._tasks.values() if task.status == status]

    def update_task_status(self, task_id: uuid.UUID, new_status: TaskStatus) -> Optional[Task]:
        task = self.get_task_by_id(task_id)
        if task:
            task.status = new_status
        return task

    def update_task_details(
        self,
        task_id: uuid.UUID,
        description: Optional[str] = None,
        schedule_for: Optional[datetime] = None
    ) -> Optional[Task]:
        task = self.get_task_by_id(task_id)
        if task:
            if description is not None:
                task.description = description
            if schedule_for is not None:
                task.schedule_for = schedule_for
        return task

    def delete_task(self, task_id: uuid.UUID) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False