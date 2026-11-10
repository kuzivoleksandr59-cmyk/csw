from datetime import datetime
import uuid
from models7 import TaskModel, TaskStatus
from views import TaskView


class TaskController:
    def __init__(self, model: TaskModel, view: TaskView) -> None:
        self.model = model
        self.view = view

    def add_task(self, description: str, schedule_str: str) -> None:
        try:
            schedule_for = datetime.strptime(schedule_str, "%Y-%m-%d %H:%M")
            task = self.model.create_task(description, schedule_for)
            self.view.display_message(f"Задачу створено успішно. ID: {task.id}")
        except ValueError:
            self.view.display_error("Невірний формат дати. Використовуйте: РРРР-ММ-ДД ГГ:ХХ")

    def change_status(self, task_id_str: str, status_choice: str) -> None:
        try:
            task_id = uuid.UUID(task_id_str)
            status_map = {
                "1": TaskStatus.TODO,
                "2": TaskStatus.IN_PROGRESS,
                "3": TaskStatus.DONE
            }
            new_status = status_map.get(status_choice)
            if not new_status:
                self.view.display_error("Некоректний вибір статусу.")
                return

            task = self.model.update_task_status(task_id, new_status)
            if task:
                self.view.display_message("Статус задачі оновлено.")
            else:
                self.view.display_error("Задачу з таким ID не знайдено.")
        except ValueError:
            self.view.display_error("Некоректний формат UUID.")

    def delete_task(self, task_id_str: str) -> None:
        try:
            task_id = uuid.UUID(task_id_str)
            if self.model.delete_task(task_id):
                self.view.display_message("Задачу успішно видалено.")
            else:
                self.view.display_error("Задачу з таким ID не знайдено.")
        except ValueError:
            self.view.display_error("Некоректний формат UUID.")

    def edit_task(self, task_id_str: str, new_description: str, new_schedule_str: str) -> None:
        try:
            task_id = uuid.UUID(task_id_str)
            schedule_for = None
            if new_schedule_str.strip():
                schedule_for = datetime.strptime(new_schedule_str, "%Y-%m-%d %H:%M")

            desc = new_description.strip() if new_description.strip() else None

            task = self.model.update_task_details(task_id, description=desc, schedule_for=schedule_for)
            if task:
                self.view.display_message("Задачу відредаговано.")
            else:
                self.view.display_error("Задачу з таким ID не знайдено.")
        except ValueError:
            self.view.display_error("Помилка даних або формату дати (використовуйте РРРР-ММ-ДД ГГ:ХХ).")

    def show_all_tasks(self) -> None:
        tasks = self.model.get_all_tasks()
        self.view.display_tasks(tasks)

    def filter_tasks_by_status(self, status_choice: str) -> None:
        status_map = {
            "1": TaskStatus.TODO,
            "2": TaskStatus.IN_PROGRESS,
            "3": TaskStatus.DONE
        }
        status = status_map.get(status_choice)
        if not status:
            self.view.display_error("Некоректний вибір статусу.")
            return
        tasks = self.model.filter_by_status(status)
        self.view.display_tasks(tasks)

    def show_task_by_id(self, task_id_str: str) -> None:
        try:
            task_id = uuid.UUID(task_id_str)
            task = self.model.get_task_by_id(task_id)
            self.view.display_task(task)
        except ValueError:
            self.view.display_error("Некоректний формат UUID.")