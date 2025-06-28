import uuid

import task
import os
import json
import db_manager



default_directory = './app_files/tasks.json'

def create_task(title, description, init_date, termination_date, images_directories, files_directories):
    new_task = task.Task(title, description, init_date, termination_date, images_directories, files_directories)

    add_task_to_json(new_task)
    save_task_in_db(new_task)

    return new_task

def add_task_to_json(task):
    # If the file does not exist, it creates.
    if not os.path.isfile(default_directory):
        create_json_at_frist_time = open(default_directory, 'w', encoding='utf-8')
        json.dump({}, create_json_at_frist_time, indent=2)
        create_json_at_frist_time.close()

    with open(default_directory, 'r', encoding='utf-8') as json_read:
        try:
            tasks_data = json.load(json_read)
        except json.JSONDecodeError:
            tasks_data = {}
            json_read.close()
        json_read.close()

    task_name = len(tasks_data) +1

    tasks_data[task_name] = {
            "title": task.title,
            "description": task.description,
            "init_date": task.init_date,
            "termination_date": task.termination_date,
            "images_directories": task.images_directories,
            "files_directories": task.files_directories
    }

    with open(default_directory, 'w', encoding='utf-8') as f:
        json.dump(tasks_data, f, indent=2)
        f.close()

def save_task_in_db(task):
    db_manager.cursor.execute(
        f"""INSERT INTO {db_manager.task_table_name}
        (title, description, init_date, termination_date, images_directories, files_directories
        ) VALUES (?,?,?,?,?,?)""", (
            task.title,
            task.description,
            task.init_date,
            task.termination_date,
            task.images_directories,
            task.files_directories
        ))

    db_manager.connection.commit()

# retrieve
def get_all_tasks():
    result = db_manager.cursor.execute(
    f"""SELECT * FROM {db_manager.task_table_name}""").fetchall()

    #Parse to json
    task_dicc_list = []

    for element in result:
        tasks_data = {
            "id" : element[0],
            "title": element[1],
            "description": element[2],
            "init_date": element[3],
            "termination_date": element[4],
            "images_directories": element[5],
            "files_directories": element[6]
        }
        task_dicc_list.append(tasks_data)
    return json.dumps(task_dicc_list, ensure_ascii=False, indent=2).encode('utf8').decode()

def get_task_by_id(id):
    result = db_manager.cursor.execute(
    f"""SELECT * FROM {db_manager.task_table_name} WHERE id = {id}""").fetchone()

    if result is None:
        return None
    else:
        result_to_json = {
            "id" : result[0],
            "title": result[1],
            "description": result[2],
            "init_date": result[3],
            "termination_date": result[4],
            "images_directories": result[5],
            "files_directories": result[6]
        }

        return json.dumps(result_to_json, ensure_ascii=False, indent=2).encode('utf8').decode()

def update_task_info_by_id(task_id, title=None, description=None, init_date=None, termination_date=None, images_directories=None, files_directories=None):
    if title is not None:
        db_manager.cursor.execute(
            f"UPDATE {db_manager.task_table_name} SET title = ? WHERE id = ?", (title, task_id))
    if description is not None:
        db_manager.cursor.execute(
            f"UPDATE {db_manager.task_table_name} SET description = ? WHERE id = ?", (description, task_id))
    if init_date is not None:
        db_manager.cursor.execute(
            f"UPDATE {db_manager.task_table_name} SET init_date = ? WHERE id = ?", (init_date, task_id))
    if termination_date is not None:
        db_manager.cursor.execute(
            f"UPDATE {db_manager.task_table_name} SET termination_date = ? WHERE id = ?", (termination_date, task_id))
    if images_directories is not None:
        db_manager.cursor.execute(
            f"UPDATE {db_manager.task_table_name} SET images_directories = ? WHERE id = ?", (images_directories, task_id))
    if files_directories is not None:
        db_manager.cursor.execute(
            f"UPDATE {db_manager.task_table_name} SET files_directories = ? WHERE id = ?", (files_directories, task_id))

    db_manager.connection.commit()
    return get_task_by_id(task_id)

def delete_task_by_id(task_id):
    db_manager.cursor.execute(f"DELETE FROM {db_manager.task_table_name} WHERE id = ?", task_id)
    db_manager.connection.commit()