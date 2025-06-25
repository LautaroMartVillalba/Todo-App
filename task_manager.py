import task
import os
import json

default_directory = './app_files/tasks.json'

def create_task(title, description, init_date, termination_date, images_directories, files_directories):
    new_task = task.Task(title, description, init_date, termination_date, images_directories, files_directories)

    add_task_to_json(new_task)

    return new_task

def add_task_to_json(task):
    # If the file does not exist, it creates.
    if not os.path.isfile(default_directory):
        create_json_at_frist_time = open(default_directory, 'w')
        json.dump({}, create_json_at_frist_time, indent=2)
        create_json_at_frist_time.close()

    with open(default_directory, 'r') as json_read:
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

    with open(default_directory, 'w') as f:
        json.dump(tasks_data, f, indent=2)
        f.close()

