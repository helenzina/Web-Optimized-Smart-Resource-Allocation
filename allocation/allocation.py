# students = [] # students aem (string) or students name (string)
# students_gpa = [] # students gpa (int scaled up *= 100)
# all_students = range(len(students))

# required_courses_per_student = [] # how many courses can a student take
# extra_courses_per_student = [] # how many extra courses can a student take

# courses = [] # courses names (string)
# all_courses = range(len(courses))

# courses_min_students = [] # min students for each course (int)
# courses_max_students = [] # max students for each course (int)

# preferences_rank = [
# 	[], # student, course_preference (booleans)
# 	[]
# ]

# # constraints

# model.minimize(
#     sum(preferences_rank * allocation * students_gpa)
# )


# e.g.
from ortools.sat.python import cp_model

SCALING_FACTOR = 100

students = ["20046", "21110", "20000"]
students_gpa = [8.83, 6, 7.5]
students_gpa_scaled = [x * SCALING_FACTOR for x in students_gpa]
all_students = range(len(students))

required_courses_per_student = [3, 1, 0] 
extra_courses_per_student = [3, 2, 0] 

courses = ["Compilers", "Knowledge Mining", "Introduction to Robotics"]
all_courses = range(len(courses))

courses_min_students = [1, 1, 1] # min students for each course (int)
courses_max_students = [3, 3, 3] # max students for each course (int)

model = cp_model.CpModel()

allocation = [[model.new_bool_var(f"allocation_{s}_{c}") for c in all_courses] for s in all_students]

preferences_rank = [
	[1, 2, 3],
	[3, 2, 1],
	[1, 3, 2],
]
all_preferences = range(len(preferences_rank[0]))

# constraints

# each student i must attend exactly xi courses
# for s in all_students:
#     model.add(sum(allocation[s][c] for c in all_courses) == required_courses_per_student[s])

# m<=course_capacity<=M
# for c in all_courses:
#     # each course has min students m (courses_min_students[c])
#     model.add(sum(allocation[s][c] for s in all_students) >= courses_min_students[c])
#     # each course has max students M (courses_max_students[c])
#     model.add(sum(allocation[s][c] for s in all_students) <= courses_max_students[c])
# in case of infeasibility, we could create a list of integer variables representing each course's domain values
# so that we could make the script change them in an "automatic" way until the solution is optimal or at least feasible

# it may be useless due to objective functions- a thought of allocation based on gpa (but everything needs to be sorted)

# indices = np.argsort(students) 
# sorted_students = [students[i] for i in indices]
# sorted_students_gpa_scaled = [students_gpa_scaled[i] for i in indices]
# sorted_preferences_rank = [preferences_rank[i] for i in indices]
# for p in all_preferences:
#     for c in all_courses:
#         for s in all_students:
#             if sorted_preferences_rank[s][c] == p+1:
#                 model.add(allocation[s][c] == 1) # it's already constrained to be at most the max of the course's capacity
        



# old

# model.minimize(
#     sum(preferences_rank[s][c] * allocation[s][c] * students_gpa_scaled[s] 
#         for s in all_students 
#         for c in all_courses)
# )

# solver = cp_model.CpSolver()
# status = solver.solve(model)

# if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
#     for c in all_courses:
#         print(f"{courses[c]}:\n")
#         print(f"{"Course":<20} {"GPA":<20} {"Preference":<20} \n")
#         for s in all_students:
#             if solver.value(allocation[s][c]): 
#                 print(f"{students[s]:<20} {(students_gpa_scaled[s]/SCALING_FACTOR):<20} {preferences_rank[s][c]:<20}")
#     print()

# else:
#     print("Infeasible solution.")

# new

# maximize student allocation based on their gpa
model.maximize(
    sum(students_gpa_scaled[s] * allocation[s][c]
        for s in all_students 
        for c in all_courses)
)

solver = cp_model.CpSolver()
status = solver.solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    maximized_gpa_allocation = [[solver.value(allocation[s][c]) for c in all_courses] for s in all_students]
    
    for s in all_students:
        for c in all_courses:
            model.add_hint(allocation[s][c], maximized_gpa_allocation[s][c])
    
    # minimize student allocation based on their preferences
    model.minimize(
        sum(preferences_rank[s][c] * allocation[s][c]
            for s in all_students
            for c in all_courses)
    )

    solver = cp_model.CpSolver()
    status = solver.solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for c in all_courses:
            print(f"{courses[c]}:\n")
            print(f"{"Course":<20} {"GPA":<20} {"Preference":<20} \n")
            for s in all_students:
                if solver.value(allocation[s][c]): 
                    print(f"{students[s]:<20} {(students_gpa_scaled[s]/SCALING_FACTOR):<20} {preferences_rank[s][c]:<20}")
        print()

    else:
        print("Infeasible solution.")

