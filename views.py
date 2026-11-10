from typing import List, Optional
from models7 import Task


class TaskView:
    @staticmethod
    def display_tasks(tasks: List[Task]) -> None:
        if not tasks:
            print("\n[!] Список задач порожній.")
            return

        print("\n" + "=" * 115)
        print(f"| {'ID':<36} | {'Опис':<25} | {'Створено':<16} | {'Заплановано на':<16} | {'Статус':<10} |")
        print("=" * 115)
        for t in tasks:
            desc = t.description if len(t.description) <= 25 else t.description[:22] + "..."
            created = t.created_at.strftime("%Y-%m-%d %H:%M")
            scheduled = t.schedule_for.strftime("%Y-%m-%d %H:%M")
            print(f"| {str(t.id):<36} | {desc:<25} | {created:<16} | {scheduled:<16} | {t.status.value:<10} |")
        print("=" * 115)

    @staticmethod
    def display_task(task: Optional[Task]) -> None:
        if not task:
            print("\n[!] Задачу з таким ID не знайдено.")
            return
        TaskView.display_tasks([task])

    @staticmethod
    def display_message(msg: str) -> None:
        print(f"\n[УСПІХ] {msg}")

    @staticmethod
    def display_error(msg: str) -> None:
        print(f"\n[ПОМИЛКА] {msg}")