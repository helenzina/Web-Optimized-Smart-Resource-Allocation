import sys

from ortools.sat.python import cp_model
from allocation.excel_writer.excel_writer import ExcelWriter


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

        # self.solver.parameters.log_search_progress = True # for solver statistics
        self.status = self.solver.solve(self.model_obj.model)

        if self.status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            to_excel = ExcelWriter(self.model_obj, self.solver)
            results = to_excel.save_results()
            to_excel.save_sat_preferences()
            return self.model_obj, self.solver, results
        else:
            return None, None, None

