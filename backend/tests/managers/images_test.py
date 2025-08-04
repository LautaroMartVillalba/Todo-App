import os
import shutil
import sqlite3
import unittest
import uuid
from pathlib import Path

from backend.database import db_manager
from backend.managers import images_manager
from backend.tests.test_files_and_images.FilesEnum import File

class ImagesTests(unittest.TestCase):
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

    def test_save_single_image_directory(self):
        task_id = str(uuid.uuid4())
        image_path = File.SOMBRERO_GALAXY_JPG.value.__str__()
        images_manager.save_images_directories_in_db(task_id, image_path)

        image_id = None
        with db_manager.call_new_cursor() as (cursor, connection):
            query_result = cursor.execute(
                f"""SELECT * FROM {db_manager.images_table_name} WHERE task_id = ?""", (task_id,)
            ).fetchone()
            image_id = str(query_result[0])

        copied_dir = Path(__file__).parent.parent / 'user_folder' / 'images' / str(task_id)
        copied_files = os.listdir(copied_dir)
        self.assertEqual(len(copied_files), 1)
        self.assertTrue(copied_files[0].endswith(os.path.basename(image_path)))

        # delete the generated folder
        shutil.rmtree(copied_dir.parent.parent)

    def test_save_multiple_image_directories(self):
        task_id = str(uuid.uuid4())
        image_one = File.SOMBRERO_GALAXY_JPG.value
        image_two = File.HEIC_1311_A_JPG.value
        image_paths = [image_one, image_two]

        images_manager.save_images_directories_in_db(task_id, image_paths)

        result = None
        with db_manager.call_new_cursor() as (cursor, connection):
            result = cursor.execute("SELECT * FROM " + db_manager.images_table_name + " WHERE task_id = ?",
                                (task_id,)).fetchall()

        self.assertEqual(len(result), 2)
        for each in result:
            self.assertIn(Path(each[1]), image_paths)

        copied_dir = Path(__file__).parent.parent / 'user_folder' / 'images' / str(task_id)
        copied_files = os.listdir(copied_dir)
        self.assertEqual(len(copied_files), 2)
        for each in image_paths:
            self.assertTrue(any(f.endswith(os.path.basename(each)) for f in copied_files))

        shutil.rmtree(copied_dir)

    def test_get_image_by_id_with_single_image(self):
        task_id = str(uuid.uuid4())
        image_path = File.SOMBRERO_GALAXY_JPG.value

        images_manager.save_images_directories_in_db(task_id, image_path)

        with db_manager.call_new_cursor() as (cursor, connection):
            result = cursor.execute(
                f"SELECT * FROM {db_manager.images_table_name} WHERE task_id = ?", (task_id,)
            ).fetchone()
            image_id = result[0]
            original_path = result[1]

        image_data = images_manager.get_image_by_id(image_id)

        self.assertEqual(image_data["image_id"], image_id)
        self.assertEqual(image_data["directory"], original_path)

        copied_dir = Path(__file__).parent.parent / 'user_folder' / 'images' / str(task_id)
        shutil.rmtree(copied_dir.parent.parent)

    def test_get_image_by_id_with_multiple_images(self):
        task_id = str(uuid.uuid4())
        image_paths = [File.SOMBRERO_GALAXY_JPG.value, File.HEIC_1311_A_JPG.value]

        images_manager.save_images_directories_in_db(task_id, image_paths)

        with db_manager.call_new_cursor() as (cursor, connection):
            results = cursor.execute(
                f"SELECT * FROM {db_manager.images_table_name} WHERE task_id = ?", (task_id,)
            ).fetchall()

        for image_id, path, id_from_related_task in results:
            image_data = images_manager.get_image_by_id(image_id)
            self.assertEqual(image_data["image_id"], image_id)
            self.assertEqual(image_data["directory"], path)

        copied_dir = Path(__file__).parent.parent / 'user_folder' / 'images' / str(task_id)
        shutil.rmtree(copied_dir)

    def test_get_image_by_task_id_single_image(self):
        task_id = str(uuid.uuid4())
        image_path = File.SOMBRERO_GALAXY_JPG.value
        images_manager.save_images_directories_in_db(task_id, image_path)

        result = images_manager.get_image_by_task_id(task_id)

        self.assertEqual(len(result), 1)
        image_id, data = list(result.items())[0]
        self.assertTrue(image_id)
        self.assertEqual(Path(data["directory"]), image_path)

        copied_dir = Path(__file__).parent.parent / 'user_folder' / 'images' / str(task_id)
        shutil.rmtree(copied_dir)

    def test_get_image_by_task_id_multiple_images(self):
        task_id = str(uuid.uuid4())
        image_paths = [File.SOMBRERO_GALAXY_JPG.value, File.HEIC_1311_A_JPG.value]
        images_manager.save_images_directories_in_db(task_id, image_paths)

        result = images_manager.get_image_by_task_id(task_id)

        self.assertEqual(len(result), 2)
        retrieved_paths = [Path(v["directory"]) for v in result.values()]
        for p in image_paths:
            self.assertIn(p, retrieved_paths)

        copied_dir = Path(__file__).parent.parent / 'user_folder' / 'images' / str(task_id)
        shutil.rmtree(copied_dir)

    def test_get_image_by_task_id_none(self):
        task_id = str(uuid.uuid4())

        result = images_manager.get_image_by_task_id(task_id)

        self.assertEqual(result, {})

    def test_delete_image_by_id_existing(self):
        task_id = str(uuid.uuid4())
        image_path = File.SOMBRERO_GALAXY_JPG.value
        images_manager.save_images_directories_in_db(task_id, image_path)

        image_id = None
        with db_manager.call_new_cursor() as (cursor, connection):
            query_result = cursor.execute(
                f"SELECT * FROM {db_manager.images_table_name} WHERE task_id = ?", (task_id,)
            ).fetchone()
            image_id = str(query_result[0])

        images_manager.delete_image_by_id(image_id)

        with db_manager.call_new_cursor() as (cursor, connection):
            deleted_check = cursor.execute(
                f"SELECT * FROM {db_manager.images_table_name} WHERE image_id = ?", (image_id,)
            ).fetchone()
            self.assertIsNone(deleted_check)

        copied_dir = Path(__file__).parent.parent / 'user_folder' / 'images' / str(task_id)
        shutil.rmtree(copied_dir)

    @classmethod
    def tearDown(cls):
        cls.connection.close()