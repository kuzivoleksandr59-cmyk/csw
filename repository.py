from datetime import datetime
from typing import List, Optional
import uuid

from sqlalchemy.orm import Session
from models8 import Task, TaskStatus


class TaskRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_task(self, description: str, schedule_for: datetime) -> Task:
        task = Task(description=description, schedule_for=schedule_for)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_all_tasks(self) -> List[Task]:
        return self.session.query(Task).all()

    def get_task_by_id(self, task_id: uuid.UUID) -> Optional[Task]:
        return self.session.query(Task).filter(Task.id == task_id).first()

    def filter_by_status(self, status: TaskStatus) -> List[Task]:
        return self.session.query(Task).filter(Task.status == status).all()

    def update_task_status(self, task_id: uuid.UUID, new_status: TaskStatus) -> Optional[Task]:
        task = self.get_task_by_id(task_id)
        if task:
            task.status = new_status
            self.session.commit()
            self.session.refresh(task)
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
            self.session.commit()
            self.session.refresh(task)
        return task

    def delete_task(self, task_id: uuid.UUID) -> bool:
        task = self.get_task_by_id(task_id)
        if task:
            self.session.delete(task)
            self.session.commit()
            return True
        return False