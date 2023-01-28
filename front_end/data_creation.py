import pandas as pd

if __name__ == '__main__':
    course_info = {"Course_ID": {
        "CS 120a": {"Student_ID": [], "Student Name": [], "Current_Enrollment": 0, "Max_Enrollment": 20},
        "CS 120b": {"Student_ID": [], "Student Name": [], "Current_Enrollment": 0, "Max_Enrollment": 20},
        "CS 120c": {"Student_ID": [], "Student Name": [], "Current_Enrollment": 0, "Max_Enrollment": 20},
        "CS 120d": {"Student_ID": [], "Student Name": [], "Current_Enrollment": 0, "Max_Enrollment": 20},
        "CS 120e": {"Student_ID": [], "Student Name": [], "Current_Enrollment": 0, "Max_Enrollment": 20}},
        "CS 120f": {"Student_ID": [], "Student Name": [], "Current_Enrollment": 0, "Max_Enrollment": 20},
        "CS 120g": {"Student_ID": [], "Student Name": [], "Current_Enrollment": 0, "Max_Enrollment": 20},
        "CS 120h": {"Student_ID": [], "Student Name": [], "Current_Enrollment": 0, "Max_Enrollment": 20},
        "CS 120i": {"Student_ID": [], "Student Name": [], "Current_Enrollment": 0, "Max_Enrollment": 20},
        "CS 120j": {"Student_ID": [], "Student Name": [], "Current_Enrollment": 0, "Max_Enrollment": 20},
        },
    }

    df = pd.DataFrame(course_info)
    df.to_csv("course_info.csv", index=False)
