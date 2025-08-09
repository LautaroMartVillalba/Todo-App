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

DB_PATH = Path().resolve().parent / 'database' / 'tasks_db.sqlite'

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
    with call_new_cursor() as (cursor, connection):
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


shared_connection = None

def set_shared_connection(connection):
    """
    Set the global shared SQLite connection for use across the application.
    
    This connection will be reused by the `call_new_cursor` context manager to ensure consistent database access.
    """
    global shared_connection
    shared_connection = connection

@contextmanager
def call_new_cursor(path=DB_PATH):
    """
    Context manager that yields an SQLite cursor and connection for database operations.
    
    If a shared connection is set, yields a cursor from it and commits changes after use. Otherwise, creates a new connection to the specified database path, yields a cursor and connection, commits changes, and closes the connection upon exit.
    
    Parameters:
        path (Path or str, optional): Path to the SQLite database file. Defaults to DB_PATH.
    
    Yields:
        tuple: (cursor, connection) for executing database operations.
    """
    if shared_connection:
        cursor = shared_connection.cursor()
        yield cursor, shared_connection
        shared_connection.commit()
    else:
        connection = sqlite3.connect(path)
        try:
            cursor = connection.cursor()
            yield cursor, connection
            connection.commit()
        finally:
            connection.close()
