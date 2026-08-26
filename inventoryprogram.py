#Inventory Program Version 3 (GUI transition)
#import libraries
from tkinter import*
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk

#student class
class Student():
    def __init__(self, student_id, email, name, password):
        self.student_id = student_id
        self.email = email
        self.name = name
        self.password = password
        self.inventory = []

def load_students():
    try:
        with open('students.json','r') as file:
            data = json.load(file)
        students = {}
        for student_id, student_data in data.items():
            student = Student(
                int(student_id),
                student_data["Name"],
                student_data["Password"],
                student_data["Email"]
            )
            student.inventory = student_data["Inventory"]
            students[int(student_id)] = student
        return students
    except FileNotFoundError:
        return {}
def save_students():
    data = {}
    for student_id, student in students.items():
        data[str(student_id)] = {
            "Name":student.name,
            "Email":student.email,
            "Password":student.password,
            "Inventory":student.inventory
        }
    with open("students.json","w") as file:
        json.dump(data,file,indent = 4)

#inventory main app class
class InventoryApp:

    def __init__(self, root):
        #window
        self.root = root
        self.root.title("Inventory Management System")
        self.root.state("zoomed")
        self.root.configure(bg="aliceblue" )
        #store and load current student data
        self.students = load_students()
        self.current_student = None

        #title frame
        self.title_frame = Frame(self.root,bg="midnightblue",height=80)
        self.title_frame.pack(fill=X)
        self.title_frame.pack_propagate(False)
        Label(self.title_frame,text="INVENTORY MANAGEMENT SYSTEM",font=("Garamond", 24, "bold"),bg="midnightblue",fg="white").pack(pady=20)

        #main frame
        self.main_frame = Frame(self.root,bg="aliceblue")
        self.main_frame.pack(fill=BOTH,expand=True)

        #footer frame
        self.footer_frame = Frame(self.root,bg="white",height=160)
        self.footer_frame.pack(fill=X)
        self.footer_frame.pack_propagate(False)

        # Start with the login page
        self.show_login()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def clear_footer(self):
        for widget in self.footer_frame.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_main_frame()
        self.clear_footer()

        Label(self.main_frame,text="LOGIN",font=("Garamond", 28, "bold"),bg="aliceblue",fg="midnightblue").pack(pady=50)
        Label(self.main_frame,text="Student ID",font=("Calibri", 12),bg="aliceblue").pack()
        Entry(self.main_frame,width=30).pack(pady=10)
        Label(self.main_frame,text="Password",font=("Calibri", 12),bg="aliceblue").pack()
        Entry(self.main_frame,width=30,show="*").pack(pady=10)
        Button(self.main_frame,bg = "midnightblue", fg = "snow", activebackground = "lightskyblue1", activeforeground = "midnightblue",text="Login",width=20).pack(pady=20)
        Button(self.main_frame,bg = "midnightblue", fg = "snow", activebackground = "lightskyblue1", activeforeground = "midnightblue",text="Create Account",width=20,command=self.show_signup).pack()

        # Footer is only displayed on login
        self.create_footer()


    def show_signup(self):
        self.clear_main_frame()
        self.clear_footer()
        Label(self.main_frame,text="CREATE ACCOUNT",font=("Garamond", 28, "bold"),bg="aliceblue",fg="midnightblue").pack(pady=50)  
        Button(self.main_frame,bg = "midnightblue", fg = "snow", activebackground = "lightskyblue1", activeforeground = "midnightblue",text="Back to Login",command=self.show_login).pack(pady=20)

    def create_footer(self):
        cards = [
            ("📦","Pocket Inventory","Keep track of \nstudent belongings."),

            ("🔒","Protected Data","Secure storage\n for all records."),

            ("🔔","Easy Management","Quickly manage and stay\n updated about your items."),

            ( "📊","Statistical Analysis","View inventory and school\n statistics easily."
            )
        ]

        for icon, title, description in cards:

            card = Frame(
                self.footer_frame,
                bg="aliceblue",
                bd=1,
                relief="solid"
            )

            card.pack(
                side=LEFT,
                expand=True,
                fill=BOTH,
                padx=10,
                pady=15
            )


            Label(
                card,
                text=icon,
                font=("Segoe UI Emoji", 22),
                bg="aliceblue"
            ).pack(
                pady=5
            )


            Label(
                card,
                text=title,
                font=("Garamond", 13, "bold"),
                bg="aliceblue"
            ).pack()


            Label(
                card,
                text=description,
                font=("Calibri", 10),
                bg="aliceblue"
            ).pack(
                pady=5
            )


#start the program
root = Tk()
app = InventoryApp(root)
root.mainloop()