import task
import os

default_directory = './app_files/tasks.json'
open_brace = '{'
closed_brace = '}'

def create_task(title, description, init_date, termination_date, images_directories, files_directories):
    new_task = task.Task(title, description, init_date, termination_date, images_directories, files_directories)

    if not os.path.isfile(default_directory):
        create_json_at_frist_time = open(default_directory, 'w')
        create_json_at_frist_time.write(
"""{
}""")
        create_json_at_frist_time.close()

    task_info =\
f""""task1": {open_brace}
  "title":"{new_task.title}",
  "description":"{new_task.description}",
  "init_date":"{new_task.init_date}",
  "termination_date":"{new_task.termination_date}",
  "images_directories":"{new_task.images_directories}",
  "files_directories":"{new_task.files_directories}"
{closed_brace}
"""

    created_json = open(default_directory, 'r')
    created_json_list = created_json.readlines()
    file = open(default_directory, 'w')

    if created_json_list.__len__() > 9:
            created_json_list.insert(-1, ',')

    created_json_list.insert(-1, task_info)
    print(created_json_list)
    for line in created_json_list:
        file.write(line)

    file.close()
    created_json.close()

    return new_task


