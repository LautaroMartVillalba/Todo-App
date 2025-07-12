"""
Module: Task Management

This module provides functionality to manage tasks
persistence to both an SQLiten database and a JSON file, retrieval, update, and deletion.
It also handles associated image and file directories through delegation to external managers
(images_manager and files_manager respectively).

Attributes:
    BASE_DIR (Path): Root directory of the project.
    default_directory (Path): Full path to the default JSON file for storing task data.
"""

import uuid
import os
import json
from pathlib import Path

from backend.managers import files_manager
from backend.managers import images_manager
from backend.models import task
from backend.database import db_manager

BASE_DIR = Path().resolve().parent
default_directory = BASE_DIR / 'database/tasks.json'

def create_task(title, description, init_date, termination_date, images_directories, files_directories):
    """
    Creates a new task and persists it in both the SQLite database and the local JSON file.
    Also stores the provided image and file directories associated with the task.

    Args:
        title (str): Title of the task.
        description (str): Description of the task.
        init_date (str): Task start date.
        termination_date (str): Task end date.
        images_directories (list[str]): List of image directory paths related to the task.
        files_directories (list[str]): List of file directory paths related to the task.

    Returns:
        dict: The complete task object with metadata and related files/images.
    """
    new_task = task.Task(title, description, init_date, termination_date)
    task_id = uuid.uuid4().__str__()

    add_task_to_json(new_task)
    save_task_in_db(task_id, new_task)
    images_manager.save_images_directories_in_db(task_id, images_directories)
    files_manager.save_files_directories_in_db(task_id, files_directories)

    return get_task_by_id(task_id)

def add_task_to_json(task_data):
    """
    Appends the given task to a JSON file.

    Args:
        task_data (Task): The task object to be stored with attributes such as
                          title, description, init_date, and termination_date.
    """
    if not os.path.isfile(default_directory):
        create_json_at_first_time = open(default_directory, 'w', encoding='utf-8')
        json.dump({}, create_json_at_first_time, indent=2)

    with open(default_directory, 'r', encoding='utf-8') as json_read:
        try:
            tasks_data = json.load(json_read)
        except json.JSONDecodeError:
            tasks_data = {}

    task_name = len(tasks_data) +1

    tasks_data[task_name] = {
            "title": task_data.title,
            "description": task_data.description,
            "init_date": task_data.init_date,
            "termination_date": task_data.termination_date
    }

    with open(default_directory, 'w', encoding='utf-8') as f:
        json.dump(tasks_data, f, indent=2)

# ////////////////////////////////////DB methods////////////////////////////////////

def save_task_in_db(task_id, task_data):
    """
    Persists a task's metadata in the database.

    Args:
        task_id (str): UUID used as the unique identifier for the task.
        task_data (Task): Task object containing metadata to store.
    """
    with db_manager.call_new_cursor() as (cursor, connection):
        cursor.execute(
            f"""INSERT INTO {db_manager.task_table_name}
            (task_id, title, description, init_date, termination_date
            ) VALUES (?,?,?,?,?)""", (
                task_id,
                task_data.title,
                task_data.description,
                task_data.init_date,
                task_data.termination_date
            ))
        connection.commit()


# ------------------------------------------get data methods----------------------------------
def get_all_tasks():
    """
    Retrieves all tasks from the database, including associated image and file directories.

    Returns:
        dict: A dictionary where each key is a task ID and the value is a dictionary
              of task metadata and associated directories.
    """
    all_tasks_dict = {}
    with db_manager.call_new_cursor() as (cursor, connection):
        all_tasks_list = cursor.execute(f"SELECT * FROM {db_manager.task_table_name}").fetchall()
        for each in all_tasks_list:

            all_tasks_dict[each[0]] = {
                "title": each[1],
                "description": each[2],
                "init_date": each[3],
                "termination_date": each[4],
                "images_directories": images_manager.get_image_by_task_id(each[0]),
                "files_directories": files_manager.get_file_by_task_id(each[0])
            }

    return all_tasks_dict


def get_task_by_id(task_id):
    """
    Retrieves a task from the database using its unique task ID.

    Args:
        task_id (str): The UUID string of the task.

    Returns:
        dict: Task metadata along with image and file directories.
    """

    with db_manager.call_new_cursor() as (cursor, connection):
        task_query = cursor.execute(
        f"select * from {db_manager.task_table_name} where task_id = '" + task_id + "'"
        ).fetchone()

    task_info_in_dict = {
        "id" : task_query[0],
        "title": task_query[1],
        "description": task_query[2],
        "init_date": task_query[3],
        "termination_date": task_query[4],
        "images_directories": images_manager.get_image_by_task_id(task_id),
        "files_directories": files_manager.get_file_by_task_id(task_id)
    }

    return task_info_in_dict

# ---------------------------------------update data methods---------------------------------------
def update_task_info_by_id(task_id, title=None, description=None, init_date=None, termination_date=None, image_id =None, new_image_directory=None, file_id =None, new_file_directory=None):
    """
    Updates task metadata or associated directories based on provided arguments.

    Args:
        task_id (str): UUID of the task to update.
        title (str, optional): New title.
        description (str, optional): New description.
        init_date (str, optional): New start date.
        termination_date (str, optional): New end date.
        image_id (str, optional): Image ID to update.
        new_image_directory (str, optional): New image directory path.
        file_id (str, optional): File ID to update.
        new_file_directory (str, optional): New file directory path.

    Returns:
        dict: Updated task metadata and associated file/image directories.
    """

    if title is not None:
        with db_manager.call_new_cursor() as (cursor, connection):
            cursor.execute(
                f"UPDATE {db_manager.task_table_name} SET title = ? WHERE task_id ='" + task_id + "'", title
            )
    if description is not None:
        with db_manager.call_new_cursor() as (cursor, connection):
            cursor.execute(
                f"UPDATE {db_manager.task_table_name} SET description = ? WHERE task_id ='" + task_id + "'", description
            )
    if init_date is not None:
        with db_manager.call_new_cursor() as (cursor, connection):
            cursor.execute(
                f"UPDATE {db_manager.task_table_name} SET init_date = ? WHERE task_id ='" + task_id + "'", init_date
            )
    if termination_date is not None:
        with db_manager.call_new_cursor() as (cursor, connection):
            cursor.execute(
                f"UPDATE {db_manager.task_table_name} SET termination_date = ? WHERE task_id ='" + task_id + "'", termination_date
            )
    if image_id is not None and new_image_directory is not None:
        images_manager.update_images_direct_info_by_id(image_id, new_image_directory)
    if file_id is not None and new_file_directory is not None:
        files_manager.update_files_direct_info_by_id(file_id, new_file_directory)

    modified_task = get_task_by_id(task_id)
    return modified_task



# ---------------------------------delete data methods-----------------------------------
def delete_task_images_and_files_by_task_id(task_id):
    """
    Deletes a task and its associated image and file records from the database.

    Args:
        task_id (str): UUID of the task to be deleted.
    """

    with db_manager.call_new_cursor() as (cursor, connection):
        cursor.execute(f"DELETE FROM {db_manager.task_table_name} WHERE task_id = '" + task_id + "'"
                                  )
        cursor.execute(f"DELETE FROM {db_manager.images_table_name} WHERE task_id = '" + task_id + "'"
                                  )
        cursor.execute(f"DELETE FROM {db_manager.files_table_name} WHERE task_id = '" + task_id + "'"
                              )
