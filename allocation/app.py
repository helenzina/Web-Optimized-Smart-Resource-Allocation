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
        self.students = self.load_data(
            filepath + students_file_name, students_sheet_name, "students"
        )
        self.courses = self.load_data(
            filepath + courses_file_name, courses_sheet_name, "courses"
        )
        self.preferences = self.load_data(
            filepath + preferences_file_name, preferences_sheet_name, "preferences"
        )

    def load_data(self, file_name, sheet_name, data_category):
        from_excel = ExcelReader(file_name, sheet_name)
        load_methods = {
            "students": from_excel.read_students,
            "courses": from_excel.read_courses,
            "preferences": from_excel.read_preferences,
        }
        data = load_methods[data_category]()
        if data_category == "preferences":
            data = self.load_additional_data_to_students(data)

        return data

    def load_additional_data_to_students(self, preferences):
        (
            students_ids_with_preferences,
            students_is_obligated_preference,
            students_gpa_with_preferences,
            students_preferences,
        ) = preferences

        # parse only the students who submitted their preferences from all the students
        chosen_students = []
        for student in self.students:
            if student.student_id in students_ids_with_preferences:
                idx = students_ids_with_preferences.index(student.student_id)

                # creating a dictionary for each student's preferences sorted by the courses
                # (key: value == course: preference_of_student)
                chosen_student_preferences = {
                    course: preference_of_student
                    for preference_of_student, course in enumerate(
                        students_preferences[idx], start = 1
                    )
                }
                chosen_student_preferences = dict(
                    sorted(chosen_student_preferences.items())
                )

                student.set_preferences(chosen_student_preferences)
                student.set_gpa(students_gpa_with_preferences[idx])
                student.set_is_obligated(students_is_obligated_preference[idx])
                chosen_students.append(student)

        self.students = chosen_students
        return students_preferences

    def run(self):
        model = Model(self.students, self.courses)
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
