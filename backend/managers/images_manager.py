"""
Module: Image Directory Manager

This module provides functions to handle operations related to image directories
associated with tasks. It includes functionality to persist image paths into the
database.

Functions:
    - save_images_directories_in_db
    - get_image_by_id
    - get_image_by_task_id
    - update_images_direct_info_by_id
    - delete_image_by_id
"""

import uuid
import os
import shutil
from pathlib import Path
from backend.database import db_manager

user_images_directory = Path(Path().resolve().parent / 'user_folder' / 'images')

def save_images_directories_in_db(task_id, image_directory):
    """
    Saves one or multiple image directory paths to the database and associates
    them with the given task ID.

    Args:
        task_id (str): UUID of the task to which the images belong.
        image_directory (str or list[str]): A single directory path or a list of
                                            directory paths to be stored.
    """
    images_direct = []

    if isinstance(image_directory, list):
        for element in image_directory:
            images_direct.append(element.__str__())
    else:
        images_direct.append(image_directory.__str__())

    if not os.path.exists(user_images_directory / f'{task_id}'):
        os.makedirs(user_images_directory / f'{task_id}')

    for each in images_direct:
        with db_manager.call_new_cursor() as (cursor, connection):
            unique_id = uuid.uuid4().__str__()

            file_name = unique_id + '_' + str(Path(each).name)

            shutil.copy2(each, user_images_directory / f'{task_id}' / file_name)
            cursor.execute(
                f"""INSERT INTO {db_manager.images_table_name} (image_id, directory, task_id) VALUES(?,?,?)""", (unique_id, each, task_id)
            )


def get_image_by_id(image_id):
    """
    Retrieves a single image record from the database based on its unique image ID.

    Args:
        image_id (str): UUID of the image record.

    Returns:
        dict: A dictionary containing the image ID and its corresponding directory.
              Format: {"image_id": ..., "directory": ...}
    """
    with db_manager.call_new_cursor() as (cursor, connection):
        query = cursor.execute(
            f"select * from {db_manager.images_table_name} where image_id = '" + image_id + "'"
        ).fetchone()

    image_dict = {
        "image_id": query[0],
        "directory": query[1]
    }

    return image_dict

def get_image_by_task_id(task_id):
    """
    Retrieves all image records associated with a specific task ID.

    Args:
        task_id (str): UUID of the task for which images are to be retrieved.

    Returns:
        dict: A dictionary where each key is the image ID and the value is
              a dictionary with the directory path. Format:
              {
                  "image_id_1": { "directory": ... },
                  "image_id_2": { "directory": ... },
                  ...
              }
    """
    with db_manager.call_new_cursor() as (cursor, connection):
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
    """
    Updates the directory path of an image record identified by its image ID.

    Args:
        image_id (str): UUID of the image record to be updated.
        directory (str): New directory path to replace the old one.
    """
    with db_manager.call_new_cursor() as (cursor, connection):
        cursor.execute(
            f"UPDATE {db_manager.images_table_name} SET directory = ? WHERE image_id ='" + image_id + "'", directory
        )

def delete_image_by_id(image_id):
    """
    Deletes an image record from the database by its image ID.

    Args:
        image_id (str): UUID of the image record to delete.
    """
    with db_manager.call_new_cursor() as (cursor, connection):
        cursor.execute(
           f"DELETE FROM {db_manager.images_table_name} WHERE image_id = '" + image_id + "'"
        )