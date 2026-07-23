#isbn number on textbook barcode, encryption similar to indexed order
#eg. instead of food[0], it could be like food[1234567]

#a set is unordered and mutable
'''a = {1,2,3}
b = {4,5,6}
c = a|b
print(c)'''



#inventory and reports containers, however beginning it with an empty container means data will be lost after window is closed
inventories = {}#inventory is declared as a dictionary so that the key can be a different student ID number and not a shared list
reports = [] #reports are collective and are used to make our trends report therefore kept in a list

#login function
def login():
    global student_id #made the variable global so it can be used in the other functions
    while True:
        student_id_str = input("Please enter your Student ID number: ")#started off as string so that I can find the length
        if student_id_str.isdigit() and len(student_id_str) == 5: #putting is digit (instead of VE) allows me to still spot non-int values
        #since bdsc id numbers are always 5digits i wanted to enhance security by ensuring the id number inputted is within the range
            student_id = int(student_id_str) #i then converted it back into an integer as it was initially a string
            break
        else:
            print("Invalid! Please enter your ID as a 6-digit number")
    if student_id not in inventories:
        inventories[student_id] = [] #if the student hasn't logged in the system before, the system creates a new inventory within the dictionary
        return student_id 

#inventory functions
def add_item():
    item_name = input("Enter the item name: ")
    item_ID = input(f"Enter the ID number of '{item_name}': ") #i kept the item ID as a string input because some barcodes have letters
    due_date = input("Please enter the due date of the item:" )

    item = { #this dictionary stores all the info relating to the item user wishes to store
        "Name": item_name,
        "ID Number": item_ID,
        "Due Date": due_date
        }

    inventories[student_id].append(item)

    print("Item has been successfully stored\n")

def view_inventory():
    if len(inventories[student_id]) == 0:
        print("No items have been stored in your inventory\n")
        return

    print("\n---Inventory---")
    for item in inventories[student_id]:
        print(f"Name: {item["Name"]}")
        print(f"ID Number: {item["ID Number"]}")
        print(f"Due Date: {item["Due Date"]}")
        print("------------------------------------")

def report_incident():
    location = input("Enter the location of the incident: ")
    incident_type = input("Incident type (theft/missing): ")
    student_id = input("Enter your ID number: ")

    report = {
        "Location": location,
        "Type of Incident": incident_type,
        "Student ID":student_id
        }
    reports.append(report) 

    print("Your report has been submitted successfully\n")

print("\n--------------------Management---------------------")

current_user = login() #put the login first because it must be defined first as the functions following relate to that specific ID

while True:
    print("\n--------------------Main Menu---------------------")
    print("1. Add Item")
    print("2.View inventory")
    print("3. Report Incident")
    #next version will have a trends option which analyses the data in the reports list
    print("4. Switch User")
    print("5. Exit")

    choice = input("Choose an option (1/2/3/4/5): ")
    if choice == "1":
        add_item()
    elif choice == "2":
        view_inventory()
    elif choice == "3":
        report_incident()
    elif choice == "4":
        current_user = login() #repeat the same function call for a new user to sign in
    elif choice == "5":
        print("Goodbye!")
        break
    else:
        print("Invalid Option, please choose one of (1/2/3/4/5)")




''' Main improvements for next version
- more visually appealing so use tkinter or easygui as my second version
- creating a trends report page that analyses all the reports stored in the system
- maybe appending the data into a text/json file so that it doesn't clear when i close the window
- move to more complex functionalities by using java script
- rather than manually inputting item id, open a pop-up scanner/camera to scan the barcode of things like textbooks
'''
