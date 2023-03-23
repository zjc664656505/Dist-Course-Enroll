import tkinter as tk
from tkinter import messagebox
from tkinter import *
import tkinter.ttk as ttk
import requests
import json
import os

#############################################################
                    #Register#
#############################################################
def main_account_screen():
    global main_screen
    main_screen = Tk()# create a GUI window
    main_screen.geometry("300x250")  # set the configuration of GUI window
    main_screen.title("Account Login")  # set the title of GUI window


    # create a Form label
    Label(text="Choose Login Or Register", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()

    # create Login Button
    Button(text="Login", height="2", width="30", command=login).pack()
    Label(text="").pack()

    # create a register button

    Button(text="Register", height="2", width="30", command=register).pack()

    main_screen.mainloop()  # start the GUI


def register():
    # The Toplevel widget work pretty much like Frame,
    # but it is displayed in a separate, top-level window.
    # Such windows usually have title bars, borders, and other “window decorations”.
    # And in argument we have to pass global screen variable

    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250")

    # Set text variables
    global username
    global password
    global username_entry
    global password_entry

    username = StringVar()
    password = StringVar()

    # Set label for user's instruction
    Label(register_screen, text="Please enter details below", bg="blue").pack()
    Label(register_screen, text="").pack()

    # Set username label
    username_lable = Label(register_screen, text="Student ID")
    username_lable.pack()

    # Set username entry
    # The Entry widget is a standard Tkinter widget used to enter or display a single line of text.

    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()

    # Set password label
    password_lable = Label(register_screen, text="Student Name")
    password_lable.pack()

    # Set password entry
    password_entry = Entry(register_screen, textvariable=password)
    password_entry.pack()

    Label(register_screen, text="").pack()

    # Set register button
    Button(register_screen, text="Register", width=10, height=1, bg="blue", command = register_user).pack()



def register_user():
    # get username and password
    username_info = username.get()
    password_info = password.get()

    # Open file in write mode
    # student_ident.append([username_info, password_info])
    # print(student_ident)
    print(json.loads(requests.get(f"http://127.0.0.1:3000/register?studentId={username_info}&studentName={password_info}").content))


    username_entry.delete(0, END)
    password_entry.delete(0, END)

#############################################################
                    #Login#
#############################################################
# set a label for showing success information on screen
def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify
    global username_login_entry
    global password_login_entry

    username_verify = StringVar()
    password_verify = StringVar()

    Label(login_screen, text="Student ID").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Student Name").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify)
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command=login_verify).pack()


def login_verify():
    # get username and password

    username1 = username_verify.get()
    password1 = password_verify.get()
    # this will delete the entry after login button is pressed
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    student_login_bool = json.loads(requests.get(f"http://127.0.0.1:3000/login?studentId={username1}&studentName={password1}").content)
    if "success" in student_login_bool:
        login_sucess()
    else:
        tk.messagebox.showinfo("error", student_login_bool["error"])


def login_sucess():
    global login_success_screen  # make login_success_screen global
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Login Success").pack()

    # create OK button
    Button(login_success_screen, text="OK", command=enrollment_window).pack()





#############################################################
                    #Enrollment window#
#############################################################
def enrollment_window():
    student_data = json.loads(requests.get("http://127.0.0.1:3000/records").content)


    # button function to send request to server
    def send_request():
        # TODO: send request to server
        # Incomplete
        messagebox.showinfo("Success", "Request sent to server!")

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
        # send add request to remote server
        student_add_bool = json.loads(requests.get(f"http://127.0.0.1:3000/insert?classId={student_course}&studentName={student_name}&studentId={student_id}").content)
        if "success" in student_add_bool:
            student_data.append([student_id, student_name, student_course])
            messagebox.showinfo("Enrollment list", student_course+ " has been added to the enrollment list")
            load_student_data()
        else:
            messagebox.showinfo("Error", student_add_bool["error"])


    # button function delete student data
    def delete_student_data(index):
        student_info = student_data[index]
        s_id, s_name, c_id = student_info[0], student_info[1], student_info[2]
        student_del_bool = json.loads(requests.get(f"http://127.0.0.1:3000/delete?classId={c_id}&studentName={s_name}&studentId={s_id}").content)
        if "success" in student_del_bool:
            del student_data[index]
            messagebox.showinfo("Enrollment list", "Selected course has been dropped from the enrollment list")
            load_student_data()
        else:
            messagebox.showinfo("Error", student_del_bool["error"])


    # button function load student data
    def load_student_data():
        for i in record_table.get_children():
            record_table.delete(i)

        for i in range(len(student_data)):
            record_table.insert(parent='', index='end', iid=i, text='', values=student_data[i])


    # Front-End GUI Design
    root_window = Toplevel(login_success_screen)
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


if __name__ == "__main__":
    main_account_screen()