import pandas as pd
from course import Course
from student import Student


class ExcelReader:
    def __init__(self, file_name, sheet_name):
        self.file_name = file_name
        self.sheet_name = sheet_name

    def read_students(self):
        try:
            df = pd.read_excel(self.file_name, self.sheet_name)

            data_sheets = []
            for sheet in df.keys():
                data_sheets.append(pd.read_excel(self.file_name, sheet))
            
            all_data_sheets = range(len(data_sheets))

            # getting all the students data from every sheet in students excel and removing nan & duplicate values
            students_ids = self.multiple_sheets_data_reader(data_sheets, all_data_sheets, "ID", int)
            students_names = self.multiple_sheets_data_reader(data_sheets, all_data_sheets, ["Name", "Surname"], str)
            students_semesters = self.multiple_sheets_data_reader(data_sheets, all_data_sheets, "Sem", int)
            # how many obliged courses are remaining to select
            extra_courses_per_student = self.multiple_sheets_data_reader(data_sheets, all_data_sheets, "ObligRemain", int)
            # how many obliged courses they can select
            required_courses_per_student = self.multiple_sheets_data_reader(data_sheets, all_data_sheets, "ChoiceRemain", int)

            students = []
            for index, name in enumerate(students_names):
                students.append(
                    Student(
                        id = students_ids[index], 
                        fullname = students_names[index],
                        semester = students_semesters[index],
                        required_courses = required_courses_per_student[index],
                        extra_courses = extra_courses_per_student[index]
                    )
                )
            return students

        except Exception as e:
            print("An error occurred with the students excel file. \n", e)

    def multiple_sheets_data_reader(self, data_sheets, all_data_sheets, sheet_names, type):
        if isinstance(sheet_names, list):
            students_data = [list(data_sheets[s][sheet_names[0]].dropna().astype(type) + " " + data_sheets[s][sheet_names[1]].dropna().astype(type)) for s in all_data_sheets]
        else:
            students_data = [list(data_sheets[s][sheet_names].dropna().astype(type)) for s in all_data_sheets]
        flattened_students_data = sum(students_data, [])
        return flattened_students_data


    def read_courses(self):
        try:
            df = pd.read_excel(self.file_name, self.sheet_name)
            courses_names = list(df.course_name)
            
            courses = []
            for index, name in enumerate(courses_names):
                courses.append(
                    Course(id = index + 1, name = name, min_students = 7, max_students = 35)
                )
            return courses

        except Exception as e:
            print("An error occurred with the courses excel file. \n", e)


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

