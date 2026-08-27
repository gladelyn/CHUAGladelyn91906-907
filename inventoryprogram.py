#Inventory Program Version 3 (GUI transition)
#import libraries
from tkinter import*
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
from datetime import datetime
import smtplib
from email.message import EmailMessage
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

    def check_overdue(self):
        try:
            due_date = datetime.strptime(self.due_date,"%d/%m/%Y")
            if datetime.now() >due_date:
                self.status = "Overdue"
                return True
        except ValueError:
            return False
        return False


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
        self.notifications = []

    def add_item(self, item):
        self.inventory.append(item)

    def delete_item(self, index):
        if 0<= index <len(self.inventory):
            return self.inventory.pop(index)
        return None

    def add_notification(self, notification):
        self.notifications.append(notification)

class Teacher(User):
    def __init__(self, teachercode, name, email, password):
        User.__init__(self,name, email, password)
        self.teachercode = teachercode

    def analyse_trends(self, students, reports):
        total_students = len(students)
        total_items = 0

        for student in students.values():
            total_items += len(student.inventory)

        total_reports = len(reports)
        total_overdue = 0
        for student in students.values():
            for item in student.inventory:
                try:
                    due_date = datetime.strptime(item["Due Date"], "%d/%m/%Y")
                    if due_date.date() < datetime.now().date():
                        total_overdue +=1
                except ValueError:
                    continue 

        return {
            "Students":total_students,
            "Items":total_items,
            "Reports":total_reports,
            "Overdue":total_overdue
        }

def load_students():
    try:
        with open('students.json','r') as file:
            data = json.load(file)
        students = {}
        for student_id, student_data in data.items():
            student = Student(
                int(student_id),
                student_data["Email"],
                student_data["Name"],
                student_data["Password"],
            )
            student.inventory = student_data["Inventory"]
            students[int(student_id)] = student
        return students
    except FileNotFoundError:
        return {}
def save_students(students):
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

def load_reports():
    try:
        with open("reports.json","r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_reports(reports):
    with open("reports.json","w") as file:
        json.dump(reports, file, indent = 4)

def hash_pswd(password):
    return hashlib.sha256(password.encode()).hexdigest()

def send_email(recipient, subject, message):
    try:
        email = EmailMessage()
        email["Subject"] = subject
        email["From"] = "YOUR_SYSTEM_EMAIL"
        email["To"] = recipient
        email.sent_content(message)

        #email server connection
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.send_message(email)
        server.quit()
        return True
    except Exception:
        return False
#notifications class
class Notification:
    def __init__(self, message, notification_type):
        self.message = message
        self.notification_type = notification_type
        self.read = False

    def mark_as_read(self):
        self.read = True

    def to_dictionary(self):
        return {
            "Message":self.message,
            "Type":self.notification_type,
            "Read":self.read
        }

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
        #loading reports
        self.reports = load_reports()

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

    def create_button(self,parent, text, command, width = 20):
        button = Button(parent, text= text, width = width, height =2, bg = "midnightblue",fg = "white",activebackground = "lightskyblue1",activeforeground = "midnightblue",command = command)
        button.pack(side = LEFT, padx = 8)
        return button
    

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
            student_id = identry.get().strip()
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

        def clear_fields():
            identry.delete(0,END)
            pswdentry.delete(0,END)

        buttonframe = Frame(self.main_frame, bg = "aliceblue")
        buttonframe.pack(pady =20)
        self.create_button(buttonframe, "Clear Fields",clear_fields,20)
        self.create_button(buttonframe,"Login",login,20)
        self.create_button(buttonframe,"Create Account",self.show_signup,20)

        
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

        def clear_fields():
            nameentry.delete(0,END)
            identry.delete(0,END)
            emailentry.delete(0,END)
            pswdentry.delete(0,END)           

        buttonframe = Frame(self.main_frame, bg = "aliceblue")
        buttonframe.pack(pady = 20)
        Button(buttonframe, text = "Clear Fields",bg = "midnightblue",fg = "snow",activebackground = "lightskyblue1",activeforeground = "midnightblue",width = 20,command = clear_fields).pack(side = LEFT, padx = 8)
        Button(buttonframe, text = "Sign Up",bg = "midnightblue", fg = "snow", activebackground = "lightskyblue1", activeforeground = "midnightblue", width = 20, command = signup).pack(side = LEFT, padx = 8)
        Button(buttonframe,bg = "midnightblue", fg = "snow", activebackground = "lightskyblue1", activeforeground = "midnightblue",text="Return to Login",width = 20, command=self.show_login).pack(side = LEFT, padx =8)

        self.create_footer()

    def show_home(self):
        self.clear_main_frame()
        self.clear_footer()
        self.check_notifications()
        student = self.current_student

        Label(self.main_frame, text = f"Welcome, {student.name}", font = ("Garamond", 28, "bold"),bg = "aliceblue",fg = "midnightblue").pack(pady = 30)
        Label(self.main_frame, text = "Inventory Dashboard", font = ("Calibri",14),bg = "aliceblue").pack()
        stats_frame = Frame(self.main_frame, bg = "aliceblue")
        stats_frame.pack(pady = 30)
        self.create_stats_card(stats_frame,"📦", "Total Items", len(student.inventory) )

        #quick action buttons
        Label(self.main_frame, text = "Quick Actions",font = ("Garamond",20,"bold"),bg = "aliceblue",fg = "midnightblue").pack(pady = 15)
        buttonframe = Frame(self.main_frame, bg = "aliceblue")
        buttonframe.pack(pady = 20)
        self.create_button(buttonframe,"📦 Manage Your Inventory", self.show_inventory,20)
        self.create_button(buttonframe, "🔔 Notifications", self.show_notifications,20)
        self.create_button(buttonframe, "🚨 Report an Incident", self.show_reports,20)
        self.create_button(buttonframe,  "Logout",  self.logout,20)

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

        buttonframe = Frame(self.main_frame, bg = "aliceblue")
        buttonframe.pack(pady = 20)
        self.create_button(buttonframe, "Add an Item", self.add_item)
        self.create_button(self.main_frame,  "Remove an Item", self.delete_item)
        self.create_button(buttonframe,"Return to Dashboard", self.show_home)

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

        def clear_fields():
            nameentry.delete(0,END)
            identry.delete(0,END)
            dueentry.delete(0,END)
        

        def save_item():
            item_name = nameentry.get().strip()
            item_id = identry.get().strip()
            due_date = dueentry.get().strip()
            #checking for empty fields
            if not item_name or not item_id or not due_date:
                messagebox.showwarning("Missing Informaiton","Please complete all fields.")
                return
            #checking for valid date time
            try:
                valid_date = datetime.strptime(due_date,"%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Invalid Date","Please enter a valid date in DD/MM/YYYY format.")
                return
            #checking that the date has not already passed
            if valid_date.date()<datetime.now().date():
                messagebox.showerror("Invalid Date","The due date cannot be in the past.")
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

        buttonframe = Frame(addwindow, bg = "aliceblue")
        buttonframe.pack(pady = 20)
        self.create_button(buttonframe, "Clear Fields",clear_fields,20)
        self.create_button(buttonframe, "Save Item", save_item,20).pack(pady = 20)
        self.create_button(buttonframe,"Cancel", addwindow.destroy,20)

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

    def show_notifications(self):
        self.clear_main_frame()
        self.clear_footer()

        Label(self.main_frame, text = "Notifications",font = ("Garamond",28,"bold"),bg = "aliceblue",fg = "midnightblue").pack(pady =30)
        if len(self.current_student.notifications) == 0:
            Label(self.main_frame, text = "You have no new notifications.", bg = "aliceblue").pack(pady=20)
        else:
            for notification in self.current_student.notifications:
                if not notification.read:
                    Label(self.main_frame, text = f"⚠ {notification.message}",bg = "white",width = 60, pady = 10).pack(pady = 5)


        Button(self.main_frame, text = "Return to Dashboard", command = self.show_home).pack(pady = 20)

    def check_notifications(self):
        student = self.current_student
        for item in student.inventory:
            try:
                due_date = datetime.strptime(item["Due Date"],"%d/%m/%Y")
            except ValueError:
                continue
            if due_date.date() < datetime.now().date():
                message = (
                    f"Your item '{item["Name"]}'"
                    f"is overdue."
                    f"It was due on {item["Due Date"]}."
                )
                #check if this notification already exists
                notification_exists = False
                for notification in student.notifications:
                    if notification.message == message:
                        notification_exists = True
                        break
                if not notification_exists:
                    notification = Notification(message, "Overdue")
                    student.add_notification(notification)
                    email_sent = send_email(student.email,"Inventory Management Alert",message)

    def show_teacher_dashboard(self):
        self.clear_main_frame()
        self.clear_footer()

        Label(self.main_frame, text = "Teacher Dashboard", font = ("Garamond",28,"bold"), bg = "aliceblue",fg = "midnightblue").pack(pady = 30)
        teacher = self.current_user
        trends = teacher.analyse_trends(self.students, self.reports)
        Label(self.main_frame, text = f"Total Students: {trends["Students"]}",bg = "aliceblue").pack(pady = 10)
        Label(self.main_frame, text = f"Total Items: {trends["Items"]}",bg = "aliceblue").pack(pady = 10)
        Label(self.main_frame, text = f"Incident Reports: {trends["Reports"]}",bg = "aliceblue").pack(pady = 10)
        

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