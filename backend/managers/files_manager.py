"""
Module: File Directory Manager

This module provides functions to manage file directory records associated
with tasks. It handles insertion, retrieval, update, and deletion of file paths
in the task-related database table.

Functions:
    - save_files_directories_in_db
    - get_file_by_id
    - get_file_by_task_id
    - update_files_direct_info_by_id
    - delete_file_by_id
"""
from backend.database import db_manager
import uuid

def save_files_directories_in_db(task_id, image_directory):
    """
    Persists one or multiple file directory paths to the database,
    associating them with a given task ID.

    Args:
        task_id (str): UUID of the task to which the files are related.
        image_directory (str or list[str]): A single path or a list of paths
                                            to file directories that should be saved.
    """
    file_direct = []

    if isinstance(image_directory, list):
        for element in image_directory:
            file_direct.append(element)
    else:
        file_direct.append(image_directory)

    for each in file_direct:
        with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
            unique_id = uuid.uuid4().__str__()
            cursor.execute(
                f"""INSERT INTO {db_manager.files_table_name} (file_id, directory, task_id) VALUES(?,?,?)""", (unique_id, each, task_id)
            )
            connection.commit()


def get_file_by_id(file_id):
    """
    Retrieves a file record from the database using its unique file ID.

    Args:
        file_id (str): UUID of the file record to be retrieved.

    Returns:
        dict: Dictionary containing file ID and its directory path.
              Format: {"image_id": ..., "directory": ...}
    """
    with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
        query = cursor.execute(
            f"select * from {db_manager.files_table_name} where file_id = '" + file_id + "'"
        ).fetchone()

    file_dict = {
        "file_id": query[0],
        "directory": query[1]
    }

    return file_dict

def get_file_by_task_id(task_id):
    """
    Retrieves all file records associated with a specific task ID.

    Args:
        task_id (str): UUID of the task for which to retrieve associated files.

    Returns:
        dict: A dictionary where each key is the file ID and the value is
              a dictionary containing the directory path.
              Format:
              {
                  "file_id_1": { "directory": ... },
                  "file_id_2": { "directory": ... },
                  ...
              }
    """
    with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
        images_list = cursor.execute(
            f"select * from {db_manager.files_table_name} where task_id = '" + task_id + "'"
        ).fetchall()

    files_dict = {}

    for each in images_list:
        files_dict[each[0]] = {
            "directory": each[1]
        }

    return files_dict

def update_files_direct_info_by_id(file_id, directory):
    """
    Updates the directory path of a file entry identified by its file ID.

    Args:
        file_id (str): UUID of the file to be updated.
        directory (str): New directory path to assign to the file.
    """
    with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
        cursor.execute(
            f"UPDATE {db_manager.files_table_name} SET directory = ? WHERE file_id = '" + file_id + "'", directory
        )


def delete_file_by_id(file_id):
    """
    Deletes a file record from the database using its unique file ID.

    Args:
        file_id (str): UUID of the file record to delete.
    """
    with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
        cursor.execute(
            f"DELETE FROM {db_manager.files_table_name} WHERE file_id = '" + file_id + "'"
        )
