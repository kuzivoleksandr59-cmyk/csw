from controllers import TaskController
from database import SessionLocal, init_db
from repository import TaskRepository
from views import TaskView


def main() -> None:
    init_db()

    db_session = SessionLocal()
    repository = TaskRepository(db_session)
    view = TaskView()
    controller = TaskController(repository, view)

    try:
        while True:
            print("1. Створити таску")
            print("2. Змінити статус таски")
            print("3. Видалити таску")
            print("4. Змінити таску")
            print("5. Відобразити список всіх задач")
            print("6. Відфільтрувати список задач по статусу")
            print("7. Відобразити задачу із заданим id")
            print("0. Вихід")

            choice = input("\nОберіть дію (0-7): ").strip()

            if choice == "1":
                desc = input("Введіть опис таски: ")
                sched = input("Запланувати на (РРРР-ММ-ДД ГГ:ХХ): ")
                controller.add_task(desc, sched)

            elif choice == "2":
                task_id = input("Введіть UUID таски: ")
                print("Виберіть новий статус: 1 - ToDo, 2 - InProgress, 3 - Done")
                st_choice = input("Ваш вибір: ")
                controller.change_status(task_id, st_choice)

            elif choice == "3":
                task_id = input("Введіть UUID таски для видалення: ")
                controller.delete_task(task_id)

            elif choice == "4":
                task_id = input("Введіть UUID таски для редагування: ")
                new_desc = input("Новий опис (Enter — залишити без змін): ")
                new_sched = input("Нова дата (РРРР-ММ-ДД ГГ:ХХ) (Enter — залишити без змін): ")
                controller.edit_task(task_id, new_desc, new_sched)

            elif choice == "5":
                controller.show_all_tasks()

            elif choice == "6":
                print("Виберіть статус для фільтрації: 1 - ToDo, 2 - InProgress, 3 - Done")
                st_choice = input("Ваш вибір: ")
                controller.filter_tasks_by_status(st_choice)

            elif choice == "7":
                task_id = input("Введіть UUID таски: ")
                controller.show_task_by_id(task_id)

            elif choice == "0":
                print("Програму завершено.")
                break
            else:
                print("Некоректний вибір. Спробуйте ще раз.")
    finally:
        db_session.close()


if __name__ == "__main__":
    main()