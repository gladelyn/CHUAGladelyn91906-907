#Inventory Program Version 3 (GUI transition)
#import libraries
from tkinter import*
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import json
import hashlib

#inventory items class
class InventoryItem:
    def __init__(self, name, item_id, due_date):
        self.name = name
        self.item_id = item_id
        self.due_date = due_date
        self.status = "Borrowed"

    def mark_as_missing(self):
        self.status = "Missing"

    def mark_as_returned(self):
        self.status = "Returned"

#User class (generic parent class which has all the attributes for teacher and student)
class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

#student class
class Student(User):
    def __init__(self, student_id, email, name, password):
        User.__init__(self,name,email,password)
        self.student_id = student_id
        self.inventory = []

    def add_item(self, item):
        self.inventory.append(item)

    def delete_item(self, index):
        if 0<= index <len(self.inventory):
            return self.inventory.pop(index)
        return None

class Teacher(User):
    def __init__(self, teachercode, name, email, password):
        User.__init__(self,name, email, password)
        self.teachercode = teachercode

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

def hash_pswd(password):
    return hashlib.sha256(password.encode()).hexdigest()

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

        Label(self.main_frame,text="LOGIN",font=("Garamond", 28, "bold"),bg="aliceblue",fg="midnightblue").pack(pady=40)
        Label(self.main_frame,text="Student ID",font=("Calibri", 12),bg="aliceblue").pack()
        identry = Entry(self.main_frame, width = 30)
        identry.pack(pady = 10)
        Label(self.main_frame,text="Password",font=("Calibri", 12),bg="aliceblue").pack()
        pswdentry = Entry(self.main_frame, width = 30, show = "*")
        pswdentry.pack(pady =10)
        def login():
            studennt_id = identry.get().strip()
            password = pswdentry.get()
            #checking for empty fields
            if not student_id or not password:
                messagebox.showwarning("Missing Information","Please enter your Student ID and password.")
                return
            #validating the student id
            if not student_id.isdigit() or len(student_id) !=5:
                messagebox.showerror("Invalid Student ID","Student ID must be 5 digits.")
                return
            #checking whether ID has been signed up already
            if student_id not in self.students:
                messagebox.showerror("Login Failed","Student ID does not exist, please go to sign up")
                return
            student = self.students[student_id]
            #checking the password against hashed password
            if hash_pswd(password) != student.password:
                messagebox.showerror("Login Failed","Incorrect Password. Please try again.")
                return
            #store the current student as object
            self.current_student = student
            #switch to dashboard/homepage
            self.show_home()

        Button(self.main_frame,bg = "midnightblue", fg = "snow", activebackground = "lightskyblue1", activeforeground = "midnightblue",text="Login",width=20,command = login).pack(pady=20)
        Button(self.main_frame,bg = "midnightblue", fg = "snow", activebackground = "lightskyblue1", activeforeground = "midnightblue",text="Create Account",width=20,command=self.show_signup).pack()

        # Footer is only displayed on login
        self.create_footer()


    def show_signup(self):
        self.clear_main_frame()
        self.clear_footer()
        Label(self.main_frame,text="CREATE ACCOUNT",font=("Garamond", 28, "bold"),bg="aliceblue",fg="midnightblue").pack(pady=50)  
        Label(self.main_frame, text = "Name", bg = "aliceblue").pack()
        nameentry = Entry(self.main_frame, width = 30)
        nameentry.pack(pady = 5)
        Label(self.main_frame, text = "Student ID",bg = "aliceblue").pack()
        identry = Entry(self.main_frame, width =30)
        identry.pack(pady = 5)
        Label(self.main_frame, text = "Email", bg = "aliceblue").pack()
        emailentry = Entry(self.main_frame, width = 30)
        emailentry.pack(pady = 5)
        Label(self.main_frame, text = "Password", bg = "aliceblue").pack()
        pswdentry = Entry(self.main_frame, width = 30, show = "*")
        pswdentry.pack(pady = 5)
        def signup():
            name = nameentry.get().strip()
            student_id = identry.get().strip()
            email = emailentry.get().strip()
            password = pswdentry.get().strip()

            #check for empty fields
            if not name or not student_id or not email or not password:
                messagebox.showwarning("Missing Information","Please complete all fields.")
                return
            #check student id
            if not student_id.isdigit() or len(student_id)!= 5:
                messagebox.showerror("Invalid Student ID","Student ID must be 5 digits")
                return
            student_id = int(student_id)
            #checking whether the id already exists
            if student_id in self.students:
                messagebox.showerror("Account Already Exists","This Student ID is already registed.")
                return
            #creating the student object after signup is verified
            student = Student(student_id, name, email, hash_pswd(password))
            #adding student to the dictionary and saving as current student
            self.students[student_id] = student
            save_students(self.students)
            self.current_student = student
            messagebox.showinfo("Account Successfully Created",f"Hello {name}, welcome to the Inventory Management System!")

            #return to dashboard
            self.show_home()

        Button(self.main_frame, text = "Sign Up",bg = "midnightblue", fg = "snow", activebackground = "lightskyblue1", activeforeground = "midnightblue", width = 20, command = signup).pack(pady = 15)
        Button(self.main_frame,bg = "midnightblue", fg = "snow", activebackground = "lightskyblue1", activeforeground = "midnightblue",text="Back to Login",width = 20, command=self.show_login).pack()

    def show_home(self):
        self.clear_main_frame()
        self.clear_footer()
        student = self.current_student

        Label(self.main_frame, text = f"Welcome, {student.name}", font = ("Garamond", 28, "bold"),bg = "aliceblue",fg = "midnightblue").pack(pady = 30)
        Label(self.main_frame, text = "Inventory Dashboard", font = ("Calibri",14),bg = "aliceblue").pack()
        stats_frame = Frame(self.main_frame, bg = "aliceblue")
        statsframe.pack(pady = 30)
        self.create_stats_card(stats_frame,"📦", "Total Items", len(student.inventory) )

        #quick action buttons
        Label(self.main_frame, text = "Quick Actions",font = ("Garamond",20,"bold"),bg = "aliceblue",fg = "midnightblue").pack(pady = 15)
        Button(self.mainframe,text = "📦 Manage Your Inventory", width = 25,height = 2, command = self.show_inventory).pack(pady = 5)
        Button(self.main_frame, text = "🔔 Notifications", width = 25, height = 2, command = self.show_notifications).pack(pady = 5)
        Button(self.main_frame, text = "🚨 Report an Incident",width = 25, height = 2, command = self.show_reports).pack(pady = 5)
        Button(self.main_frame, text = "Logout", width = 25, height = 2, command = self.logout).pack(pady = 15)

    def show_inventory(self):
        self.clear_main_frame()
        self.clear_footer()
        student = self.current_student

        Label(self.main_frame, text = "My Inventory", font = ("Garamond",28,"bold"),bg = "aliceblue",fg = "midnightblue").pack(pady =25)
        Label(self.main_frame, text = f"{student.name}'stored items",font = ("Calibri",13),bg = "aliceblue").pack(pady = 5)

        inventoryframe = Frame(self.main_frame, bg = "aliceblue")
        inventoryframe.pack(fill = BOTH, expand = True, padx = 50, pady = 20)
        Label(inventoryframe, text = "Item Name", font = ("Garamond",13,"bold"),bg = "aliceblue").grid(row = 0,column = 0, padx = 20, pady = 10)
        Label(inventoryframe, text = "ID Number", font = ("Garamond",13,"bold"),bg = "aliceblue").grid(row = 0,column = 2, padx = 20, pady = 10)
        #displaying the items
        if len(student.inventory) ==0:
            Label(inventoryframe, text = "No items have been stored yet.",font = ("Calibri",12),bg = "aliceblue").grid(row = 1, column = 0, columnspan = 3, pady = 30)
        else:
            for index, item in enumerate(student.inventory):
                Label(inventoryframe, text = item["Name"],bg = "white",width =20).grid(row = index + 1, column = 0, padx = 10, pady = 5)
                Label(inventoryframe, text = item["ID Number"],bg = "white", width = 20).grid(row = index +1, column = 1, padx = 10, pady = 5)
                Label(inventoryframe, text = item["Due Date"], bg = "white",width = 20).grid(row = index +1, column = 2, padx = 10, pady = 5)

        Button(self.main_frame, text = "Add an Item", width = 20, command = self.add_item).pack(side =LEFT, padx = 10, pady = 20)
        Button(self.main_frame, text = "Remove an Item", width = 20, command = self.delete_item).pack(side = LEFT, padx = 10, pady = 20)
        Button(self.main_frame, text = "Return to Dashboard",width = 20, command = self.show_home).pack(side = LEFT, padx = 10, pady = 20)

    def add_item(self):
        #creating a new separate window to add items from
        addwindow = Toplevel(self.root)
        addwindow.title("Add an Item")
        addwindow.geometry("400x400")
        addwindow.configure(bg = "aliceblue")

        Label(addwindow, text = "Add an item to your inventory", font = ("Garamond",22,"bold"),bg = "aliceblue",fg = "midnightblue" ).pack(pady =25)
        Label(addwindow, text = "Item Name",bg = "aliceblue").pack()
        nameentry = Entry(addwindow, width = 30)
        nameentry.pack(pady = 8)
        Label(addwindow,text = "ID Number",bg = "aliceblue").pack()
        identry = Entry(addwindow,width = 30)
        identry.pack(pady = 8)
        Label(addwindow, text = "Due Date",bg = "aliceblue").pack()
        dueentry = Entry(addwindow, width = 30)
        dueentry.pack(pady = 8)

        def save_item():
            item_name = nameentry.get().strip()
            item_id = identry.get().strip()
            due_date = dueentry.get().strip()
            #checking for empty fields
            if not item_name or not item_id or not due_date:
                messagebox.showwarning("Missing Informaiton","Please complete all fields.")
                return
            #creating an item dictionary to store it as a set
            item = {
                "Name":item_name,
                "ID Number":item_id,
                "Due Date": due_date
            }
            #adding item to current student's inventory list then saving
            self.current_student.add_item(item)
            save_students(self.students)
            messagebox.showinfo("Item Added","Your item has been successfully added.")

            addwindow.destroy()
            self.show_inventory()

        Button(addwindow, text = "Save Item", width = 20, command = save_item).pack(pady = 20)
        Button(addwindow, text = "Cancel", width = 20, command = addwindow.destroy).pack()

    def delete_item(self):
        student = self.current_student
        #again, checking whether inventory is empty
        if len(student.inventory) == 0:
            messagebox.showinfo("No Items","There are no items to remove.")
            return

        #creating a new separate window to remove items
        deletewindow = Toplevel(self.root)
        deletewindow.title("Remove an Item")
        deletewindow.geometry("400x400")
        deletewindow.configure(bg = "aliceblue")

        Label(deletewindow, text = "Remove an item from your inventory.",font = ("Garamond",22,"bold"),bg = "aliceblue",fg ="midnightblue").pack(pady = 20)
        Label(deletewindow, text = "Select the number of the item you wish to remove: ",bg = "aliceblue").pack(pady = 10)

        for index, item in enumerate(student.inventory):
            Label(deletewindow, text = f"{index+1}.{item["Name"]}"f"({item["ID Number"]})",bg = "aliceblue").pack(pady = 3)

        indexentry = Entry(deletewindow, width = 20)
        indexentry.pack(pady = 15)

        def confirm_delete():
            index_text = indexentry.get().strip()
            if not index_text.isdigit():
                messagebox.showerror("Invalid Input","Please enter a valid item number from the list.")
                return
            index = int(index_text) - 1
            if index < 0 or index >= len(student.inventory):
                messagebox.showerror("Invalid Item","That item number does not exist")
                return

            item_name = student.inventory[index]["Name"]
            confirmation = messagebox.askyesno("Confirm Delete",f"Are you sure you want to remove "f"'{item_name}'?")
            if confirmation:
                student.delete_item(index)
                save_students(self.students)
                messagebox.showinfo("Item Deleted","Item Successfully Removed")
                deletewindow.destroy()
                self.show_inventory()

        Button(deletewindow, text = "Remove", width =20, command = confirm_delete).pack(pady = 10)
        Button(deletewindow, text = "Cancel", width = 20, command = deletewindow.destroy).pack()


    def create_stat_card(self, parent, icon, title, value):
        card = Frame(parent, bg = "white", bd = 1, relief = "solid",width = 220, height = 130)
        card.pack(side = LEFT, padx =10)
        card.pack_propagate(False)
        Label(card, text = icon, font = ("Segoe UI Emoji", 25), bg = "white").pack(pady = 5)
        Label(card, text = title, font = ("Garamond",13,"bold"),bg = "white").pack()
        Label(card, text = value, font = ("Garamond",20,"bold"),bg ="white").pack()

    def logout(self):
        self.current_student = None
        self.show_login()

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