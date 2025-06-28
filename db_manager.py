import sqlite3

connection = sqlite3.connect("tasks_db")
task_table_name = 'task_table'

cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS " + task_table_name + "(id INTEGER PRIMARY KEY ASC, title, description, init_date, termination_date, images_directories, files_directories)")

