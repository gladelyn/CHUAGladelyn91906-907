#Inventory Program Version 4 (GUI + Aesthetic and Interactive Features)
#import libraries 
from tkinter import* #GUI
from tkinter import messagebox #GUI
from datetime import datetime #date validation
import smtplib #email notifications
from email.message import EmailMessage #email notifications
import json #JSON file storage
import hashlib #password encryption

#inventory items class (storing information about items stored by students)
#contains methods allowing their inventory to be edited
class InventoryItem:
    def __init__(self, name, item_id, due_date):
        self.name = name
        self.item_id = item_id
        self.due_date = due_date
        self.status = "Stored"

    #changing the item's status when it has been reported as missing
    def mark_as_missing(self):
        self.status = "Missing"

    #changing the item's status when it has been returned
    def mark_as_returned(self):
        self.status = "Returned"

    #checking whether the item's due date has passed
    def check_overdue(self):
        try:
            due_date = datetime.strptime(self.due_date,"%d/%m/%Y")
            if datetime.now() >due_date:
                self.status = "Overdue"
                return True
        except ValueError:
            #returning as false if the date is not stored in the valid format
            return False
        return False


#User class (generic parent class which has all the attributes for teacher and student)
class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

#student class (inherits attributes from the user class)
#their specific attributes include student ID, inventory, notifications
class Student(User):
    def __init__(self, student_id, email, name, password):
        User.__init__(self,name,email,password)
        self.student_id = student_id
        self.inventory = []
        self.notifications = []

    #adding a new item to inventory
    def add_item(self, item):
        self.inventory.append(item)

    #removing an item from the inventory using its list index
    def delete_item(self, index):
        if 0<= index <len(self.inventory):
            return self.inventory.pop(index)
        return None

    #adding a new notification to the student's notification list
    def add_notification(self, notification):
        self.notifications.append(notification)

#teacher class inherits the attributes from the User class
#teachers will have access to system wide information and trends analysis
class Teacher(User):
    def __init__(self, teachercode, name, email, password):
        User.__init__(self,name, email, password)
        self.teachercode = teachercode

    #function to analyse information across all registered students to provide useful statistics
    def analyse_trends(self, students, reports):
        #counting the total number of registered students
        total_students = len(students)
        #counting the total number of inventory items logged
        total_items = 0

        for student in students.values():
            total_items += len(student.inventory)
        #counting the total number of incident reports submitted
        total_reports = len(reports)
        #counting the number of overdue items
        total_overdue = 0
        for student in students.values():
            for item in student.inventory:
                try:
                    due_date = datetime.strptime(item["Due Date"], "%d/%m/%Y")
                    if due_date.date() < datetime.now().date():
                        total_overdue +=1
                except ValueError:
                    #ignoring items whose due date is invalid
                    continue 
        #find the most common incident type
        incident_types = {}
        for report in reports:
            incident_type = report["Type of Incident"]
            #increasing the count when this incident type exists
            if incident_type in incident_types:
                incident_types[incident_type]+=1
            #otherwise, a new entry for the incident type is created
            else:
                incident_types[incident_type] =1

        #finding the incident type with the highest number of reports
        most_common_incident = "None"
        if incident_types:
            most_common_incident = max(incident_types, key = incident_types.get)

        #find most common location
        locations = {}
        for report in reports:
            location = report["Location"]
            if location in locations:
                locations[location]+=1
            else:
                locations[location] = 1

        #finds the location with the highest number of incidents
        most_common_location = "None"
        if locations:
            most_common_location = max(locations, key = locations.get)

        #returns all calculated statistics to be displayed on the teacher dashboard
        return {
            "Students":total_students,
            "Items":total_items,
            "Reports":total_reports,
            "Overdue":total_overdue,
            "Common Incident": most_common_incident,
            "Common Location": most_common_location
        }
#notifications class stores messages that will be displayed to students
class Notification:
    def __init__(self, message, notification_type):
        self.message = message
        self.notification_type = notification_type
        self.read = False

    #marking a notification as read
    def mark_as_read(self):
        self.read = True
    #converting the notification object into a dictionary so it can be stored on JSON file
    def to_dictionary(self):
        return {
            "Message":self.message,
            "Type":self.notification_type,
            "Read":self.read
        }
#loading students information to students.json file
def load_students():
    try:
        with open('students.json','r') as file:
            data = json.load(file)
        students = {}
        #recreate Student objects from the data stored in JSON
        for student_id, student_data in data.items():
            student = Student(
                int(student_id),
                student_data["Email"],
                student_data["Name"],
                student_data["Password"],
            )
            #restore the student's inventory
            student.inventory = student_data["Inventory"]
            #restore previously saved notifications
            student.notifications = []
            for notification_data in student_data.get("Notifications",[]):
                notification = Notification(
                    notification_data["Message"],
                    notification_data["Type"]
                )
                notification.read = notification_data["Read"]
                student.notifications.append(notification)
            students[int(student_id)] = student
        return students
    #if the JSON file doesn't exist, start with an empty dictionary
    except FileNotFoundError:
        return {}
#loading teachers on a separate teachers.json file 
#teacher accounts are controlled by the school rather than being created through the signup page
def load_teachers():
    try:
        with open("teachers.json","r") as file:
            data = json.load(file)
        teachers = {}
        #recreates Teacher objects using information stored in JSON
        for teacher_code, teacher_data in data.items():
            teacher = Teacher(
                teacher_code,
                teacher_data["Name"],
                teacher_data["Email"],
                teacher_data["Password"]
            )
            teachers[teacher_code] = teacher
        return teachers
    #if no teacher files exists, start with no registered teachers
    except FileNotFoundError:
        return {}
#convert teacher objects into dictionaries so it can be saved on JSON
def save_teachers(teachers):
    data = {}
    for teacher_code, teacher in teachers.items():
        data[teacher_code] = {
            "Name": teacher.name,
            "Email": teacher.email,
            "Password": teacher.password
        }
    #writing the information
    with open("teachers.json","w") as file:
        json.dump(data, file, indent = 4)
#converting student objects into dictionary and save them
def save_students(students):
    data = {}
    for student_id, student in students.items():
        data[str(student_id)] = {
            "Name":student.name,
            "Email":student.email,
            "Password":student.password,
            "Inventory":student.inventory,
            #converts each notification object into dictionary before storing on JSON
            "Notifications": [
                notification.to_dictionary()
                for notification in student.notifications

            ]
        }
    with open("students.json","w") as file:
        json.dump(data,file,indent = 4)

#load previously submitted incident reports from reports.json
def load_reports():
    try:
        with open("reports.json","r") as file:
            return json.load(file)
    except FileNotFoundError:
        #start with an empty list if no reports have been submitted
        return []

#save the current list of incident reports to JSON
def save_reports(reports):
    with open("reports.json","w") as file:
        json.dump(reports, file, indent = 4)

#hash passwords using SHA-256 before they are stored or compared
#keeps original password private
def hash_pswd(password):
    return hashlib.sha256(password.encode()).hexdigest()

#sending email notification to a student for overdue items
def send_email(recipient, subject, message):
    try:
        email = EmailMessage()
        email["Subject"] = subject
        email["From"] = "YOUR_SYSTEM_EMAIL"
        email["To"] = recipient
        email.set_content(message)

        #email server connection
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.send_message(email)
        server.quit()
        return True
    except Exception:
        #return false if the email could not be sent
        return False

#inventory main app class
#controls the GUI and connects different classes and functions together
class InventoryApp:

    def __init__(self, root):
        #configuring main application window
        self.root = root
        self.root.title("Inventory Management System")
        self.root.state("zoomed")
        self.root.configure(bg="aliceblue" )
        #store and load current student or current teacher data
        self.students = load_students()
        self.current_student = None
        self.teachers = load_teachers()
        self.current_teacher = None
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

    #removing all widgets from main frame before displaying new page
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    #removing all widgets from the footer before displaying a new page
    def clear_footer(self):
        for widget in self.footer_frame.winfo_children():
            widget.destroy()

    #creates a reusable button design so buttons across the program have a consistent appearance
    def create_button(self,parent, text, command, width = 20):
        button = Button(parent, text= text, width = width, height =2, bg = "midnightblue",fg = "white",activebackground = "lightskyblue1",activeforeground = "midnightblue",command = command)
        button.pack(side = LEFT, padx = 8)
        return button

    #display the login page 
    #users can choose between student or teacher account
    def show_login(self):
        self.clear_main_frame()
        self.clear_footer()

        Label(self.main_frame,text="LOGIN",font=("Garamond", 28, "bold"),bg="aliceblue",fg="midnightblue").pack(pady=40)

        #stores selected account type so the login function can search between either students.json or teachers.json
        account_type = StringVar()
        account_type.set("Student")
        Label(self.main_frame, text = "Account Type", font = ("Calibri",12),bg = "aliceblue").pack()
        Radiobutton(self.main_frame, text = "Student", variable = account_type, value = "Student", bg = "aliceblue").pack()
        Radiobutton(self.main_frame, text = "Teacher",variable = account_type, value = "Teacher", bg = "aliceblue").pack()
        Label(self.main_frame,text="Student ID/Teacher Code",font=("Calibri", 12),bg="aliceblue").pack()
        identry = Entry(self.main_frame, width = 30)
        identry.pack(pady = 10)
        Label(self.main_frame,text="Password",font=("Calibri", 12),bg="aliceblue").pack()
        pswdentry = Entry(self.main_frame, width = 30, show = "*")
        pswdentry.pack(pady =10)
        def login():
            #get and remove unnecessary spaces from the entered details
            login_id = identry.get().strip()
            password = pswdentry.get()
            #checking for empty fields
            if not login_id or not password:
                messagebox.showwarning("Missing Information","Please enter your Student ID/Teacher Code and password.")
                return

            #teacher login uses teacher code stored in teachers.json
            if account_type.get() == "Teacher":
                #validating teacher code is 3 letters
                if len(login_id)!=3 or not login_id.isalpha():
                    messagebox.showerror("Invalid Teacher Code","Teacher code must be 3 letters")
                    return
                #convert the code to uppercase so teacher codes are entered consistently
                login_id = login_id.upper()
                #check whether this code exists in teachers.json
                if login_id not in self.teachers:
                    messagebox.showerror("Login Failed", "Teacher code does not exist")
                    return
                #retrieve the matching Teacher object
                teacher = self.teachers[login_id]
                #hashing the password and comparing with one stored on JSON file
                if hash_pswd(password)!= teacher.password:
                    messagebox.showerror("Login Failed","Incorrect Password, please try again")
                    return
                #store the current logged in teacher
                #remove any previously stored student session
                self.current_teacher  = teacher
                self.current_student = None
                #open the teacher dashboard after successful login
                self.show_teacher_dashboard()
            #student login uses 5-digit ID
            else:
                #validating the student id
                if not login_id.isdigit() or len(login_id) !=5:
                    messagebox.showerror("Invalid Student ID","Student ID must be 5 digits.")
                    return
                student_id = int(login_id)
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
                self.current_teacher = None
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
        self.create_button(buttonframe, "Exit Program",self.exit_program,20)

        
        self.create_footer()

    #display the student account sign up page
    #teachers dont need to use this page becase their accounts are pre-created by the school in teachers.json
    def show_signup(self):
        self.clear_main_frame()
        self.clear_footer()
        Label(self.main_frame,text="CREATE ACCOUNT",font=("Garamond", 28, "bold"),bg="aliceblue",fg="midnightblue").pack(pady=50)  
        Label(self.main_frame, text = "Full Name", bg = "aliceblue").pack()
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
            #retrieve information entered by student
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
            student = Student(student_id,email, name,hash_pswd(password))
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

    #display the incident reporting page for students
    def show_reports(self):
            self.clear_main_frame()
            self.clear_footer()
            student = self.current_student
    
            Label(self.main_frame, text = "Report an Incident",font = ("Garamond",28,"bold"),bg = "aliceblue", fg = "midnightblue").pack(pady = 30)
            Label(self.main_frame, text = "Location",bg ="aliceblue").pack()
            locentry = Entry(self.main_frame, width = 30)
            locentry.pack(pady =10)
            Label(self.main_frame, text = "Incident Type", bg = "aliceblue").pack()
            incentry = Entry(self.main_frame, width = 30)
            incentry.pack(pady = 10)
            Label(self.main_frame, text = "Description of Incident (optional)", bg ="aliceblue").pack()
            descentry = Text(self.main_frame, width = 40, height = 5)
            descentry.pack(pady = 10)
    
            def submit_report():
                #collect the location, incident type, and optional description entered by the student
                location = locentry.get().strip()
                incident_type = incentry.get().strip()
                description = descentry.get("1.0",END).strip()
                #checking for empty fields
                if not location or not incident_type:
                    messagebox.showwarning("Missing Information","Please complete all fields.")
                    return
                #create a report dictionary so it can be saved in reports.json and used by teachers
                report = {
                    "Location":location,
                    "Type of Incident":incident_type,
                    "Description":description,
                    "Student ID":self.current_student.student_id,
                }
                #add and save report
                self.reports.append(report)
                save_reports(self.reports)
                messagebox.showinfo("Report Submitted","Your incident report has been submitted successfully.")
                self.show_home()
    
            def clear_fields():
                locentry.delete(0,END)
                incentry.delete(0,END)
    
            buttonframe = Frame(self.main_frame, bg = "aliceblue")
            buttonframe.pack(pady = 20)
            self.create_button(buttonframe, "Clear Fields",clear_fields,20)
            self.create_button(buttonframe, "Submit Report",submit_report,20)
            self.create_button(buttonframe, "Return to Dashboard",self.show_home,20)
    
    #display the main dashboard for the currently logged in student
    def show_home(self):
        self.clear_main_frame()
        self.clear_footer()
        #check for newly overdue items whenever the dashboard opens
        self.check_notifications()
        student = self.current_student

        Label(self.main_frame, text = f"Welcome, {student.name}", font = ("Garamond", 28, "bold"),bg = "aliceblue",fg = "midnightblue").pack(pady = 30)
        Label(self.main_frame, text = "Inventory Dashboard", font = ("Calibri",14),bg = "aliceblue").pack()
        stats_frame = Frame(self.main_frame, bg = "aliceblue")
        stats_frame.pack(pady = 30)
        self.create_stat_card(stats_frame,"📦", "Total Items", len(student.inventory) )

        #quick action buttons
        Label(self.main_frame, text = "Quick Actions",font = ("Garamond",20,"bold"),bg = "aliceblue",fg = "midnightblue").pack(pady = 15)
        buttonframe = Frame(self.main_frame, bg = "aliceblue")
        buttonframe.pack(pady = 20)
        Button(buttonframe,text ="📦 Manage Your Inventory", command = self.show_inventory,width =20, bg = "midnightblue", fg = "snow", activebackground = "lightskyblue1", activeforeground = "midnightblue").pack(side = LEFT, padx = 8)
        Button(buttonframe,text =  "🔔 Notifications", command = self.show_notifications,width =20,bg = "midnightblue",fg = "snow",activebackground = "lightskyblue1",activeforeground = "midnightblue").pack(side = LEFT, padx = 8)
        Button(buttonframe, text ="🚨 Report an Incident", command = self.show_reports,width =20,bg = "midnightblue",fg = "snow",activebackground = "lightskyblue1",activeforeground = "midnightblue").pack(side = LEFT, padx = 8)
        Button(buttonframe, text = "Logout", command = self.logout,width =20,bg = "midnightblue",fg = "snow",activebackground = "lightskyblue1",activeforeground = "midnightblue").pack(side =LEFT, padx = 8)

    #display all inventory items belonging to this current student
    def show_inventory(self):
        self.clear_main_frame()
        self.clear_footer()
        student = self.current_student

        Label(self.main_frame, text = "My Inventory", font = ("Garamond",28,"bold"),bg = "aliceblue",fg = "midnightblue").pack(pady =25)
        Label(self.main_frame, text = f"{student.name}'s stored items",font = ("Calibri",13),bg = "aliceblue").pack(pady = 5)

        #search and filter controls to easily navigate inventory
        search_frame = Frame(self.main_frame, bg ="aliceble")
        search_frame.pack(pady = 15)
        Label(search_frame, text = "Search Inventory:", bg ="aliceblue").pack(side = LEFT, padx = 5)
        searchentry = Entry(search_frame, width = 25)
        searchentry.pack(side = LEFT, padx = 5)
        Label(search_frame, text = "Status", bg = "aliceblue").pack(side = LEFT, padx = 5)

        #variable to store selected filter
        status_filter = StringVar()
        status_filter.set("All")
        status_options = [
            "All",
            "Stored",
            "Overdue",
            "Missing",
            "Returned"
        ]
        OptionMenu(search_frame, status_filter, *status_options).pack(side = LEFT, padx = 5)

        #a frame where the inventory items will be displayed
        inventoryframe = Frame(self.main_frame, bg = "aliceblue")
        inventoryframe.pack(fill = BOTH, expand = True, padx = 50, pady = 20)

        def display_inventory():
            #clearing the previous inventory display
            for widget in inventoryframe.winfo_children():
                widget.destroy()
            #get the user's search input
            search_text = searchentry.get().strip().lower()
            #get the user's selected status filter
            selected_status = status_filter.get()
            #table headings
            Label(inventoryframe, text = "Item Name", font = ("Garamond",13,"bold"),bg = "aliceblue").grid(row = 0,column = 0,padx =20,pady = 10)
            Label(inventoryframe, text = "ID Number",font = ("Garamond",13,"bold"),bg = "aliceblue").grid(row =0, column = 1, padx =20, pady = 10)
            Label(inventoryframe, text = "Due Date", font = ("Garamond",13,"bold"),bg = "aliceblue").grid(row = 0,column = 2, padx = 20, pady = 10)
            Label(inventoryframe, text = "Status", font = ("Garamond",13,"bold"),bg = "aliceblue").grid(row = 0,column =3, padx =20, pady =10)

            displayed_items = []

            #check every item against the search and filter
            for item in student.inventory:
                item_name = item["Name"].lower()
                item_status = item.get("Status", "Stored")
                #check whether item matches the search
                matches_search = (
                    search_text in item_name or search_text in item["ID Number"].lower()
                )
                #check whether the item matches selected status
                matches_status = (
                    selected_status == "All" or item_status == selected_status
                )
                if matches_search and matches_status:
                    displayed_items.append(item)

            #display a message if there are no matching items
            if len(displayed_items) == 0:
                Label(inventoryframe, text = "No matching items found.",font = ("Calibri",12), bg = "aliceblue").grid(row = 1,column = 0, columnspan = 4,pady = 30)
            else:
                #display each matching item
                for index, item in enumerate(displayed_items):
                    Label(inventoryframe, text = item["Name"],bg = "white",width = 20).grid(row = index+1, column = 0, padx = 10, pady = 5)
                    Label(inventoryframe, text = item["ID Number"],bg = "white",width = 20).grid(row = index+1, column = 1, padx = 10, pady = 5)
                    Label(inventoryframe, text = item["Due Date"], bg = "white",width = 20).grid(row = index+1, column = 2, padx = 10, pady = 5)
                    Label(inventoryframe, text = item.get("Status","Stored"),bg = "white",width = 20).grid(row = index+1, column = 3, padx = 10, pady =5)

        #update the inventory whenever the search text changes
        searchentry.bind("<KeyRelease>",lambda event:display_inventory())
        #update the inventory whenever status filter changes
        status_filter.trace_add(
            "write",lambda *args: display_inventory()
        )

        #display inventory when the page first opens
        display_inventory()
        #inventory action buttons
        buttonframe = Frame(self.main_frame, bg = "aliceblue")
        buttonframe.pack(pady = 20)
        self.create_button(buttonframe, "Add an Item", self.add_item)
        self.create_button(buttonframe,  "Remove an Item", self.delete_item)
        self.create_button(buttonframe,"Return to Dashboard", self.show_home)
       

    #open a pop-up window so the student can enter an inventory item
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
            #checking for valid date format
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
                "Due Date": due_date,
                "Status":"Stored"
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

    #allow the student to select and remove an item from their inventory
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

        #display each inventory item with a number so the user can easily select the item they wish to remove
        for index, item in enumerate(student.inventory):
            Label(deletewindow, text = f"{index+1}.{item["Name"]}"f"({item["ID Number"]})",bg = "aliceblue").pack(pady = 3)

        indexentry = Entry(deletewindow, width = 20)
        indexentry.pack(pady = 15)

        def confirm_delete():
            index_text = indexentry.get().strip()
            #validate that the user entered a number
            if not index_text.isdigit():
                messagebox.showerror("Invalid Input","Please enter a valid item number from the list.")
                return
            #convert the displayed number into the correct, corresponding python list index
            index = int(index_text) - 1
            if index < 0 or index >= len(student.inventory):
                messagebox.showerror("Invalid Item","That item number does not exist")
                return

            item_name = student.inventory[index]["Name"]
            #asking the user to confirm before permanently removing the item
            confirmation = messagebox.askyesno("Confirm Delete",f"Are you sure you want to remove "f"'{item_name}'?")
            if confirmation:
                #remove the selected item and save the new inventory
                student.delete_item(index)
                save_students(self.students)
                messagebox.showinfo("Item Deleted","Item Successfully Removed")
                deletewindow.destroy()
                self.show_inventory()

        Button(deletewindow, text = "Remove", width =20, command = confirm_delete).pack(pady = 10)
        Button(deletewindow, text = "Cancel", width = 20, command = deletewindow.destroy).pack()

    #display notifications belonging to the currently logged in student
    def show_notifications(self):
        self.clear_main_frame()
        self.clear_footer()

        Label(self.main_frame, text = "Notifications",font = ("Garamond",28,"bold"),bg = "aliceblue",fg = "midnightblue").pack(pady =30)

        #count the number of unread notifications
        unread_count = 0
        for notification in self.current_student.notifications:
            if not notification.read:
                unread_count +=1
        Label(self.main_frame, text = f"You have {unread_count} unread notification(s).", bg = "aliceblue",font = ("Calibri",12)).pack(pady = 5)
        if len(self.current_student.notifications) == 0:
            Label(self.main_frame, text = "You have no new notifications.", bg = "aliceblue").pack(pady=20)
        else:
            #only display the unread notifications to the student
            for notification in self.current_student.notifications:
                notification_frame = Frame(self.main_frame, bg ="white",bd = 1,relief = "solid")
                notification_frame.pack(pady = 5, padx = 100, fill = X)
                #display the notification message
                Label(
                    notification_frame, text = f"⚠ {notification.message}", bg = "white", wraplength = 600).pack(side = LEFT, padx = 15, pady = 15)
                #only show the button for unread notifications
                if not notification.read:
                    def mark_read(n = notification):
                        #mark the selected notification as read
                        n.mark_as_read()
                        #save updated notification status
                        save_students(self.students)
                        #refresh notification page
                        self.show_notifications()

                    Button(notification_frame, text = "Mark as Read",command = mark_read).pack(side = RIGHT, padx = 15)
                else:
                    Label(notification_frame, text = "✓ Read",bg = "white").pack(side = RIGHT, padx = 15)

        Button(self.main_frame, text = "Return to Dashboard",command = self.show_home).pack(pady = 20)


        Button(self.main_frame, text = "Return to Dashboard", command = self.show_home).pack(pady = 20)

    #check for overdue items and create a notification when overdue
    def check_notifications(self):
        student = self.current_student
        for item in student.inventory:
            try:
                due_date = datetime.strptime(item["Due Date"],"%d/%m/%Y")
            except ValueError:
                continue
            #compare the item's due date to today's date
            if due_date.date() < datetime.now().date():
                #update the item's status when its due date has passed
                item["Status"] = "Overdue"
                #create a message containing the item's name and due date
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
                #create and save the notification if it doesn't exist
                if not notification_exists:
                    notification = Notification(message, "Overdue")
                    student.add_notification(notification)
                    #attempt to notify the student by email
                    email_sent = send_email(student.email,"Inventory Management Alert",message)
                    save_students(self.students)

    #display the teacher dashboard showing statistics and report trends
    def show_teacher_dashboard(self):
        self.clear_main_frame()
        self.clear_footer()

        Label(self.main_frame, text = "Teacher Dashboard", font = ("Garamond",28,"bold"), bg = "aliceblue",fg = "midnightblue").pack(pady = 30)
        #analyse the current student and incident report data
        teacher = self.current_teacher
        trends = teacher.analyse_trends(self.students, self.reports)
        #display the calculated statistics so teacher can see the patterns
        Label(self.main_frame, text = "Inventory Insights",font = ("Garamond",20,"bold"),bg ="aliceblue",fg = "midnightblue").pack(pady=20)
        Label(self.main_frame, text = f"Total Students: {trends["Students"]}",bg = "aliceblue").pack(pady = 10)
        Label(self.main_frame, text = f"Total Items: {trends["Items"]}",bg = "aliceblue").pack(pady = 10)
        Label(self.main_frame, text = f"Incident Reports: {trends["Reports"]}",bg = "aliceblue").pack(pady = 10)
        Label(self.main_frame,text = f"Overdue Items: {trends["Overdue"]}",bg = "aliceblue").pack(pady =10)
        Label(self.main_frame, text = f"Most Common Incident: {trends["Common Incident"]}",bg = "aliceblue").pack(pady = 5)
        Label(self.main_frame, text = f"Most Common Location: {trends["Common Location"]}",bg = "aliceblue").pack(pady = 5)

        #generate a recommended action based on trends
        #this turns collected data into useful information that the teacher can use to take appropriate action
        if trends["Overdue"]>0:
            action = (
                "Consider reminding students about due dates and review the returning process"
            )
        #if there are many incident reports, recommend investigating the locations where they occur
        elif trends["Reports"]>=5:
            action=("Consider reviewing the areas where incidents are occurring most frequently.")
        #else, display a general message when there are only a few issues requiring teacher attention
        else:
            action = ("Inventory records are currently showing very few issues to discuss.")

        Label(self.main_frame, text = "Recommended Action", font = ("Garamond",18,"bold"),bg = "aliceblue",fg = "midnightblue").pack(pady = 15)
        Label(self.main_frame,text = action, wraplength = 700, bg = "white", padx = 20, pady = 15).pack()
        
        buttonframe = Frame(self.main_frame, bg = "aliceblue")
        buttonframe.pack(pady =20)
        self.create_button(buttonframe, "Logout",self.logout,20)
        
    #create a reusable card to display statistics on the dashboard
    def create_stat_card(self, parent, icon, title, value):
        card = Frame(parent, bg = "white", bd = 1, relief = "solid",width = 220, height = 130)
        card.pack(side = LEFT, padx =10)
        card.pack_propagate(False)
        Label(card, text = icon, font = ("Segoe UI Emoji", 25), bg = "white").pack(pady = 5)
        Label(card, text = title, font = ("Garamond",13,"bold"),bg = "white").pack()
        Label(card, text = value, font = ("Garamond",20,"bold"),bg ="white").pack()

    #clearing the current user and return to login page
    def logout(self):
        self.current_student = None
        self.current_teacer = None
        self.show_login()

    #asking user for confirmation before fully closing program
    def exit_program(self):
        answer = messagebox.askyesno("Exit Program","Are you sure you want to exit?")
        if answer:
            #save all information stored in the session before closing
            save_students(self.students)
            save_reports(self.reports)
            #close the application window
            self.root.destroy()

    #create reusable information cards for login/signup pages
    #these introduce the main features of the system
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
#generating the main Tkinter window
root = Tk()
#create an instance of InventoryApp and pass the window into it
app = InventoryApp(root)
#make the window's close button use the same exit procedure so that data is saved before closed
root.protocol("WM_DELETE_WINDOW",app.exit_program)
#keep the GUI running and responsive until user exits program
root.mainloop()