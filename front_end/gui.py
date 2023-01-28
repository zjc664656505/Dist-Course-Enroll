import tkinter as tk
from tkinter import messagebox
from tkinter import *
import tkinter.ttk as ttk

# global variable student data
# All student data will be stored in this variable
# Current data are sample student data
student_data = [
    ['1', 'John', '1'],
    ['1', 'John', '2'],
    ['1', 'John', '3'],
    ['1', 'John', '4'],
    ['1', 'John', '5'],
    ['1', 'John', '6'],
]


# button function to send request to server
def send_request():
    # TODO
    pass

# buttom function clear student data
def clear_student_data():
    student_id_entry.delete(0, tk.END)
    student_name_entry.delete(0, tk.END)
    course_id_entry.delete(0, tk.END)
    load_student_data()

def put_student_in_entry(index):
    student_id_entry.delete(0, tk.END)
    student_name_entry.delete(0, tk.END)
    course_id_entry.delete(0, tk.END)

    s_id = student_data[index][0]
    s_name = student_data[index][1]
    s_course = student_data[index][2]

    student_id_entry.insert(0, s_id)
    student_name_entry.insert(0, s_name)
    course_id_entry.insert(0, s_course)


# button function add student data
def add_student_data(student_id, student_name, student_course):
    if any(student_course in data for data in student_data) and any(student_id not in data for data in student_data):
        student_data.append([student_id, student_name, student_course])
    elif any(student_course in data for data in student_data) and any(student_id in data for data in student_data):
        messagebox.showerror("Error", "You have already attempted to enrollin this course!")
    load_student_data()


# button function delete student data
def delete_student_data(index):
    try:
        del student_data[index]
        load_student_data()
    except:
        pass


# button function load student data
def load_student_data():
    for i in record_table.get_children():
        record_table.delete(i)

    for i in range(len(student_data)):
        record_table.insert(parent='', index='end', iid=i, text='', values=student_data[i])


# Front-End GUI Design
root_window = tk.Tk()
root_window.title("UCI Course Enrollment System")
root_window.geometry("500x600")

# Create a label for the title
head_frame = tk.Frame(root_window)
heading_lb = tk.Label(head_frame, text="UCI Course Enrollment System", font=("Bold", 13), bg="blue", fg="yellow")
heading_lb.pack(fill=tk.X, pady=5)
head_frame.pack(pady=10)
head_frame.pack_propagate(False)
head_frame.configure(width=400, height=300)

####ENTRY BOX#####
# create student id
student_id_lb = tk.Label(head_frame, text="Student ID: ", font=("Bold", 10), bg="blue", fg="yellow")
student_id_lb.place(x=0, y=50)
student_id_entry = tk.Entry(head_frame, font=('Bold', 10))
student_id_entry.place(x=110, y=50, width=150)

# create student name
student_name_lb = tk.Label(head_frame, text="Student Name: ", font=("Bold", 10), bg="blue", fg="yellow")
student_name_lb.place(x=0, y=80)
student_name_entry = tk.Entry(head_frame, font=('Bold', 10))
student_name_entry.place(x=110, y=80, width=150)

# create course id
course_id_lb = tk.Label(head_frame, text="Course ID: ", font=("Bold", 10), bg="blue", fg="yellow")
course_id_lb.place(x=0, y=110)
course_id_entry = tk.Entry(head_frame, font=('Bold', 10))
course_id_entry.place(x=110, y=110, width=150)

#####BUTTON######
# course enrollment button
enroll_btn = tk.Button(head_frame, text="Enroll", font=("Bold", 12), bg="blue", fg="yellow",
                       command=lambda: add_student_data(student_id_entry.get(),
                                                        student_name_entry.get(),
                                                        course_id_entry.get()))
enroll_btn.place(x=0, y=150)

# course drop button
drop_btn = tk.Button(head_frame, text="Drop", font=("Bold", 12), bg="blue", fg="yellow",
                     command=lambda: delete_student_data(index=int(record_table.selection()[0])))
drop_btn.place(x=150, y=150)

# course clear button
clear_btn = tk.Button(head_frame, text="Clear", font=("Bold", 12), bg="blue", fg="yellow",
                      command=lambda :clear_student_data())
clear_btn.place(x=300, y=150)

# course send request button
send_request_btn = tk.Button(head_frame, text="Send Request", font=("Bold", 12), bg="blue", fg="yellow")
send_request_btn.place(x=120, y=200)

# build record
record_frame = tk.Frame(root_window, bg="white")
record_lb = tk.Label(record_frame, text="Select Course to Drop", font=("Bold", 13), bg="blue", fg="yellow")
record_lb.pack(fill=tk.X)
record_table = ttk.Treeview(record_frame)
record_table.pack(fill=tk.X, pady=5)

record_table.bind('<<TreeviewSelect>>',
                  lambda event: put_student_in_entry(index=int(record_table.selection()[0])))
record_table['columns'] = ["Student ID", "Student Name", "Course ID"]
record_table.column("#0", anchor=tk.W, width=0, stretch=tk.NO)
record_table.column("Student ID", anchor=tk.W, width=100)
record_table.column("Student Name", anchor=tk.W, width=150)
record_table.column("Course ID", anchor=tk.W, width=100)

record_table.heading("Student ID", text="Student ID", anchor=tk.W)
record_table.heading("Student Name", text="Student Name", anchor=tk.W)
record_table.heading("Course ID", text="Course ID", anchor=tk.W)

record_frame.pack()
record_frame.pack_propagate(False)
record_frame.configure(width=400, height=200)
load_student_data()

root_window.mainloop()
