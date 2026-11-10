from datetime import datetime
import unittest
import uuid

from controllers import TaskController
from models7 import TaskModel, TaskStatus
from views import TaskView


class TestTaskModel(unittest.TestCase):
    def setUp(self) -> None:
        self.model = TaskModel()

    def test_create_task(self) -> None:
        now = datetime.now()
        task = self.model.create_task("Тестова задача", now)
        self.assertEqual(task.description, "Тестова задача")
        self.assertEqual(task.status, TaskStatus.TODO)
        self.assertIsInstance(task.id, uuid.UUID)

    def test_get_all_tasks(self) -> None:
        self.model.create_task("T1", datetime.now())
        self.model.create_task("T2", datetime.now())
        self.assertEqual(len(self.model.get_all_tasks()), 2)

    def test_get_task_by_id(self) -> None:
        task = self.model.create_task("T1", datetime.now())
        found = self.model.get_task_by_id(task.id)
        self.assertEqual(found, task)
        self.assertIsNone(self.model.get_task_by_id(uuid.uuid4()))

    def test_filter_by_status(self) -> None:
        t1 = self.model.create_task("T1", datetime.now())
        t2 = self.model.create_task("T2", datetime.now())
        self.model.update_task_status(t2.id, TaskStatus.DONE)

        todo_tasks = self.model.filter_by_status(TaskStatus.TODO)
        done_tasks = self.model.filter_by_status(TaskStatus.DONE)

        self.assertIn(t1, todo_tasks)
        self.assertNotIn(t2, todo_tasks)
        self.assertIn(t2, done_tasks)

    def test_update_status(self) -> None:
        task = self.model.create_task("T1", datetime.now())
        self.model.update_task_status(task.id, TaskStatus.IN_PROGRESS)
        self.assertEqual(task.status, TaskStatus.IN_PROGRESS)

    def test_update_details(self) -> None:
        task = self.model.create_task("Старий опис", datetime.now())
        new_time = datetime.now()
        self.model.update_task_details(task.id, description="Новий опис", schedule_for=new_time)
        self.assertEqual(task.description, "Новий опис")
        self.assertEqual(task.schedule_for, new_time)

    def test_delete_task(self) -> None:
        task = self.model.create_task("T1", datetime.now())
        self.assertTrue(self.model.delete_task(task.id))
        self.assertIsNone(self.model.get_task_by_id(task.id))
        self.assertFalse(self.model.delete_task(uuid.uuid4()))


class TestTaskController(unittest.TestCase):
    def setUp(self) -> None:
        self.model = TaskModel()
        self.view = TaskView()
        self.controller = TaskController(self.model, self.view)

    def test_add_task_valid(self) -> None:
        self.controller.add_task("Контролер тест", "2026-12-31 15:00")
        tasks = self.model.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].description, "Контролер тест")

    def test_add_task_invalid_date(self) -> None:
        self.controller.add_task("Помилкова дата", "не-дата")
        self.assertEqual(len(self.model.get_all_tasks()), 0)

    def test_change_status(self) -> None:
        task = self.model.create_task("T1", datetime.now())
        self.controller.change_status(str(task.id), "2")
        self.assertEqual(task.status, TaskStatus.IN_PROGRESS)

        self.controller.change_status(str(task.id), "99")
        self.controller.change_status(str(uuid.uuid4()), "1")
        self.controller.change_status("invalid-uuid", "1")

    def test_delete_task(self) -> None:
        task = self.model.create_task("T1", datetime.now())
        self.controller.delete_task(str(task.id))
        self.assertEqual(len(self.model.get_all_tasks()), 0)
        self.controller.delete_task(str(uuid.uuid4()))
        self.controller.delete_task("invalid-uuid")

    def test_edit_task(self) -> None:
        task = self.model.create_task("Опис", datetime.now())
        self.controller.edit_task(str(task.id), "Оновлений опис", "2026-10-10 10:00")
        self.assertEqual(task.description, "Оновлений опис")

        self.controller.edit_task(str(task.id), "", "")
        self.controller.edit_task(str(uuid.uuid4()), "Новий", "")
        self.controller.edit_task("invalid-uuid", "Новий", "")
        self.controller.edit_task(str(task.id), "Новий", "невідома-дата")

    def test_views_and_filters(self) -> None:
        task = self.model.create_task("T1", datetime.now())
        self.controller.show_all_tasks()
        self.controller.filter_tasks_by_status("1")
        self.controller.filter_tasks_by_status("bad_choice")
        self.controller.show_task_by_id(str(task.id))
        self.controller.show_task_by_id(str(uuid.uuid4()))
        self.controller.show_task_by_id("invalid-uuid")


if __name__ == "__main__":
    unittest.main()