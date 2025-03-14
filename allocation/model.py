from ortools.sat.python import cp_model

class Model:
    def __init__(self, students, courses):
        self.model = cp_model.CpModel()
        self.students = students
        self.all_students = range(len(students))
        self.courses = courses
        self.all_courses = range(len(courses))
        self.allocation = []

    def set_allocation(self, allocation):
        self.allocation = allocation

    def build_model(self):
        # sorting students based on their gpa in descending order
        self.students = sorted(self.students, key=lambda student: student.gpa, reverse=True)

        allocation = [[self.model.new_bool_var(f"allocation_{s}_{c}") for c in self.all_courses] for s in self.all_students]

        # each student s must attend exactly xs courses
        for s in self.all_students:
            self.model.add(sum(allocation[s][c] for c in self.all_courses) == self.students[s].required_courses)
            # each student s can submit xs courses in total
            self.model.add(sum(allocation[s][c] for c in self.all_courses) <= self.students[s].required_courses + self.students[s].extra_courses)

        # m <= course_capacity <= M
        for c in self.all_courses:
            # each course has min students m
            self.model.add(sum(allocation[s][c] for s in self.all_students) >= self.courses[c].min_students)
            # each course has max students M
            self.model.add(sum(allocation[s][c] for s in self.all_students) <= self.courses[c].max_students)
        # in case of infeasibility, we could create a list of integer variables representing each course's domain values
        # so that we could make the script change them in an "automatic" way until the solution is optimal or at least feasible

        self.set_allocation(allocation)

        self.check_if_solution(self.model)

        return self

    def check_if_solution(self, model):
        """Building model until the value of max students of each course results in a feasible solution"""
        pass
