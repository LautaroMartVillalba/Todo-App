from backend.database import db_manager
import uuid
import json
from task_manager import get_task_by_id

def save_files_directories_in_db(task_id, image_directory):
    file_direct = []

    if isinstance(image_directory, list):
        for element in image_directory:
            file_direct.append(element)
    else:
        file_direct.append(image_directory)

    for each in file_direct:
        unique_id = uuid.uuid4().__str__()
        db_manager.cursor.execute(
            f"""INSERT INTO {db_manager.files_table_name} (file_id, directory, task_id) VALUES(?,?,?)""", (unique_id, each, task_id)
        )
    db_manager.connection.commit()


def get_file_by_id(file_id):
    query = db_manager.cursor.execute(
        f"select * from {db_manager.files_table_name} where file_id = '" + file_id + "'"
    ).fetchone()

    file_dict = {
        "image_id": query[0],
        "directory": query[1]
    }

    return json.dumps(file_dict, ensure_ascii=False, indent=2).encode('utf8').decode()

def get_file_by_task_id(task_id):
    images_list = db_manager.cursor.execute(
        f"select * from {db_manager.files_table_name} where task_id = '" + task_id + "'"
    ).fetchall()

    files_dict = {}

    for each in images_list:
        files_dict[each[0]] = {
            "directory": each[1]
        }

    return json.dumps(files_dict, ensure_ascii=False, indent=2).encode('utf8').decode()

def update_files_direct_info_by_id(task_id, file_id, directory):
    db_manager.cursor.execute(
        f"UPDATE {db_manager.files_table_name} SET directory = ? WHERE file_id = ?", (directory, file_id)
    )
    db_manager.connection.commit()

    return get_task_by_id(task_id)

def delete_file_by_id(file_id):
    db_manager.cursor.execute(
        f"DELETE FROM {db_manager.files_table_name} WHERE file_id = '" + file_id + "'"
    )
    db_manager.connection.commit()