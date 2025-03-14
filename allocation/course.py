class Course:
    def __init__(self, course_id, course_name, min_students, max_students):
        self.course_id = course_id
        self.course_name = course_name
        self.min_students = min_students
        self.max_students = min_students

    def set_max_students(self, max_students):
        self.max_students = max_students