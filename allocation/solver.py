import sys

from ortools.sat.python import cp_model
from excel_writer import ExcelWriter


class Solver:
    def __init__(self, model_obj):
        self.model_obj = model_obj
        self.solver = cp_model.CpSolver()
        self.status = None

    def solve_model(self):
        # maximize student allocation based on their gpa and
        # minimize student allocation based on their preferences

        self.model_obj.model.maximize(
            sum(
                (self.model_obj.students[s].scaled_gpa -
                 self.model_obj.students[s].preferences[self.model_obj.courses[c].course_id]) *
                self.model_obj.allocation[s][c]
                for s in self.model_obj.all_students
                for c in self.model_obj.all_courses
            )
        )

        # self.solver.parameters.log_search_progress = True
        self.status = self.solver.solve(self.model_obj.model)

        if self.status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            to_excel = ExcelWriter(self.model_obj, self.solver)
            to_excel.write_results()
            return

        print("Infeasible solution.")
        self.fix_max_students_in_course()


    def fix_max_students_in_course(self, course_idx = None):
        if course_idx is not None:
            self.model_obj.courses[course_idx].max_students -= 1
            print(f"Reducing max students for course {self.model_obj.courses[course_idx].course_name}"
                    f" to {self.model_obj.courses[course_idx].max_students}.")
        else:
            for c in self.model_obj.all_courses:
                self.model_obj.courses[c].max_students -= 1
            print("Reducing max students for all courses by 1.")

        for c in self.model_obj.all_courses:
            print(f"Current value of max number of students in {self.model_obj.courses[c].course_name}"
                    f" = {self.model_obj.courses[c].max_students}")

            if self.model_obj.courses[c].max_students < self.model_obj.courses[c].min_students:
                print(f"Infeasible solution - max number of students in course"
                        f" {self.model_obj.courses[c].course_name} "
                        f"is below its minimum number ({self.model_obj.courses[c].min_students}).")
                sys.exit(0)

        # solve the model again with the new values of max number of students
        self.model_obj = self.model_obj.build_model()

        self.solve_model()

        if self.status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            print("Found feasible solution after reducing max students.")
            to_excel = ExcelWriter(self.model_obj, self.solver)
            to_excel.write_results()
            sys.exit(0)


    # def solve_model(self):
    #     # maximize student allocation based on their gpa
    #     self.model_obj.model.maximize(
    #         sum(self.model_obj.students[s].scaled_gpa * self.model_obj.allocation[s][c]
    #             for s in self.model_obj.all_students
    #             for c in self.model_obj.all_courses)
    #     )
    #
    #     # self.solver.parameters.log_search_progress = True
    #     self.status = self.solver.solve(self.model_obj.model)
    #
    #     if self.status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
    #         maximized_gpa_allocation = [
    #             [self.solver.value(self.model_obj.allocation[s][c]) for c in self.model_obj.all_courses] for s in
    #             self.model_obj.all_students]
    #
    #         for s in self.model_obj.all_students:
    #             for c in self.model_obj.all_courses:
    #                 self.model_obj.model.add_hint(self.model_obj.allocation[s][c], maximized_gpa_allocation[s][c])
    #
    #         # minimize student allocation based on their preferences
    #         self.model_obj.model.minimize(
    #             sum(self.model_obj.students[s].preferences[self.model_obj.courses[c].course_id] *
    #                 self.model_obj.allocation[s][c]
    #                 for s in self.model_obj.all_students
    #                 for c in self.model_obj.all_courses)
    #         )
    #
    #         # self.solver.parameters.log_search_progress = True
    #         self.status = self.solver.solve(self.model_obj.model)
    #
    #         if self.status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
    #             to_excel = ExcelWriter(self.model_obj, self.solver)
    #             to_excel.write_results()
    #             return
    #
    #     print("Infeasible solution.")
    #     self.fix_max_students_in_course()


    #
    # def check_solution_infeasibility(self):
    #     print("Reason of infeasibility:")
    #
    #     if self.model_obj.allocation is None:
    #         print("The allocation is empty.")
    #         return
    #
    #     # check if each course has at least m students
    #     for c in self.model_obj.all_courses:
    #         num_students_in_course = sum(
    #             self.solver.value(self.model_obj.allocation[s][c])
    #             for s in self.model_obj.all_students
    #         )
    #         if num_students_in_course < self.model_obj.courses[c].min_students:
    #             print(f"Course {self.model_obj.courses[c].course_name}"
    #                   f"has {num_students_in_course}"
    #                   f"instead of {self.model_obj.courses[c].min_students}.")
    #             self.fix_max_students_in_course(c)
    #             return
    #
    #     # check if each student has exactly xs courses
    #     for s in self.model_obj.all_students:
    #         num_courses_for_student = sum(
    #             self.solver.value(self.model_obj.allocation[s][c])
    #             for c in self.model_obj.all_courses
    #         )
    #         if num_courses_for_student != self.model_obj.students[s].required_courses:
    #             print(f"Student {self.model_obj.students[s].fullname} {self.model_obj.students[s].student_id}"
    #                   f"has {num_courses_for_student}"
    #                   f"instead of {self.model_obj.students[s].required_courses}.")
    #             self.fix_max_students_in_course()
    #             return

