import os
import shutil
import sqlite3
import unittest
import uuid
from pathlib import Path

from backend.database import db_manager
from backend.managers import files_manager
from backend.tests.test_files_and_images.FilesEnum import File

class FilesTests(unittest.TestCase):
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

    def test_save_single_file_directory(self):
        task_id = str(uuid.uuid4())
        file = File.SOMBRERO_GALAXY_JPG.value.__str__()

        files_manager.save_files_directories_in_db(task_id, file)

        with db_manager.call_new_cursor() as (cursor, connection):
            query_result = cursor.execute(
                f"SELECT * FROM {db_manager.files_table_name} WHERE task_id = ?", (task_id,)
            ).fetchone()
            self.assertEqual(query_result[1], file)
            self.assertEqual(query_result[2], task_id)

        copied_dir = Path(__file__).parent.parent / 'user_folder' / 'files' / task_id
        copied_files = os.listdir(copied_dir)
        self.assertEqual(len(copied_files), 1)
        self.assertTrue(copied_files[0].endswith(os.path.basename(file)))

        shutil.rmtree(copied_dir.parent.parent)

    def test_save_multiple_file_directories(self):
        task_id = str(uuid.uuid4())
        file_one = File.SOMBRERO_GALAXY_JPG.value
        file_two = File.HEIC_1311_A_JPG.value
        file_paths = [file_one, file_two]

        files_manager.save_files_directories_in_db(task_id, file_paths)

        with db_manager.call_new_cursor() as (cursor, connection):
            results = cursor.execute(
                f"SELECT * FROM {db_manager.files_table_name} WHERE task_id = ?", (task_id,)
            ).fetchall()
            self.assertEqual(len(results), 2)
            for row in results:
                self.assertIn(Path(row[1]), file_paths)

        copied_dir = Path(__file__).parent.parent / 'user_folder' / 'files' / task_id
        copied_files = os.listdir(copied_dir)
        self.assertEqual(len(copied_files), 2)
        for each in file_paths:
            self.assertTrue(any(f.endswith(os.path.basename(each)) for f in copied_files))

        shutil.rmtree(copied_dir)

    def test_get_file_by_id(self):
        task_id = str(uuid.uuid4())
        file_path = File.SOMBRERO_GALAXY_JPG.value.__str__()

        files_manager.save_files_directories_in_db(task_id, file_path)

        file_data = files_manager.get_file_by_task_id(task_id)
        file_id = list(file_data)[0]
        self.assertEqual(file_data[file_id]["directory"], file_path)

    def test_get_file_by_task_id_returns_all_files(self):
        task_id = str(uuid.uuid4())

        file_1 = str(File.SOMBRERO_GALAXY_JPG.value)
        file_2 = str(File.CRAB_NEBULA_PDF.value)

        files_manager.save_files_directories_in_db(task_id, [file_1, file_2])

        files = files_manager.get_file_by_task_id(task_id)
        files_ids = list(files)

        self.assertEqual(len(files), 2)
        self.assertEqual(files[files_ids[0]]["directory"], file_1)
        self.assertEqual(files[files_ids[1]]["directory"], file_2)

    def test_delete_file_by_id_removes_file_from_database(self):
        task_id = str(uuid.uuid4())
        file_path = str(File.STARS_CSV.value)

        files_manager.save_files_directories_in_db(task_id, file_path)

        with db_manager.call_new_cursor() as (cursor, _):
            exists_before = cursor.execute(
                f"SELECT COUNT(*) FROM {db_manager.files_table_name} WHERE task_id = ?", (task_id,)
            ).fetchone()[0]
        self.assertEqual(exists_before, 1)

        file_id = list(files_manager.get_file_by_task_id(task_id))[0]
        files_manager.delete_file_by_id(file_id)

        # Verificamos que fue eliminado
        with db_manager.call_new_cursor() as (cursor, _):
            exists_after = cursor.execute(
                f"SELECT COUNT(*) FROM {db_manager.files_table_name} WHERE file_id = ?", (file_id,)
            ).fetchone()[0]
        self.assertEqual(exists_after, 0)

    @classmethod
    def tearDown(cls):
        cls.connection.close()