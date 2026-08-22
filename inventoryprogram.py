#external libraries
import json #for appending details to external file
import hashlib #for encryption
#Inventory Program Version 1
students = {} #key = student ID, value = inventory item
reports = [] #stores all incident reports


#encyrpted password
def hash_pswd(password):
    return hashlib.sha256(password.encode()).hexdigest()

#loading student information from students.json so that details are kept even when program is closed
def load_students():
    try:
        with open("students.json", "r") as file:
            data = json.load(file)

        #dictionary to store the Loaded Student objects
        loaded_students = {}

        #converting the saved dictionaries back into Student objects
        for student_id, student_data in data.items():

            student = Student(
                int(student_id),
                student_data["Name"],
                student_data["Email"],
                student_data["Password"]
            )

            #restore the student's inventory
            student.inventory = student_data["Inventory"]

            loaded_students[int(student_id)] = student

        #return the loaded students into the main program
        return loaded_students
    except FileNotFoundError:
        #if the file does not exist yet, return empty dictionary
        return{}

#saving student information to external JSON file
def save_students(students):
    data = {}

    #converting each Student object into dictionary
    for student_id, student in students.items():
        data[str(student_id)] = {
            "Name":student.name,
            "Email": student.email,
            "Password": student.password,
            "Inventory": student.inventory
        }

    #saving the information as JSON
    with open("students.json","w") as file:
        json.dump(data, file, indent = 4)

#loading incident reports to external JSON file
def load_reports():
    try:
        with open("reports.json","r") as file:
            reports = json.load(file)
        #return the reports that were loaded
        return reports
    except FileNotFoundError:
        #if the file does not exist, return empty list
        return []

#saving the reports to external file
def save_reports(reports):
    with open("reports.json","w") as file:
        json.dump(reports, file, indent = 4)
    

#Student Class, represents the student and their inventory items
class Student:
    def __init__(self, student_id, name, email,password):
        self.student_id = student_id #stores student ID number
        self.inventory = [] #stores inventory items for this student
        self.name = name #stores user's name as well
        self.email = email #stores user's email
        self.password = password #stores user's password

    def add_item(self): #allows this student to add items
        #getting the details of this item from user
        item_name = input("Enter the item name: ")
        item_id = input(f"Enter the ID number of '{item_name}': ")
        due_date = input("Enter the due date of the item: ")

        #stores the item information in a dictionary
        item = {
            "Name": item_name,
            "ID Number": item_id,
            "Due Date": due_date
        }

        #adding the new item to this student's inventory
        self.inventory.append(item)

        print("Item successfully stored.\n")

    
    def view_inventory(self):#displays all inventory items belonging to the current student
        #checking whether the student has any stored items
        if len(self.inventory) == 0:
            print("No items have been stored.\n")
            return

        print("\n----- Inventory -----")

        #loop through each item in the student's inventory
        for item in self.inventory:
            print(f"NameL {item['Name']}")
            print(f"ID Number: {item['ID Number']}")
            print(f"Due Date: {item['Due Date']}")
            print("---------------------------") 

    def delete_item(self):
        #check whether the inventory is already empty first
        if len(self.inventory)==0:
            print("No items have been stored.\n")
            return
        print("\n----- Inventory -----")
        #enumerate each item so the user can select which one they want to delete
        for number, item, in enumerate(self.inventory, start = 1):
            print(
                f"{number}.{item["Name"]} -ID: {item["ID Number"]}"
            )
        #validating the user's choice, because they might write the name of item instead of choosing number
        while True:
            choice = input("Enter the number of the item you want to delete: ")
            if choice.isdigit():
                choice = int(choice)
                if 1<= choice <= len(self.inventory):
                    break
            print("Invalid! Please select an item from the list based on it's number.")

        #removing the chosen item from the inventory list
        removed_item = self.inventory.pop(choice - 1)

        print(
            f"{removed_item["Name"]} has been removed from your inventory.\n"
        )

#signing up a new user
def signup(students):

    print("\n---------- Sign Up ----------")

    name = input("Enter your name: ")
    print(f"Hello {name}, welcome to the Inventory Management System.")

    #validating the student id
    while True:
        student_id_str = input("Enter your Student ID: ")
        if student_id_str.isdigit() and len(student_id_str) == 5:
            student_id = int(student_id_str)

            #check whether id exists
            if student_id not in students:
                break
            else:
                print("This Student ID is already registered.")
        else:
            print("Invalid! Please enter a 5-digit Student ID.")

    email = input("Enter your email: ")
    password = input("Enter a password: ")
    hashed_pswd = hash_pswd(password)


    #creating a new student object
    student = Student(student_id, name, email, hashed_pswd)
    #adding the student object to the dictionary
    students[student_id] = student
    print("Account successfully created.\n")

    return students, student

# logging an already signed up student into this inventory system
# this function will check whether student id exists, students dictionary is passed into the function            
def login(students):

    print("\n-------------- Log In --------------")

    while True:
        #asking user for their student id
        student_id_str = input("Enter your Student ID: ")

        #validating that the ID contains at least 5 digits
        if student_id_str.isdigit() and len(student_id_str) == 5:
            student_id = int(student_id_str)
            break
        else:
            print("Invalid! Please enter a 5-digit Student ID.")

    #if the student doesn't exist, student is redirected to sign up
    if student_id not in students:
        print("Student ID not found. Please sign up first.\n")
        return None

    #ask user for their desired password
    password = input("Enter a password: ")
    hashed_pswd = hash_pswd(password)
    #after password is hashed, compare with stored password to check whether it matches
    if students[student_id].password == hashed_pswd:
        print(f"\nWelcome Back, {students[student_id].name}")

        return students[student_id]

    else:
        print("Incorrect Password.\n")
        return None

#allows student to report a theft or missing item
def report_incident():
    #getting the details of incident from user
    location = input("Enter the location: ")
    incident_type = input("Incident Type (theft/missing): ")
    student_id = input("Enter your Student ID: ")

    #stores the incident information in a dictionary
    report = {
        "Location": location,
        "Type of Incident": incident_type,
        "Student ID": student_id
    }          

    #adding the report to the list of all incident reports to make future trends analysis
    reports.append(report)
    print("Report submitted successfully.\n")

    return reports

#main program
#loading the students and reports
students = load_students()
reports = load_reports()
print("\n------------- Inventory Management -------------")

while True:
    print("\n-------------- Sign Up or Log In --------------")
    print("1. Sign Up (new users)")
    print("2. Log In")
    print("3. Exit Program")

    choice = input("Choose an option: ")
    if choice == "1":
        #signup will return updated students dictionary and newly created student object
        #students dictionary is updated to include new account
        #current_student identifies the student who has just signed up
        students, current_student = signup(students)
        break
    elif choice == "2":
        current_student = login(students)
        if current_student is not None:
            break
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid Option. Please choose between 1-3.")

#keep displaying menu until the user wants to exit
while True:
    print("\n-------------- Main Menu --------------")
    print("1. Add Item")
    print("2. View Inventory")
    print("3. Remove Item")
    print("4. Report Incident")
    print("5. Switch User")
    print("6. Exit")

    #asking the user which function they want to use
    choice = input("Choose an option: ")
    #adding item to current student's inventory
    if choice == "1":
        current_student.add_item()
    #viewing current student's inventory
    elif choice == "2":
        current_student.view_inventory()
    #deleting item
    elif choice == "3":
        current_student.delete_item()
        #then save the updated inventory to the JSON file
        save_students(students)
    #submit a report
    elif choice == "4":
        reports = report_incident(reports)
        save_reports(reports)
    #logging in as a different student
    elif choice == "5":
        current_student = login()
    #end the program
    elif choice == "6":
        save_students(students)
        save_reports(reports)
        print("Goodbye!")
        break
    #handles menu choices that are not between 1-5
    else:
        print("Invalid option.")
