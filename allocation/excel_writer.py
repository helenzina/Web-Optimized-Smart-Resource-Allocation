import os

import pandas as pd


class ExcelWriter:
    def __init__(self, model_obj, solver):
        self.file_path = os.getcwd() + "\\data_excels\\" + "output.xlsx"
        self.model_obj = model_obj
        self.solver = solver

    def write_results(self):
        data = []
        for c in self.model_obj.all_courses:
            for s in self.model_obj.all_students:
                if self.solver.value(self.model_obj.allocation[s][c]):
                    data.append([
                        self.model_obj.courses[c].name,
                        self.model_obj.courses[c].id,
                        self.model_obj.students[s].fullname,
                        self.model_obj.students[s].id,
                        self.model_obj.students[s].semester,
                        self.model_obj.students[s].gpa,
                        self.model_obj.students[s].preferences[self.model_obj.courses[c].id],
                        self.model_obj.students[s].is_obligated
                    ])

        df = pd.DataFrame(data, columns=[
            "Course Name", "Course ID", "Fullname", "AEM", "Semester", "GPA", "Preference", "Obligated"
        ])

        try:
            print(f"Results saved to {self.file_path}")
            df.to_excel(self.file_path, index = False)
        except Exception as e:
            print("An error occurred writing to the excel file. \n", e)

