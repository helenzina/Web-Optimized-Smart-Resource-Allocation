from ortools.sat.python import cp_model

from excel_writer import ExcelWriter


class Solver:
    def __init__(self, model_obj):
        self.model_obj = model_obj

    def solve_model(self):
        # maximize student allocation based on their gpa
        self.model_obj.model.maximize(
            sum(self.model_obj.students[s].scaled_gpa * self.model_obj.allocation[s][c]
                for s in self.model_obj.all_students
                for c in self.model_obj.all_courses)
        )

        solver = cp_model.CpSolver()
        # solver.parameters.log_search_progress = True
        status = solver.solve(self.model_obj.model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            maximized_gpa_allocation = [[solver.value(self.model_obj.allocation[s][c]) for c in self.model_obj.all_courses] for s in self.model_obj.all_students]

            for s in self.model_obj.all_students:
                for c in self.model_obj.all_courses:
                    self.model_obj.model.add_hint(self.model_obj.allocation[s][c], maximized_gpa_allocation[s][c])


            # minimize student allocation based on their preferences
            self.model_obj.model.minimize(
                sum(self.model_obj.students[s].preferences[self.model_obj.courses[c].course_id] * self.model_obj.allocation[s][c]
                    for s in self.model_obj.all_students
                    for c in self.model_obj.all_courses)
            )

            solver = cp_model.CpSolver()
            # solver.parameters.log_search_progress = True
            status = solver.solve(self.model_obj.model)

            if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
                to_excel = ExcelWriter(self.model_obj, solver)
                to_excel.write_results()

                # for c in self.model_obj.all_courses:
                #     print()
                #     print(f"{self.model_obj.courses[c].name} (ID = {self.model_obj.courses[c].id}):")
                #     print("--------------------------------")
                #     print(f"{"Fullname":<25} {"AEM":<10} {"Semester":<17} {"GPA":<10} {"Preference":<15} {"Obligated":<15} \n")
                #     for s in self.model_obj.all_students:
                #         if solver.value(self.model_obj.allocation[s][c]):
                #             print(
                #                 f"{self.model_obj.students[s].fullname:<25}"
                #                 f"{self.model_obj.students[s].id:<15}"
                #                 f"{self.model_obj.students[s].semester:<15}"
                #                 f"{self.model_obj.students[s].gpa:<15}"
                #                 f"{self.model_obj.students[s].preferences[self.model_obj.courses[c].id]:<15}"
                #                 f"{self.model_obj.students[s].is_obligated:<15}"
                #             )
                # print()

            else:
                print("Infeasible solution for minimizer.")

        else:
            print("Infeasible solution for maximizer.")
