import sqlite3
from contextlib import contextmanager
from pathlib import Path

BASE_DIR = Path().resolve().parent
DB_PATH = BASE_DIR / 'database' / 'tasks_db.sqlite'

task_table_name = 'task_table'
images_table_name = 'images_table'
files_table_name = 'files_table'

def init_db():
    cursor, connection = call_new_cursor(DB_PATH)

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS " + task_table_name + "(task_id TEXT,"
                                                          " title,"
                                                          " description,"
                                                          " init_date,"
                                                          " termination_date)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS " + images_table_name + "(image_id TEXT PRIMARY KEY,"
                                                            " directory TEXT,"
                                                            " task_id INTEGER,"
                                                            "FOREIGN KEY (task_id) REFERENCES " + task_table_name + "(task_id))")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS " + files_table_name + "(file_id TEXT PRIMARY KEY,"
                                                           " directory TEXT,"
                                                           " task_id INTEGER,"
                                                           "FOREIGN KEY (task_id) REFERENCES " + task_table_name + "(task_id))")

    cursor.close()

shared_connection = None

def set_shared_connection(connection):
    global shared_connection
    shared_connection = connection

@contextmanager
def call_new_cursor(data_base_dir):
    if shared_connection:
        cursor = shared_connection.cursor()
        yield cursor, shared_connection
        shared_connection.commit()
    else:
        connection = sqlite3.connect(DB_PATH)
        try:
            cursor = connection.cursor()
            yield cursor, connection
            connection.commit()
        finally:
            connection.close()