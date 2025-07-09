from backend.database import db_manager
import uuid

def save_files_directories_in_db(task_id, image_directory):
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
    # connection_to_db.close()


def get_file_by_id(file_id):
    with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
        query = cursor.execute(
            f"select * from {db_manager.files_table_name} where file_id = '" + file_id + "'"
        ).fetchone()

    file_dict = {
        "image_id": query[0],
        "directory": query[1]
    }

    # connection_to_db.close()
    return file_dict

def get_file_by_task_id(task_id):
    with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
        images_list = cursor.execute(
            f"select * from {db_manager.files_table_name} where task_id = '" + task_id + "'"
        ).fetchall()

    files_dict = {}

    for each in images_list:
        files_dict[each[0]] = {
            "directory": each[1]
        }

    # connection_to_db.close()
    return files_dict

def update_files_direct_info_by_id(file_id, directory):
    with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
        cursor.execute(
            f"UPDATE {db_manager.files_table_name} SET directory = ? WHERE file_id = ?", (directory, file_id)
        )
    # connection_to_db.close()


def delete_file_by_id(file_id):
    with db_manager.call_new_cursor(db_manager.DB_PATH) as (cursor, connection):
        cursor.execute(
            f"DELETE FROM {db_manager.files_table_name} WHERE file_id = '" + file_id + "'"
        )
    # connection_to_db.close()
