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
    """Create a new Task object and call add_tas_to_json(x) and save_task_in_db(x) methods.

    Return Task object."""
    new_task = task.Task(title, description, init_date, termination_date)
    task_id = uuid.uuid4().__str__()

    add_task_to_json(new_task)
    save_task_in_db(task_id, new_task)
    images_manager.save_images_directories_in_db(task_id, images_directories)
    files_manager.save_files_directories_in_db(task_id, files_directories)

    return get_task_by_id(task_id)

def add_task_to_json(task_data):
    """Adds to an existing (or create it if not exists) JSON dedicated file the inputted task data."""

    # If the file does not exist, it creates.
    if not os.path.isfile(default_directory):
        create_json_at_first_time = open(default_directory, 'w', encoding='utf-8')
        json.dump({}, create_json_at_first_time, indent=2)

    # Reads the JSON file.
    with open(default_directory, 'r', encoding='utf-8') as json_read:
        try:
            tasks_data = json.load(json_read)
        except json.JSONDecodeError:
            tasks_data = {}

    # Assigns a new position in the JSON file.
    task_name = len(tasks_data) +1

    # Set the Task data.
    tasks_data[task_name] = {
            "title": task_data.title,
            "description": task_data.description,
            "init_date": task_data.init_date,
            "termination_date": task_data.termination_date
    }

    with open(default_directory, 'w', encoding='utf-8') as f:
        json.dump(tasks_data, f, indent=2)

# ////////////////////////////////////DB methods////////////////////////////////////

# -------------------------------------save data methods--------------------------------------
def save_task_in_db(task_id, task_data):
    """Saves the task data in the local DataBase."""
    # SQL command.
    with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
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
        # Save changes.
        connection.commit()


# ------------------------------------------get data methods----------------------------------
def get_all_tasks():
    """Search all tasks saved in the DataBase.

    Return list of JSON with tasks data."""
    all_tasks_dict = {}
    with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
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

    return json.dumps(all_tasks_dict, indent=2, ensure_ascii=False).encode('utf8').decode()


def get_task_by_id(task_id):
    """Find and retrieve a task in the DataBase by her ID.

    Return JSON with task data."""

    with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
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

    return json.dumps(task_info_in_dict, ensure_ascii=False, indent=2).encode('utf8').decode()

# ---------------------------------------update data methods---------------------------------------
def update_task_info_by_id(task_id, title=None, description=None, init_date=None, termination_date=None, image_id =None, new_image_directory=None, file_id =None, new_file_directory=None):
    """Update task info by her id."""

    if title is not None:
        with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
            cursor.execute(
                f"UPDATE {db_manager.task_table_name} SET title = ? WHERE '" + task_id + "'", title
            )
    if description is not None:
        with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
            cursor.execute(
                f"UPDATE {db_manager.task_table_name} SET description = ? WHERE '" + task_id + "'", description
            )
    if init_date is not None:
        with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
            cursor.execute(
                f"UPDATE {db_manager.task_table_name} SET init_date = ? WHERE '" + task_id + "'", init_date
            )
    if termination_date is not None:
        with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
            cursor.execute(
                f"UPDATE {db_manager.task_table_name} SET termination_date = ? WHERE '" + task_id + "'", termination_date
            )
    if image_id is not None and new_image_directory is not None:
        images_manager.update_images_direct_info_by_id(image_id, new_image_directory)
    if file_id is not None and new_file_directory is not None:
        files_manager.update_files_direct_info_by_id(file_id, new_file_directory)

    modified_task = get_task_by_id(task_id)
    return modified_task



# ---------------------------------delete data methods-----------------------------------
def delete_task_images_and_files_by_task_id(task_id):
    """Delete a task saved in the DataBase by her ID."""

    with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
        cursor.execute(f"DELETE FROM {db_manager.task_table_name} WHERE task_id = '" + task_id + "'"
                                  )
        cursor.execute(f"DELETE FROM {db_manager.images_table_name} WHERE task_id = '" + task_id + "'"
                                  )
        cursor.execute(f"DELETE FROM {db_manager.files_table_name} WHERE task_id = '" + task_id + "'"
                              )
