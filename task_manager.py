import task
import os

default_directory = './app_files/tasks.json'
open_brace = '{'
closed_brace = '}'

def create_task(title, description, init_date, termination_date, images_directories, files_directories):
    new_task = task.Task(title, description, init_date, termination_date, images_directories, files_directories)

    add_task_to_json(new_task)

    return new_task

def add_task_to_json(task):
    if not os.path.isfile(default_directory):
        create_json_at_frist_time = open(default_directory, 'w')
        create_json_at_frist_time.write(
"""{
}""")
        create_json_at_frist_time.close()

    task_in_json_format =\
f""""task1": {open_brace}
  "title":"{task.title}",
  "description":"{task.description}",
  "init_date":"{task.init_date}",
  "termination_date":"{task.termination_date}",
  "images_directories":"{task.images_directories}",
  "files_directories":"{task.files_directories}"
{closed_brace}
"""

    created_file_read = open(default_directory, 'r')
    line_list_in_created_file = created_file_read.readlines()
    created_file_write = open(default_directory, 'w')

    if line_list_in_created_file.__len__() > 9:
        penultimate_line_in_fine = line_list_in_created_file[line_list_in_created_file.__len__()-1]
        line_list_in_created_file.remove(penultimate_line_in_fine)
        line_list_in_created_file.insert(-1, penultimate_line_in_fine+',\n')

    line_list_in_created_file.insert(-1, task_in_json_format)
    for line in line_list_in_created_file:
        created_file_write.write(line)

    created_file_write.close()
    created_file_read.close()

