import json
import uuid

from backend.database import db_manager
from backend.managers.task_manager import get_task_by_id


def save_images_directories_in_db(task_id, image_directory):
    images_direct = []

    if isinstance(image_directory, list):
        for element in image_directory:
            images_direct.append(element)
    else:
        images_direct.append(image_directory)

    for each in images_direct:
        unique_id = uuid.uuid4().__str__()
        db_manager.cursor.execute(
            f"""INSERT INTO {db_manager.images_table_name} (image_id, directory, task_id) VALUES(?,?,?)""", (unique_id, each, task_id)
        )
    db_manager.connection.commit()

def get_image_by_id(image_id):
    query = db_manager.cursor.execute(
        f"select * from {db_manager.images_table_name} where image_id = '" + image_id + "'"
    ).fetchone()

    image_dict = {
        "image_id": query[0],
        "directory": query[1]
    }

    return json.dumps(image_dict, ensure_ascii=False, indent=2).encode('utf8').decode()

def get_image_by_task_id(task_id):
    images_list = db_manager.cursor.execute(
        f"select * from {db_manager.images_table_name} where task_id = '" + task_id + "'"
    ).fetchall()

    images_dict = {}

    for each in images_list:
        images_dict[each[0]] = {
            "directory": each[1]
        }

    return json.dumps(images_dict, ensure_ascii=False, indent=2).encode('utf8').decode()

def update_images_direct_info_by_id(task_id, image_id, directory):
    db_manager.cursor.execute(
        f"UPDATE {db_manager.images_table_name} SET directory = ? WHERE '" + image_id + "'", directory
    )
    db_manager.connection.commit()

    return get_task_by_id(task_id)


def delete_image_by_id(image_id):
    db_manager.cursor.execute(
        f"DELETE FROM {db_manager.images_table_name} WHERE image_id = '" + image_id + "'"
    )
    db_manager.connection.commit()

# get_image_by_id('034b2245-5896-4c66-9e3f-1700c499ba6a')
get_image_by_task_id('aaf0ac2b-ee0a-450e-9647-6fb698849ae9')