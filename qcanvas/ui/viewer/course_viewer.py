import qcanvas.db as db

class CourseViewer:
    course: db.Course | None = None

    def __init__(self):
        pass

    def load_course(self, course : db.Course):
        self.course = course


