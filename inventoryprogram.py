#Inventory Program Version 1
students = {} #key = student ID, value = inventory item
reports = [] #stores all incident reports

#Student Class, represents the student and their inventory items
class Student:
    def __init__(self, student_id):
        self.student_id = student_id #stores student ID number
        self.inventory = [] #stores inventory items for this student

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
            print(f"Name: {item['Name']}")
            print(f"ID Number: {item['ID Number']}")
            print(f"Due Date: {item['Due Date']}")
            print("---------------------------") 

# logging a student into this inventory system            
def login():
    while True:
        #asking user for their student id
        student_id_str = input("Enter your Student ID: ")

        #validating that the ID contains at least 5 digits
        if student_id_str.isdigit() and len(student_id_str) == 5:
            student_id = int(student_id_str)
            break
        else:
            print("Invalid! Please enter a 5-digit Student ID.")

    #if the student doesn't exist, a new Student object is created
    if student_id not in students:
        students[student_id] = Student(student_id) 

    #return the Student object for the current logged-in student
    return students[student_id]

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

#main program
print("\n------------- Inventory Management -------------")

#logs in the first user when the program starts
current_student = login()

#keep displaying menu until the user wants to exit
while True:
    print("\n-------------- Main Menu --------------")
    print("1. Add Item")
    print("2. View Inventory")
    print("3. Report Incident")
    print("4. Switch User")
    print("5. Exit")

    #asking the user which function they want to use
    choice = input("Choose an option: ")
    #adding item to current student's inventory
    if choice == "1":
        current_student.add_item()
    #viewing current student's inventory
    elif choice == "2":
        current_student.view_inventory()
    #submit a report
    elif choice == "3":
        report_incident()
    #logging in as a different student
    elif choice == "4":
        current_student = login()
    #end the program
    elif choice == "5":
        print("Goodbye!")
        break
    #handles menu choices that are not between 1-5
    else:
        print("Invalid option.")
