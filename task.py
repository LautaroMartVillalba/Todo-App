class Task:
    """Representation of a task.
    """

    def __init__(self, title, description, init_date, termination_date, images_directories, files_directories):
        self.title = title
        self.description = description
        self.init_date = init_date
        self.termination_date = termination_date
        self.images_directories = images_directories
        self.files_directories = files_directories