from .excel_reader import ExcelReader
from allocation.ortools_sat.model import Model
from allocation.ortools_sat.solver import Solver


class App:
    def __init__(self, *args):
        if len(args) == 0:
            pass
        else:
            self.sem = args[6]
            self.min_stud = args[7]
            self.max_stud = args[8]
            self.has_error = args[9]
            self.students = self.load_data(args[0], args[1], "students")
            self.courses = self.load_data(args[2], args[3], "courses")
            self.preferences = self.load_data(args[4], args[5], "preferences")
            

    def load_data(self, file_name, sheet_name, data_category):
        from_excel = ExcelReader(
            file_name,
            sheet_name,
            self.sem,
            self.min_stud,
            self.max_stud,
            self.has_error
        )
        load_methods = {
            "students": from_excel.read_students,
            "courses": from_excel.read_courses,
            "preferences": from_excel.read_preferences,
        }
        data = load_methods[data_category]()
        
        self.has_error = from_excel.has_error
        if data_category == "preferences" and not self.has_error:
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
                # (key: value == course_id: preference_of_student)
                chosen_student_preferences = {
                    course_id: preference_of_student
                    for preference_of_student, course_id in enumerate(
                        students_preferences[idx], start=1
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
        results, avg_preferences_ratio, students_preferences_ratio = solver.solve_model()
        return results, avg_preferences_ratio, students_preferences_ratio