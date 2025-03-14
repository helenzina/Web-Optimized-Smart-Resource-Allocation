class Student:
    def __init__(self, student_id, fullname, semester, required_courses, extra_courses):
        self.student_id = student_id
        self.fullname = fullname
        self.gpa = None
        self.SCALING_FACTOR = 100
        self.scaled_gpa = None
        self.semester = semester
        self.preferences = {}
        self.required_courses = required_courses
        self.extra_courses = extra_courses
        self.is_obligated = None

    def set_gpa(self, gpa):
        self.gpa = gpa
        self.scaled_gpa = int(self.gpa * self.SCALING_FACTOR)

    def set_preferences(self, preferences):
        self.preferences = preferences

    def set_is_obligated(self, is_obligated):
        self.is_obligated = is_obligated
