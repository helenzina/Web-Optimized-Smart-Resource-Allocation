import os
from excel_reader import ExcelReader
from model import Model
from solver import Solver


class App:
    def __init__(
        self,
        filepath,
        students_file_name,
        students_sheet_name,
        courses_file_name,
        courses_sheet_name,
        preferences_file_name,
        preferences_sheet_name,
    ):
        self.students = self.load_students(
            filepath + students_file_name, students_sheet_name
        )
        self.courses = self.load_courses(
            filepath + courses_file_name, courses_sheet_name
        )
        self.preferences = self.load_preferences(
            filepath + preferences_file_name, preferences_sheet_name
        )

    # def load_data(self, file_name, sheet_name, data_category):
    #     excel = ExcelReader(file_name, sheet_name)
    #     data_categories = {
    #         "students": "read_students",
    #         "courses": "read_courses",
    #         "preferences": "read_preferences"
    #     }
    #     data = excel.read_students()
    #     return data

    def load_students(self, file_name, sheet_name):
        students_excel = ExcelReader(file_name, sheet_name)
        students = students_excel.read_students()
        return students

    def load_courses(self, file_name, sheet_name):
        courses_excel = ExcelReader(file_name, sheet_name)
        courses = courses_excel.read_courses()
        return courses

    def load_preferences(self, file_name, sheet_name):
        preferences_excel = ExcelReader(file_name, sheet_name)
        preferences = preferences_excel.read_preferences()
        students_ids_with_preferences, students_is_obligated_preference, students_gpa_with_preferences, students_preferences = preferences

        # parse only the students who submitted their preferences from all the students
        chosen_students = []
        for student in self.students:
            if student.id in students_ids_with_preferences:
                idx = students_ids_with_preferences.index(student.id)

                # creating a dictionary for each student's preferences sorted by the courses
                # (key: value == course: preference_of_student)
                chosen_student_preferences = {course: preference_of_student for preference_of_student, course in enumerate(students_preferences[idx], start=1)}
                chosen_student_preferences = dict(sorted(chosen_student_preferences.items()))

                student.set_preferences(chosen_student_preferences)
                student.set_gpa(students_gpa_with_preferences[idx])
                student.set_is_obligated(students_is_obligated_preference[idx])
                chosen_students.append(student)

        self.students = chosen_students
        return students_preferences

    def run(self):
        model = Model(self.students, self.courses, self.preferences)
        created_model = model.build_model()
        solver = Solver(created_model)
        solver.solve_model()


if __name__ == "__main__":
    app = App(
        os.getcwd() + "\\data_excels\\",
        "students_data.xlsx",
        None,
        "courses.xlsx",
        "Sheet1",
        "students_ordered_selections.xlsx",
        "selections",
    )
    app.run()
