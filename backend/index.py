import os
import sys
from time import time
import webview
from backend.managers import task_manager

class Api:
    def fullscreen(self):
        webview.windows[0].toggle_fullscreen()

    def save_content(self, content):
        filename = webview.windows[0].create_file_dialog(webview.SAVE_DIALOG)
        if not filename:
            return

        with open(filename, "w") as f:
            f.write(content)

    def ls(self):
        return os.listdir("")

    # ///////////////////////////////////task_manager methods/////////////////////////////////////////////////
    def create_task(self, title, description, init_date, termination_date, images_directories, files_directories):
        try:
            method = task_manager.create_task(title, description, init_date, termination_date, images_directories, files_directories)
            return method
        except Exception as e:
            raise RuntimeError('An error has occur.') from e

    def get_all_tasks(self):
        try:
            method = task_manager.get_all_tasks()
            return method
        except Exception as e:
            raise RuntimeError('An error has occur.') from e

    def get_task_by_id(self, task_id):
        try:
            method = task_manager.get_task_by_id(task_id)
            return method
        except Exception as e:
            raise RuntimeError('An error has occur.') from e

    def update_task_info_by_id(self,
                               task_id=None,
                               description=None,
                               init_date=None,
                               termination_date=None,
                               image_id =None,
                               new_image_directory=None,
                               file_id =None,
                               new_file_directory=None):
        try:
            method = task_manager.update_task_info_by_id(
                                                        task_id=task_id,
                                                        description=description,
                                                        init_date=init_date,
                                                        termination_date=termination_date,
                                                        image_id=image_id,
                                                        new_image_directory=new_image_directory,
                                                        file_id=file_id,
                                                        new_file_directory=new_file_directory)
            return method
        except Exception as e:
            raise RuntimeError('An error has occur.') from e

    def delete_task_images_and_files_by_task_id(self, task_id):
        try:
            task_manager.delete_task_images_and_files_by_task_id(task_id)
        except Exception as e:
            raise RuntimeError('An error has occur.') from e


# This is for choosing which enviroment is the project running
def get_entrypoint():

    isdev = os.getenv("DEV")
    if isdev:
        return "http://localhost:5173"
    
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))

    paths = [
        os.path.join(base_path, "dist", "front", "index.html"),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../dist/front/index.html")),
    ]

    for path in paths:
        if os.path.exists(path):
            return path 

    raise Exception("No index.html found")


entry = get_entrypoint()

if __name__ == "__main__":
    window = webview.create_window("Todo-app",
                                   entry,
                                   js_api=Api(),
                                   text_select=True)
    webview.start()






