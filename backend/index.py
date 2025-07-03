import os
import threading
from time import time
import webview

#### AQUI CAMBIAS CODIGO LAUTI EH

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


# This is for choosing which enviroment is the project running
def get_entrypoint():

    isdev = os.getenv("DEV")
    if isdev:
        return "http://localhost:5173"

    def exists(path):
        return os.path.exists(os.path.join(os.path.dirname(__file__), path))

    if exists("../gui/index.html"):
        return "../gui/index.html"

    raise Exception("No index.html found")


entry = get_entrypoint()

if __name__ == "__main__":
    window = webview.create_window("Todo-app",
                                   entry,
                                   js_api=Api(),
                                   text_select=True)
    webview.start()






