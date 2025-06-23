import task
import os

default_directory = './app_files'
open_brace = '{'
closed_brace = '}'

def create_task(title, description, init_date, termination_date, images_directories, files_directories):
    new_task = task.Task(title, description, init_date, termination_date, images_directories, files_directories)

    with open(default_directory+'/pito.json', 'a') as file:
        file.write(
f"""{open_brace}
"title":"{title}",
"description":"{description}",
"init_date":"{init_date}",
"termination_date":"{termination_date}",
"images_directories":"{images_directories}",
"files_directories":"{files_directories}"
{closed_brace}""")

        file.close()

    return new_task


