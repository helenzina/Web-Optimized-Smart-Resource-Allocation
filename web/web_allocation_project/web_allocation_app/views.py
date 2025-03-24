from django.shortcuts import render, HttpResponse
import pandas as pd
from allocation import app


# Create your views here.
def home(request):
    global app_obj
    app_obj = app.App()

    if request.method == "POST":
        if "files-submit" in request.POST:
            students_data = request.FILES.get("students")
            courses_data = request.FILES.get("courses")
            students_selections_data = request.FILES.get("students_selections")
            sem = request.POST.get("sem")

            try:
                students_sheet_names = pd.ExcelFile(students_data).sheet_names
                courses_sheet_name = pd.ExcelFile(courses_data).sheet_names[0]
                students_selections_sheet_name = pd.ExcelFile(
                    students_selections_data
                ).sheet_names[0]
            except Exception as e:
                return HttpResponse(
                    f"Error reading an excel file: {str(e)}", status=404
                )

            app_obj = app.App(
                students_data,
                students_sheet_names,
                courses_data,
                courses_sheet_name,
                students_selections_data,
                students_selections_sheet_name,
                int(sem),
                0,
                0,
            )

            # for showing data table
            columns = ["Fullname", "AEM", "GPA", "Selections"]
            data = {c: [] for c in columns}

            for student in app_obj.students:
                data["Fullname"].append(student.fullname)
                data["AEM"].append(student.student_id)
                data["GPA"].append(student.gpa)

                temp = {p: c for c, p in student.preferences.items()}
                temp = dict(sorted(temp.items()))

                course_choices = [c for p, c in temp.items()]

                data["Selections"].append(", ".join(map(str, course_choices)))

            selected_students = pd.DataFrame(data)

            context = {"selected_students": selected_students, "has_students": not selected_students.empty}
            
        elif "allocation-submit" in request.POST:
            min_stud = request.POST.get("min_stud")
            max_stud = request.POST.get("max_stud")
            
            if min_stud not in [0, None] and max_stud not in [0, None]:
                for c in range(len(app_obj.courses)):
                    app_obj.courses[c].min_stud = min_stud
                    app_obj.courses[c].max_stud = max_stud

                app_obj.run()

            context["min_stud"] = int(min_stud)
            context["max_stud"] = int(max_stud)

        return render(request, "home.html", context)

    return render(request, "home.html") 