import uuid

from backend.database import db_manager

def save_images_directories_in_db(task_id, image_directory):
    images_direct = []

    if isinstance(image_directory, list):
        for element in image_directory:
            images_direct.append(element)
    else:
        images_direct.append(image_directory)

    for each in images_direct:
        with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
            unique_id = uuid.uuid4().__str__()
            cursor.execute(
                f"""INSERT INTO {db_manager.images_table_name} (image_id, directory, task_id) VALUES(?,?,?)""", (unique_id, each, task_id)
            )


def get_image_by_id(image_id):
    with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
        query = cursor.execute(
            f"select * from {db_manager.images_table_name} where image_id = '" + image_id + "'"
        ).fetchone()

    image_dict = {
        "image_id": query[0],
        "directory": query[1]
    }

    return image_dict

def get_image_by_task_id(task_id):
    with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
        images_list = cursor.execute(
            f"select * from {db_manager.images_table_name} where task_id = '" + task_id + "'"
        ).fetchall()

    images_dict = {}

    for each in images_list:
        images_dict[each[0]] = {
            "directory": each[1]
        }

    return images_dict

def update_images_direct_info_by_id(image_id, directory):
    with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
        cursor.execute(
            f"UPDATE {db_manager.images_table_name} SET directory = ? WHERE '" + image_id + "'", directory
        )

def delete_image_by_id(image_id):
    with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
        cursor.execute(
           f"DELETE FROM {db_manager.images_table_name} WHERE image_id = '" + image_id + "'"
        )
