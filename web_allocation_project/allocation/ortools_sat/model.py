from ortools.sat.python import cp_model

class Model:
    def __init__(self, students, courses):
        self.model = cp_model.CpModel()
        self.students = students
        self.all_students = range(len(students))
        self.courses = courses
        self.all_courses = range(len(courses))
        self.allocation = []


    def build_model(self):
        # sorting students based on their gpa in descending order
        self.students = sorted(self.students, key=lambda student: student.gpa, reverse=True)

        allocation = [[self.model.new_bool_var(f"allocation_{s}_{c}") for c in self.all_courses] for s in self.all_students]

        # each student s must attend exactly xs courses
        for s in self.all_students:
            # assigning xs courses on student while xs is an eligible number of courses the student can be assigned on
            if self.students[s].courses_needed_remaining <= self.students[s].choices_remaining:
                self.model.add(
                    sum(allocation[s][c] for c in self.all_courses) == self.students[s].courses_needed_remaining
                )
            else:
                self.model.add(
                    sum(allocation[s][c] for c in self.all_courses) == self.students[s].choices_remaining
                )


        # m <= course_capacity <= M
        for c in self.all_courses:
            # each course has min students m
            self.model.add(sum(allocation[s][c] for s in self.all_students) >= self.courses[c].min_students)
            # each course has max students M
            self.model.add(sum(allocation[s][c] for s in self.all_students) <= self.courses[c].max_students)


        self.allocation = allocation

        return self

