from ortools.sat.python import cp_model

class Model:
    def __init__(self, students, courses, preferences):
        self.model = cp_model.CpModel()
        self.students = students
        self.all_students = range(len(students))
        self.courses = courses
        self.all_courses = range(len(courses))
        self.preferences = preferences
        self.all_preferences = range(len(preferences[0]))
        self.allocation = []

    def set_allocation(self, allocation):
        self.allocation = allocation

    def build_model(self):
        allocation = [[self.model.new_bool_var(f"allocation_{s}_{c}") for c in self.all_courses] for s in self.all_students]

        # each student i must attend exactly xi courses
        for s in self.all_students:
            self.model.add(sum(allocation[s][c] for c in self.all_courses) == self.students[s].required_courses)

        # m <= course_capacity <= M
        for c in self.all_courses:
            # each course has min students m (courses_min_students[c])
            self.model.add(sum(allocation[s][c] for s in self.all_students) >= self.courses[c].min_students)
            # each course has max students M (courses_max_students[c])
            self.model.add(sum(allocation[s][c] for s in self.all_students) <= self.courses[c].max_students)
        # in case of infeasibility, we could create a list of integer variables representing each course's domain values
        # so that we could make the script change them in an "automatic" way until the solution is optimal or at least feasible

        # indices = np.argsort(students)
        # sorted_students = [students[i] for i in indices]
        # sorted_students_gpa_scaled = [students_gpa_scaled[i] for i in indices]
        # sorted_preferences_rank = [preferences_rank[i] for i in indices]
        # for p in all_preferences:
        #     for c in all_courses:
        #         for s in all_students:
        #             if sorted_preferences_rank[s][c] == p+1:
        #                 model.add(allocation[s][c] == 1) # it's already constrained to be at most the max of the course's capacity

        self.set_allocation(allocation)
        return self