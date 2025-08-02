import json
import sqlite3
import unittest
import uuid

from backend.database import db_manager
from backend.managers import task_manager
from backend.tests.test_files_and_images.FilesEnum import File
from backend.models.task import Task

class TaskTests(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.connection = sqlite3.connect(':memory:')
        db_manager.set_shared_connection(cls.connection)

        cursor = cls.connection.cursor()
        db_manager.DB_PATH = ':memory:'

        cursor.execute("CREATE TABLE IF NOT EXISTS "
                       + db_manager.task_table_name +
                       "(task_id TEXT,"
                       " title,"
                       "description,"
                       " init_date," " termination_date)")

        cursor.execute("CREATE TABLE IF NOT EXISTS "
                       + db_manager.images_table_name +
                       "(image_id TEXT PRIMARY KEY,"
                       " directory TEXT,"
                       " task_id INTEGER,"
                       "FOREIGN KEY (task_id) REFERENCES "+ db_manager.task_table_name + "(task_id))")

        cursor.execute("CREATE TABLE IF NOT EXISTS "
                       + db_manager.files_table_name +
                       "(file_id TEXT PRIMARY KEY,"
                        " directory TEXT,"
                       " task_id INTEGER,"
                       "FOREIGN KEY (task_id) REFERENCES " + db_manager.task_table_name + "(task_id))")

    def test_if_create_task_method_save_correctly_data(self):
        method = task_manager.create_task('Testing','testing desc','2025-01-01','2025-02-01', [File.HEIC_1311_A_JPG.value, File.SOMBRERO_GALAXY_JPG.value], File.DEEP_SPACE_CSV.value)
        with db_manager.call_new_cursor() as (cursor, connection):
            task_query = cursor.execute(f"SELECT * FROM {db_manager.task_table_name} WHERE title = 'Testing'").fetchone()

            self.assertIsNotNone(method)
            self.assertEqual(method['title'], task_query[1])
            self.assertEqual(method['description'], task_query[2])
            self.assertEqual(method['init_date'], task_query[3])
            self.assertEqual(method['termination_date'], task_query[4])
            image_rows = cursor.execute(f"SELECT COUNT(*) FROM {db_manager.images_table_name} WHERE task_id = ?",
                                        (task_query[0],)).fetchone()[0]
            file_rows = cursor.execute(f"SELECT COUNT(*) FROM {db_manager.files_table_name} WHERE task_id = ?",
                                       (task_query[0],)).fetchone()[0]
            self.assertGreaterEqual(image_rows, 1)
            self.assertGreaterEqual(file_rows, 1)

    def test_if_create_task_method_only_accept_complete_data(self):
        with self.assertRaises(RuntimeError):
            task_manager.create_task('',
                                     'testing desc',
                                     '2025-01-01',
                                     '2025-02-01',
                                     [File.HEIC_1311_A_JPG.value, File.SOMBRERO_GALAXY_JPG.value],
                                     File.DEEP_SPACE_CSV.value)
        with self.assertRaises(RuntimeError):
            task_manager.create_task('Testing',
                                     '',
                                     '2025-01-01',
                                     '2025-02-01',
                                     [File.HEIC_1311_A_JPG.value, File.SOMBRERO_GALAXY_JPG.value],
                                     File.DEEP_SPACE_CSV.value)

        with self.assertRaises(RuntimeError):
            task_manager.create_task('Testing',
                                    'testing desc',
                                    '',
                                    '2025-02-01',
                                     [File.HEIC_1311_A_JPG.value, File.SOMBRERO_GALAXY_JPG.value],
                                     File.DEEP_SPACE_CSV.value)

        with self.assertRaises(RuntimeError):
            task_manager.create_task('Testing',
                                    'testing desc',
                                    '2025-01-01',
                                    '',
                                     [File.HEIC_1311_A_JPG.value, File.SOMBRERO_GALAXY_JPG.value],
                                     File.DEEP_SPACE_CSV.value)

    def test_if_save_task_in_db_method_save_correctly_data(self):

        fake_task_id = str(uuid.uuid4())
        task_data = Task(
            title='Dummy Task',
            description='Dummy description',
            init_date='2025-03-01',
            termination_date='2025-03-15'
        )

        task_manager.save_task_in_db(fake_task_id, task_data)

        with db_manager.call_new_cursor() as (cursor, connection):
            row = cursor.execute(f"""
                SELECT task_id, title, description, init_date, termination_date
                FROM {db_manager.task_table_name}
                WHERE task_id = ?
            """, (fake_task_id,)).fetchone()

            self.assertIsNotNone(row)
            self.assertEqual(row[0], fake_task_id)
            self.assertEqual(row[1], task_data.title)
            self.assertEqual(row[2], task_data.description)
            self.assertEqual(row[3], task_data.init_date)
            self.assertEqual(row[4], task_data.termination_date)

    def test_if_get_all_tasks_returns_correct_data(self):

        id1 = str(uuid.uuid4())
        task1 = Task(
           title='First',
          description='Desc',
          init_date='2025-01-01',
          termination_date='2025-01-02'
        )
        id2 = str(uuid.uuid4())
        task2 = Task(
           title='Second',
          description='Desc',
          init_date='2025-01-02',
          termination_date='2025-01-03'
        )

        task_manager.save_task_in_db(id1, task1)
        task_manager.save_task_in_db(id2, task2)
        all_tasks = task_manager.get_all_tasks()

        self.assertIsInstance(all_tasks, dict)
        self.assertGreaterEqual(len(all_tasks), 2)

        for task_id, task_info in all_tasks.items():
            self.assertIn("title", task_info)
            self.assertIn("description", task_info)
            self.assertIn("init_date", task_info)
            self.assertIn("termination_date", task_info)
            self.assertIn("images_directories", task_info)
            self.assertIn("files_directories", task_info)

            self.assertTrue(task_info["title"])
            self.assertTrue(task_info["description"])
            self.assertTrue(task_info["init_date"])
            self.assertTrue(task_info["termination_date"])

    def test_if_get_all_tasks_returns_empty_data_if_not_tasks_in_db(self):
        result = task_manager.get_all_tasks()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_get_all_tasks_without_related_files_or_images(self):
        task_id = str(uuid.uuid4())
        task_data = Task(
            title='test',
            description='No files/images',
            init_date='2025-01-01',
            termination_date='2025-01-02'
        )
        task_manager.save_task_in_db(task_id, task_data)

        result = task_manager.get_all_tasks()

        self.assertIn(task_id, result)
        task_entry = result[task_id]
        self.assertEqual(task_entry['title'], task_data.title)
        self.assertEqual(task_entry['description'], task_data.description)
        self.assertEqual(task_entry['init_date'], task_data.init_date)
        self.assertEqual(task_entry['termination_date'], task_data.termination_date)
        self.assertEqual(task_entry['images_directories'], {})
        self.assertEqual(task_entry['files_directories'], {})


    def test_if_get_by_id_returns_correct_data(self):
        task = task_manager.create_task('Testing',
                                'testing desc',
                                '2025-01-01',
                                '2025-01-02',
                                        [File.HEIC_1311_A_JPG.value, File.SOMBRERO_GALAXY_JPG.value],
                                        File.DEEP_SPACE_CSV.value)

        result = task_manager.get_task_by_id(task.get("id"))

        self.assertIsNotNone(result)
        self.assertIn("title", result)
        self.assertIn("description", result)
        self.assertIn("init_date", result)
        self.assertIn("termination_date", result)
        self.assertIn("images_directories", result)
        self.assertIn("files_directories", result)

        self.assertEqual(result.get("title"), task.get("title"))
        self.assertEqual(result.get("description"), task.get("description"))
        self.assertEqual(result.get("init_date"), task.get("init_date"))
        self.assertEqual(result.get("termination_date"), task.get("termination_date"))
        self.assertEqual(result.get("images_directories"), task.get("images_directories"))
        self.assertEqual(result.get("files_directories"), task.get("files_directories"))

    def test_get_task_by_id_returns_empty_dict_if_not_found(self):
        result = task_manager.get_task_by_id("non-existent-id")

        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    def test_update_task_info_updates_task_data_only(self):
        created = task_manager.create_task(
            title="Original",
            description="To update",
            init_date="2025-01-01",
            termination_date="2025-01-01",
            images_directories=[File.SOMBRERO_GALAXY_JPG.value],
            files_directories=File.STARS_CSV.value
        )
        task_id = created['id']

        updated = task_manager.update_task_info_by_id(
            task_id=task_id,
            title="Updated Title",
            description="Updated description",
            init_date="2025-01-05",
            termination_date="2025-01-15"
        )

        # Assert
        self.assertEqual(updated['title'], "Updated Title")
        self.assertEqual(updated['description'], "Updated description")
        self.assertEqual(updated['init_date'], "2025-01-05")
        self.assertEqual(updated['termination_date'], "2025-01-15")

    def test_update_task_info_does_nothing_if_no_args_provided(self):
        created = task_manager.create_task(
            title="No change",
            description="desc",
            init_date="2025-01-01",
            termination_date="2025-01-10",
            images_directories=[File.HEIC_1311_A_JPG.value],
            files_directories=File.STARS_CSV.value
        )
        task_id = created['id']

        result = task_manager.update_task_info_by_id(task_id)

        self.assertEqual(result['title'], "No change")
        self.assertEqual(result['description'], "desc")
        self.assertEqual(result['init_date'], "2025-01-01")
        self.assertEqual(result['termination_date'], "2025-01-10")
        images_ids = list(result['images_directories'])
        self.assertEqual(result['images_directories'][images_ids[0]]['directory'], File.HEIC_1311_A_JPG.value.__str__())
        files_ids = list(result['files_directories'])
        self.assertEqual(result['files_directories'][files_ids[0]]['directory'], File.STARS_CSV.value.__str__())

    def test_delete_task_images_and_files_by_task_id_removes_all_records(self):
        created = task_manager.create_task(
            title="Test task",
            description="Test desc",
            init_date="2025-01-01",
            termination_date="2025-01-02",
            images_directories=[File.SOMBRERO_GALAXY_JPG.value],
            files_directories=File.STARS_CSV.value
        )
        task_id = created["id"]

        all_tasks = task_manager.get_all_tasks()
        self.assertIn(task_id, all_tasks)
        self.assertTrue(len(all_tasks[task_id]["images_directories"]) > 0)
        self.assertTrue(len(all_tasks[task_id]["files_directories"]) > 0)

        task_manager.delete_task_images_and_files_by_task_id(task_id)

        task = task_manager.get_task_by_id(task_id)
        self.assertEqual(task, {})

    @classmethod
    def tearDown(cls):
        cls.connection.close()