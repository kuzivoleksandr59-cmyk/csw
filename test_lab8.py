from datetime import datetime
import unittest
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from controllers import TaskController
from database import Base
from models8 import TaskStatus
from repository import TaskRepository
from views import TaskView


class TestTaskIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("postgresql+psycopg2://postgres:password@localhost:5432/postgres")
        Base.metadata.drop_all(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        TestingSessionLocal = sessionmaker(bind=self.engine)
        self.session = TestingSessionLocal()

        self.repository = TaskRepository(self.session)
        self.view = TaskView()
        self.controller = TaskController(self.repository, self.view)

    def tearDown(self) -> None:
        self.session.close()
        Base.metadata.drop_all(bind=self.engine)
        self.engine.dispose()

    def test_create_and_get_task(self) -> None:
        now = datetime.now()
        task = self.repository.create_task("Інтеграційний тест", now)
        self.assertIsNotNone(task.id)
        self.assertEqual(task.status, TaskStatus.TODO)

        fetched = self.repository.get_task_by_id(task.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.description, "Інтеграційний тест")

    def test_get_all_and_filter(self) -> None:
        t1 = self.repository.create_task("Задача 1", datetime.now())
        t2 = self.repository.create_task("Задача 2", datetime.now())
        self.repository.update_task_status(t2.id, TaskStatus.DONE)

        all_tasks = self.repository.get_all_tasks()
        self.assertEqual(len(all_tasks), 2)

        done_tasks = self.repository.filter_by_status(TaskStatus.DONE)
        self.assertEqual(len(done_tasks), 1)
        self.assertEqual(done_tasks[0].id, t2.id)

    def test_update_details_and_delete(self) -> None:
        task = self.repository.create_task("Старий опис", datetime.now())
        new_date = datetime(2026, 12, 31, 18, 0)
        self.repository.update_task_details(task.id, description="Новий опис", schedule_for=new_date)

        updated = self.repository.get_task_by_id(task.id)
        self.assertEqual(updated.description, "Новий опис")
        self.assertEqual(updated.schedule_for, new_date)

        deleted = self.repository.delete_task(task.id)
        self.assertTrue(deleted)
        self.assertIsNone(self.repository.get_task_by_id(task.id))
        self.assertFalse(self.repository.delete_task(uuid.uuid4()))

    def test_controller_operations(self) -> None:
        self.controller.add_task("Через контролер", "2026-11-20 12:30")
        self.controller.add_task("Погана дата", "неправильна-дата")

        tasks = self.repository.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        task_id_str = str(tasks[0].id)

        self.controller.change_status(task_id_str, "2")
        self.assertEqual(self.repository.get_task_by_id(tasks[0].id).status, TaskStatus.IN_PROGRESS)

        self.controller.change_status(task_id_str, "99")
        self.controller.change_status("bad-uuid", "1")

        self.controller.edit_task(task_id_str, "Оновлено контролером", "")
        self.assertEqual(self.repository.get_task_by_id(tasks[0].id).description, "Оновлено контролером")

        self.controller.show_all_tasks()
        self.controller.filter_tasks_by_status("2")
        self.controller.show_task_by_id(task_id_str)

        self.controller.delete_task(task_id_str)
        self.assertEqual(len(self.repository.get_all_tasks()), 0)


if __name__ == "__main__":
    unittest.main()