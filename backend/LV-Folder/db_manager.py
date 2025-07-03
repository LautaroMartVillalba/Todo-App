import sqlite3

connection = sqlite3.connect("tasks_db")
task_table_name = 'task_table'
images_table_name = 'images_table'
files_table_name = 'files_table'

cursor = connection.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS " + task_table_name + "(task_id TEXT,"
                                                      " title,"
                                                      " description,"
                                                      " init_date,"
                                                      " termination_date)")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS " + images_table_name + "(image_id TEXT PRIMARY KEY,"
                                                        " directory TEXT,"
                                                        " task_id INTEGER,"
                                                        "FOREIGN KEY (task_id) REFERENCES " + task_table_name + "(task_id))")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS " + files_table_name + "(file_id TEXT PRIMARY KEY,"
                                                       " directory TEXT,"
                                                        " task_id INTEGER,"
                                                        "FOREIGN KEY (task_id) REFERENCES " + task_table_name + "(task_id))")

