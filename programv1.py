#isbn number on textbook barcode, encryption similar to indexed order
#eg. instead of food[0], it could be like food[1234567]
#Storage Structures

students = {}      # key  = student id, value = inventory item
reports = []       # Stores all incident reports

#Student Class

class Student:

    def __init__(self, student_id):
        self.student_id = student_id
        self.inventory = []

    def add_item(self):

        item_name = input("Enter the item name: ")
        item_id = input(f"Enter the ID number of '{item_name}': ")
        due_date = input("Enter the due date of the item: ")

        item = {
            "Name": item_name,
            "ID Number": item_id,
            "Due Date": due_date
        }

        self.inventory.append(item)

        print("Item successfully stored.\n")

    def view_inventory(self):

        if len(self.inventory) == 0:
            print("No items have been stored.\n")
            return

        print("\n----- Inventory -----")

        for item in self.inventory:
            print(f"Name: {item['Name']}")
            print(f"ID Number: {item['ID Number']}")
            print(f"Due Date: {item['Due Date']}")
            print("---------------------------")



def login():

    while True:

        student_id_str = input("Enter your Student ID: ")

        if student_id_str.isdigit() and len(student_id_str) == 5:

            student_id = int(student_id_str)

            break

        else:
            print("Invalid! Please enter a 5-digit Student ID.")

    if student_id not in students:
        students[student_id] = Student(student_id)

    return students[student_id]



def report_incident():

    location = input("Enter the location: ")
    incident_type = input("Incident type (theft/missing): ")
    student_id = input("Enter your Student ID: ")

    report = {
        "Location": location,
        "Type of Incident": incident_type,
        "Student ID": student_id
    }

    reports.append(report)

    print("Report submitted successfully.\n")


#main

print("\n------------- Inventory Management -------------")

current_student = login()

while True:

    print("\n-------------- Main Menu --------------")
    print("1. Add Item")
    print("2. View Inventory")
    print("3. Report Incident")
    print("4. Switch User")
    print("5. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        current_student.add_item()

    elif choice == "2":
        current_student.view_inventory()

    elif choice == "3":
        report_incident()

    elif choice == "4":
        current_student = login()

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid option.")



''' Main improvements for next version
- more visually appealing so use tkinter or easygui as my second version
- creating a trends report page that analyses all the reports stored in the system
- maybe appending the data into a text/json file so that it doesn't clear when i close the window
- move to more complex functionalities by using java script
- rather than manually inputting item id, open a pop-up scanner/camera to scan the barcode of things like textbooks
'''
