import pandas as pd
from allocation.student_course.course import Course
from allocation.student_course.student import Student


class ExcelReader:
    def __init__(self, file_name, sheet_name, sem, min_stud, max_stud, has_error):
        self.file_name = file_name
        self.sheet_name = sheet_name
        self.sem = sem
        self.min_stud = min_stud
        self.max_stud = max_stud
        self.has_error = has_error

    def read_students(self):
        try:
            df_sheets = pd.read_excel(self.file_name, self.sheet_name)

            # reformatting the dictionary of the students excel to drop rows where id is nan for each sheet
            df_sheets = {sheet: df.dropna(subset=["ID"]) for sheet, df in df_sheets.items()}

            data_sheets = list(df_sheets.values())
            all_data_sheets = range(len(data_sheets))

            # getting all the students data from every sheet in students excel and removing nan values
            students_ids = self.multiple_sheets_data_reader(
                data_sheets, all_data_sheets, "ID", int
            )
            all_students_ids = range(len(students_ids))

            students_names = self.multiple_sheets_data_reader(
                data_sheets, all_data_sheets, ["Name", "Surname"], str
            )
            students_semesters = self.multiple_sheets_data_reader(
                data_sheets, all_data_sheets, "Sem", int
            )

            # how many obligatory courses the student already passed on this semester (or not)
            passed_courses_on_this_sem = [
                list(data_sheets[s][f"Choices{self.sem}"].fillna(0).astype(int))
                for s in all_data_sheets
            ]
            passed_courses_on_this_sem = sum(passed_courses_on_this_sem, [])

            # how many obligatory courses the student can take
            choices_remaining = self.multiple_sheets_data_reader(
                data_sheets, all_data_sheets, "ChoiceRemain", int
            )
            choices_remaining = [max(0, t) for t in choices_remaining]

            students = [
                Student(
                        students_ids[i],
                        students_names[i],
                        students_semesters[i],
                        6,
                        passed_courses_on_this_sem[i],
                        choices_remaining[i]
                    )
                for i in all_students_ids
            ]
            return students

        except Exception as e:
            print("An error occurred with the students excel file. \n", e)
            self.has_error = True

    def multiple_sheets_data_reader(
        self, data_sheets, all_data_sheets, sheet_names, data_type
    ):
        if isinstance(sheet_names, list):
            students_data = [
                list(
                    data_sheets[s][sheet_names[0]].dropna().astype(data_type)
                    + " "
                    + data_sheets[s][sheet_names[1]].dropna().astype(data_type)
                )
                for s in all_data_sheets
            ]
        else:
            students_data = [
                list(data_sheets[s][sheet_names].dropna().astype(data_type))
                for s in all_data_sheets
            ]
        flattened_students_data = sum(students_data, [])
        return flattened_students_data

    def read_courses(self):
        try:
            df = pd.read_excel(self.file_name, self.sheet_name)
            courses_ids = list(df.courseID)
            courses_names = list(df.course_name)
            all_courses_ids = range(len(courses_ids))

            courses = [
                Course(
                    courses_ids[i],
                    courses_names[i],
                    self.min_stud,
                    self.max_stud
                )
                for i in all_courses_ids
            ]

            return courses

        except Exception as e:
            print("An error occurred with the courses excel file. \n", e)
            self.has_error = True

    def read_preferences(self):
        try:
            df = pd.read_excel(self.file_name, self.sheet_name)
            students_ids = list(df.ID)
            students_is_obligated = list(df.Oblig)
            students_gpa = list(df.Mean_grade)
            students_choices = df.filter(like="choice").values.tolist()

            return [students_ids, students_is_obligated, students_gpa, students_choices]

        except Exception as e:
            print("An error occurred with the preferences excel file. \n", e)
            self.has_error = True