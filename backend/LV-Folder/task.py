class Task:
    """Representation of a task.
    """

    def __init__(self, title, description, init_date, termination_date, images_directories=None, files_directories=None):
        self.title = title
        self.description = description
        self.init_date = init_date
        self.termination_date = termination_date
        # if images_directories is None:
        self.images_directories = []
        # else:
        self.images_directories = images_directories
        # if files_directories is None:
        self.files_directories = []
        # else:
        self.files_directories = files_directories
