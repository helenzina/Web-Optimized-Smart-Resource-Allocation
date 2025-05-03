import json
import os
import threading
import time
import pandas as pd
from django.http import FileResponse
from django.shortcuts import render, HttpResponse
from allocation.app.app import App
from allocation.student_course.course import Course
from allocation.student_course.student import Student


# Create your views here.
def home(request):
    request.session.set_expiry(0) 
    # session cookie will expire when the user’s web browser is closed

    if request.method == "POST" and "files-submit" in request.POST:
        request.session.flush()

        students_data = request.FILES.get("students", None)
        courses_data = request.FILES.get("courses", None)
        students_selections_data = request.FILES.get("students_selections", None)
        sem = request.POST.get("sem", None)

        students_ext = os.path.splitext(students_data.name)[-1].lower()
        courses_ext = os.path.splitext(courses_data.name)[-1].lower()
        students_selections_ext = os.path.splitext(students_selections_data.name)[
            -1
        ].lower()

        extensions = [students_ext, courses_ext, students_selections_ext]
        for e in extensions:
            if e not in [".xlsx", ".xls"]:
                return render(
                    request,
                    "home.html",
                    {
                        "error_message": "Each file should have an excel's file extension (.xlsx or .xls)."
                    },
                )

        try:
            students_sheet_names = pd.ExcelFile(students_data).sheet_names
            courses_sheet_name = pd.ExcelFile(courses_data).sheet_names[0]
            students_selections_sheet_name = pd.ExcelFile(
                students_selections_data
            ).sheet_names[0]
        except Exception as e:
            return HttpResponse(f"Error reading an excel file: {str(e)}", status=404)

        app_obj = App(
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

        selected_students = json_serialization(request, app_obj)

        context = {
            "selected_students": selected_students,
            "has_students": request.session.get("has_students", False),
        }

        return render(request, "allocation.html", context)

    if request.method == "POST" and (
        "allocation-submit" in request.POST or "allocation-download" in request.POST
    ):
        return allocation(request)
    else:
        return render(request, "home.html")


def json_serialization(request, app_obj):
    """This method converts class objects to json files and
    returns the selected students."""

    # for selected students table display
    columns = ["Ονοματεπώνυμο", "AEM", "ΜΟ", "Επιλογές"]
    data = {c: [] for c in columns}

    for student in app_obj.students:
        data["Ονοματεπώνυμο"].append(student.fullname)
        data["AEM"].append(student.student_id)
        data["ΜΟ"].append(student.gpa)

        temp = {p: c for c, p in student.preferences.items()}
        temp = dict(sorted(temp.items()))

        course_choices = [c for p, c in temp.items()]

        data["Επιλογές"].append(", ".join(map(str, course_choices)))

    selected_students = pd.DataFrame(data)

    # converting class objects to json in session
    # to use in the allocation view (serialization)
    try:
        students_json = json.dumps(
            app_obj.students, default=lambda x: x.__dict__, indent=4
        )
        courses_json = json.dumps(
            app_obj.courses, default=lambda x: x.__dict__, indent=4
        )
        selected_students_json = selected_students.to_json(orient="records")
    except Exception as e:
        return HttpResponse(
            f"Error while serializing the json files: {str(e)}", status=404
        )

    request.session["students"] = students_json
    request.session["courses"] = courses_json
    request.session["selected_students"] = selected_students_json
    request.session["has_students"] = not selected_students.empty

    return selected_students


def get_context_from_session(request):
    selected_students = json.loads(request.session.get("selected_students", "[]"))
    allocated_students = json.loads(request.session.get("allocated_students", "[]"))
    non_100_allocated_students = json.loads(
        request.session.get("non_100_allocated_students", "[]")
    )
    return {
        "selected_students": selected_students,
        "has_students": request.session.get("has_students", False),
        "allocated_students": allocated_students,
        "has_allocated_students": True if allocated_students else False,
        "avg_preferences_ratio": request.session.get("avg_preferences_ratio", None),
        "non_100_allocated_students": non_100_allocated_students,
        "non_100_allocated_students_ratio": request.session.get(
            "non_100_allocated_students_ratio", None
        ),
        "n_allocated_students": request.session.get("n_allocated_students", None),
        "n_students_per_course": request.session.get("n_students_per_course", "{}"),
    }


def json_deserialization(request):
    """This method converts json files to class objects and
    returns the App object and the context."""

    context = get_context_from_session(request)
    context.update(
        {
            "selected_students": pd.DataFrame(context["selected_students"]),
            "allocated_students": pd.DataFrame(context["allocated_students"]),
            "non_100_allocated_students": pd.DataFrame(
                context["non_100_allocated_students"]
            ),
        }
    )

    students_json = request.session.get("students", None)
    courses_json = request.session.get("courses", None)

    if not students_json or not courses_json:
        return HttpResponse("Something went wrong with the json files.", status=404)

    students_dicts = json.loads(students_json)
    class_object_students = []
    for student in students_dicts:
        student_obj = Student()
        for k, v in student.items():
            if k == "preferences":
                v = {int(p): c for p, c in v.items()}

            setattr(student_obj, k, v)

        class_object_students.append(student_obj)

    courses_dicts = json.loads(courses_json)
    class_object_courses = []
    for course in courses_dicts:
        course_obj = Course()
        for k, v in course.items():
            if k == "course_id":
                v = int(v)

            setattr(course_obj, k, v)

        class_object_courses.append(course_obj)

    new_app = App()
    new_app.students = class_object_students
    new_app.courses = class_object_courses
    return new_app, context


def delete_file_after_time(file_path, delay):
    """Deletes the specified file after a delay."""
    time.sleep(delay)
    if os.path.exists(file_path):
        os.remove(file_path)


def clear_context(request, context, min_stud, max_stud):
    context.update(
        {
            "allocated_students": None,
            "has_allocated_students": False,
            "min_stud": min_stud,
            "max_stud": max_stud,
            "error_message": request.session.get("error_message"),
            "avg_preferences_ratio": None,
            "non_100_allocated_students": None,
            "non_100_allocated_students_ratio": None,
            "n_allocated_students": None,
            "n_students_per_course": None,
        },
    )
    return context


def allocation_data_preparation(
    request,
    context,
    allocated_students,
    avg_preferences_ratio,
    students_preferences_ratio,
    courses,
    min_stud,
    max_stud
):
    n_students_per_course = {}
    for course in courses:
        n_students_per_course[f"{course.course_name}"] = int(
            allocated_students["Τίτλος Μαθήματος"].value_counts()[
                f"{course.course_name}"
            ]
        )
    non_100_allocated_students = students_preferences_ratio[
        students_preferences_ratio["% Ικανοποίησης των 6 Κορυφαίων Προτιμήσεων"] < 100
    ]
    non_100_allocated_students.loc[
        non_100_allocated_students["% Ικανοποίησης των 6 Κορυφαίων Προτιμήσεων"].index,
        "% Ικανοποίησης των 6 Κορυφαίων Προτιμήσεων",
    ] = non_100_allocated_students["% Ικανοποίησης των 6 Κορυφαίων Προτιμήσεων"].round(
        2
    )
    request.session["allocated_students"] = allocated_students.to_json(orient="records")
    request.session["non_100_allocated_students"] = non_100_allocated_students.to_json(
        orient="records"
    )
    request.session["has_allocated_students"] = True
    request.session["min_stud"] = min_stud
    request.session["max_stud"] = max_stud
    request.session["avg_preferences_ratio"] = avg_preferences_ratio
    n_allocated_students = len(pd.unique(allocated_students["AEM"]))
    non_100_allocated_students_ratio = round(100 - avg_preferences_ratio, 2)
    request.session["non_100_allocated_students_ratio"] = (
        non_100_allocated_students_ratio
    )
    request.session["n_allocated_students"] = n_allocated_students
    request.session["n_students_per_course"] = n_students_per_course
    request.session.pop("error_message")

    context.update(
        {
            "allocated_students": allocated_students,
            "has_allocated_students": True,
            "min_stud": min_stud,
            "max_stud": max_stud,
            "avg_preferences_ratio": avg_preferences_ratio,
            "non_100_allocated_students": non_100_allocated_students,
            "non_100_allocated_students_ratio": non_100_allocated_students_ratio,
            "n_allocated_students": n_allocated_students,
            "n_students_per_course": n_students_per_course,
        }
    )
    return context


def allocation(request):
    """
    Handles the student-to-course allocation for table display.
    Processes POST requests for allocation with the option of downloading results
    and renders the allocation page.
    """
    new_app, context = json_deserialization(request)
    excel_path = os.getcwd() + "\output.xlsx"

    if request.method == "POST" and "allocation-submit" in request.POST:
        min_stud = int(request.POST.get("min_stud", 0))
        max_stud = int(request.POST.get("max_stud", 0))

        if os.path.exists(excel_path):
            os.remove(excel_path)

        request.session.pop("allocated_students", None)
        request.session.pop("has_allocated_students", None)

        request.session["error_message"] = (
            "Infeasible solution. Please provide different min and max values."
        )
        context = clear_context(request, context, min_stud, max_stud)

        if min_stud < max_stud:
            for course in new_app.courses:
                course.min_students = min_stud
                course.max_students = max_stud

            allocated_students, avg_preferences_ratio, students_preferences_ratio = (
                new_app.run()
            )

            if allocated_students is not None and not allocated_students.empty:
                context = allocation_data_preparation(
                    request,
                    context,
                    allocated_students,
                    avg_preferences_ratio,
                    students_preferences_ratio,
                    new_app.courses,
                    min_stud,
                    max_stud
                )

    if request.method == "POST" and "allocation-download" in request.POST:
        allocation_download = request.POST.get("allocation-download")
        min_stud = request.session.get("min_stud", 0)
        max_stud = request.session.get("max_stud", 0)

        context.update(
            {
                "min_stud": min_stud,
                "max_stud": max_stud,
            },
        )

        if allocation_download == "download_excel":
            if os.path.exists(excel_path):
                file_thread = threading.Thread(
                    target=delete_file_after_time,
                    args=(
                        excel_path,
                        1,
                    ),
                )
                file_thread.start()
                return FileResponse(
                    open(excel_path, "rb"),
                    as_attachment=True,
                    filename=f"output_{min_stud}_{max_stud}.xlsx",
                )

    return render(request, "allocation.html", context)
