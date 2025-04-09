class Course:
    def __init__(self, *args):
        if len(args) == 0:
            pass
        else:
            self.course_id = args[0]
            self.course_name = args[1]
            self.min_students = args[2]
            self.max_students = args[3]
