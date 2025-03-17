import os

import pandas as pd

from excel_writer_charts import ExcelWriterCharts


class ExcelWriter:
    def __init__(self, model_obj, solver):
        self.data_path = os.getcwd() + "\\data_excels\\"
        self.results_file_path = self.data_path + "output.xlsx"
        self.preferences_met_file_path = self.data_path + "preferences_met.xlsx"
        self.model_obj = model_obj
        self.solver = solver
        self.add_charts = ExcelWriterCharts(self.results_file_path, self.preferences_met_file_path)

    def write_results(self):
        results_data = []
        for c in self.model_obj.all_courses:
            for s in self.model_obj.all_students:
                if self.solver.value(self.model_obj.allocation[s][c]):
                    results_data.append([
                        self.model_obj.courses[c].course_name,
                        self.model_obj.courses[c].course_id,
                        self.model_obj.students[s].fullname,
                        self.model_obj.students[s].student_id,
                        self.model_obj.students[s].semester,
                        self.model_obj.students[s].gpa,
                        self.model_obj.students[s].preferences[self.model_obj.courses[c].course_id],
                        self.model_obj.students[s].is_obligated,
                        self.model_obj.students[s].passed_courses_on_sem8,
                        self.model_obj.students[s].courses_needed_remaining,
                        self.model_obj.students[s].choices_remaining,
                        sum(self.solver.value(self.model_obj.allocation[s][c]) for c in self.model_obj.all_courses)
                    ])

        df = pd.DataFrame(results_data, columns = [
            "Course Name",
            "Course ID",
            "Fullname",
            "AEM",
            "Semester",
            "GPA",
            "Preference",
            "Obligated",
            "Passed Courses On Sem8",
            "Courses Needed Remaining",
            "Choices Remaining",
            "Assigned Courses on Student"
        ])

        try:
            print(f"Assignment results are saved to {self.results_file_path}")
            df.to_excel(self.results_file_path, index = False)
            self.add_charts.add_courses_sat_bar_chart()
        except Exception as e:
            print("An error occurred while writing to the assignment results excel file. \n", e)


    def write_sat_preferences(self):
        preferences_met_data = []
        preferences_met_ratios = []
        for s in self.model_obj.all_students:
            assigned_courses = [
                self.model_obj.courses[c].course_id for c in self.model_obj.all_courses
                if self.solver.value(self.model_obj.allocation[s][c])
            ]

            all_assigned_courses = len(assigned_courses)

            assigned_preferences = [self.model_obj.students[s].preferences[self.model_obj.courses[c].course_id]
                                for c in self.model_obj.all_courses if
                                self.solver.value(self.model_obj.allocation[s][c])]

            all_assigned_preferences = len(assigned_preferences)

            preferences_met_ratio = 100

            if all_assigned_courses > 0:
                for course_id, preference in self.model_obj.students[s].preferences.items():
                    if preference <= all_assigned_preferences and course_id not in assigned_courses:
                        preferences_met_ratio -= 100 / all_assigned_courses
            else:
                preferences_met_ratio = 0

            preferences_met_ratios.append(preferences_met_ratio)

            assigned_preferences_string = ", ".join(map(str, assigned_preferences))
            assigned_courses_string = ", ".join(map(str, assigned_courses))

            preferences_met_data.append([
                self.model_obj.students[s].fullname,
                self.model_obj.students[s].student_id,
                self.model_obj.students[s].semester,
                self.model_obj.students[s].gpa,
                assigned_courses_string,
                assigned_preferences_string,
                all_assigned_courses,
                preferences_met_ratio
            ])

        df = pd.DataFrame(preferences_met_data, columns = [
            "Fullname",
            "AEM",
            "Semester",
            "GPA",
            "IDs of Assigned Courses on Student",
            "Assigned Preferences",
            "# of Assigned Courses on Student",
            "Preferences Met Ratio on Student (%)"
        ])

        try:
            df_no_duplicates = df.drop_duplicates()
            print(f"Satisfied preferences (%) results are saved to {self.preferences_met_file_path}")
            df_no_duplicates.to_excel(self.preferences_met_file_path, index = False)
            self.add_charts.add_preferences_met_pie_chart(preferences_met_ratios)
        except Exception as e:
            print("An error occurred while writing to the satisfied preferences results excel file. \n", e)


