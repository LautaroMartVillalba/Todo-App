"""
Module: Database Initialization and Connection Management

This module provides functionality for initializing the SQLite database schema
and handling database connections through context management.

Attributes:
    BASE_DIR (Path): The absolute path to the root directory of the project.
    DB_PATH (Path): The full path to the SQLite database file (can be changed to testing cases).
    task_table_name (str): The name of the table that stores task records.
    images_table_name (str): The name of the table that stores image records.
    files_table_name (str): The name of the table that stores file records.
    shared_connection (sqlite3.Connection | None): A global connection object
        used if explicitly set by the user.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

BASE_DIR = Path().resolve().parent
DB_PATH = BASE_DIR / 'database' / 'tasks_db.sqlite'

task_table_name = 'task_table'
images_table_name = 'images_table'
files_table_name = 'files_table'

def init_db():
    """
    Initializes the SQLite database schema by creating the task, image, and file tables
    if they do not already exist.

    Use the call_new_cursor context manager to obtain a database cursor and connection.
    Ensures the cursor is closed after execution.

    Tables created:
        - task_table: Contains task metadata including ID, title, description,
                      start and end dates.
        - images_table: Stores references to image file paths linked to specific tasks.
        - files_table: Stores references to general file paths linked to specific tasks.

    Table relationships:
        - images_table and files_table reference task_table through a foreign key
          relationship on `task_id`.
    """
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
    """
    Sets a global shared connection to be used by `call_new_cursor` for consistent
    database access throughout the application.

    Args:
        connection (sqlite3.Connection): A SQLite connection object that will be
                                         reused when accessing the database.
    """
    global shared_connection
    shared_connection = connection

@contextmanager
def call_new_cursor():
    """
    A context manager that yields an SQLite cursor and connection, using either
    a previously set shared connection or creating a new one.

    Args:
        data_base_dir (Path): The path to the database file. Although this argument
                              is accepted, the function always uses the constant DB_PATH.

    Yields:
        Tuple[cursor, connection]: A tuple consisting of the SQLite cursor and the
                                   connection it belongs to.
    """
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