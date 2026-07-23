#program tkinter
from tkinter import*
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk

class User:
    def __init__(self, studentid, firstname, lastname, email, password):
        self.studentid = studentid
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

users={}

root = Tk()
root.title("Inventory Program")
root.state("zoomed")

titleframe = Frame(root, bg = "midnightblue", height = 100)
titleframe.pack(fill = X)
Label(titleframe, text = "Inventory Program", font = ("Garamond", 20,"bold"), bg = "midnightblue", fg = "snow").pack(pady = 10)

mainframe = None
footerframe = None

def start():
    global mainframe
    global footerframe
    if mainframe != None:
        mainframe.destroy()
    if footerframe != None:
        footerframe.destroy()
    mainframe = Frame(root, bg = "aliceblue")
    mainframe.pack(fill =BOTH, expand = True)
    Label(mainframe, text = "LOGIN OR SIGN UP TO OUR SERVICES",font = ("Garamond", 18, "bold"), bg = "aliceblue", fg = "midnightblue").pack(pady = 70)
    buttonframe = Frame(mainframe, bg = "aliceblue")
    buttonframe.pack()
    Button(buttonframe, text = "New\nSign Up", font = ("Garamond",18), width = 14, height = 5, bg = "midnightblue", fg = "snow", activebackground = "lightskyblue1", activeforeground = "midnightblue",command = signup).pack(side = LEFT, pady = 30,padx = 10)
    Button(buttonframe, text = "Login\nwith ID", font = ("Garamond",18), width = 14, height = 5,bg = "midnightblue", fg = "snow", activebackground = "lightskyblue1", activeforeground = "midnightblue",command = login).pack(side = LEFT, pady = 30, padx = 10)
    
    footerframe = Frame(root,bg = "snow", height = 200)
    footerframe.pack(fill = X)
    footerframe.pack_propagate(False)
    cardsframe = Frame(footerframe,bg = "snow")
    cardsframe.pack(expand = True)

    card1 = Frame(cardsframe, bg="aliceblue", bd = 1, relief = "solid", padx = 20, pady = 15)
    card1.pack(side=LEFT, padx=20, pady=20)
    Label(card1,text="📦",font=("Segoe UI Emoji", 28),bg="aliceblue",fg="midnightblue").pack()
    Label(card1,text="Pocket Inventory",font=("Garamond", 16, "bold"),bg="aliceblue",fg="midnightblue").pack(pady = (5,0))
    Label(card1,text="Keep track of\nstudent belongings.",font=("Calibri", 10),bg = "aliceblue",fg="grey26",justify="center").pack(pady=(5,0))

    card2 = Frame(cardsframe, bg="mintcream", bd=1, relief="solid", padx=20, pady=15)
    card2.pack(side=LEFT, padx=20, pady=20)
    Label(card2,text="🔒",font=("Segoe UI Emoji", 28),bg="mintcream",fg="darkslategrey").pack()
    Label(card2,text="Protected Data",font=("Garamond", 16, "bold"),bg="mintcream",fg="darkslategrey").pack(pady=(5,0))
    Label(card2,text="Secure storage\nfor all records.",font=("Calibri", 10),bg="mintcream",fg="grey26",justify="center").pack(pady=(5,0))

    card4 = Frame(cardsframe, bg="aliceblue", bd=1, relief="solid", padx=20, pady=15)
    card4.pack(side=LEFT, padx=20, pady=20)
    Label(card4,text="⚡",font=("Segoe UI Emoji", 28),bg="aliceblue",fg="midnightblue").pack()
    Label(card4,text="Easy Management",font=("Garamond", 16, "bold"),bg="aliceblue",fg="midnightblue").pack(pady=(5,0))
    Label(card4,text="Quickly manage\nall inventory items.", font=("Calibri", 10),bg="aliceblue",fg="grey26",justify="center").pack(pady=(5,0))

    card3 = Frame(cardsframe, bg="mintcream", bd=1, relief="solid", padx=20, pady=15)
    card3.pack(side=LEFT, padx=20, pady=20)
    Label(card3, text="📊",font=("Segoe UI Emoji", 28),bg="mintcream",fg="darkslategrey").pack()
    Label(card3,text="Statistical Analysis",font=("Garamond", 16, "bold"),bg="mintcream",fg="darkslategrey").pack(pady=(5,0))
    Label(card3,text="View inventory\nstatistics easily.",font=("Calibri", 10),bg="mintcream",fg="grey26",justify="center").pack(pady=(5,0))
def login():
    global mainframe
    global footerframe
    global studentid
    global password
    footerframe.destroy()
    mainframe.destroy()
    mainframe = Frame(root, bg = "aliceblue")
    mainframe.pack(fill = BOTH, expand = True)
    Label(mainframe, text = "LOGIN TO START", font = ("Garamond", 18,"bold"), bg = "aliceblue", fg = "midnightblue").pack(pady = 50)
    Label(mainframe, text = "Student ID:", font = ("Garamond",17), bg = "aliceblue", fg = "midnightblue").pack(pady = 10)
    studentid = Entry(mainframe, text = "", font = ("Garamond",17), bg = "snow", fg = "midnightblue")
    studentid.pack(pady = 10)
    Label(mainframe, text = "Password:", font = ("Garamond",17), bg = "aliceblue", fg = "midnightblue").pack(pady = 10)
    password = Entry(mainframe, text = "", font = ("Garamond",17), bg = "snow", fg = "midnightblue")
    password.pack(pady =10)

    def cleardata():
        studentid.delete(0,END)
        password.delete(0,END)

    buttonframe1 = Frame(mainframe, bg = "aliceblue")
    buttonframe1.pack()
    Button(buttonframe1, text = "New User", font = ("Garamond",17), width = 10,bg = "midnightblue", fg = "snow", activebackground = "lightskyblue1", activeforeground = "midnightblue",command = signup).pack(side = LEFT, pady =40,padx = 10)
    Button(buttonframe1, text = "Clear Data", font = ("Garamond",17), command = cleardata,width = 10, bg = "midnightblue", fg = "snow", activebackground = "lightskyblue1", activeforeground = "midnightblue").pack(side =LEFT, pady = 40,padx = 10)
    Button(buttonframe1, text = "Continue", font = ("Garamond",17), width = 10, bg = "midnightblue", fg = "snow", activebackground = "lightskyblue1", activeforeground = "midnightblue").pack(side = LEFT, pady = 40,padx =10)

    Label(mainframe, text = "Please ensure you complete all fields before submitting", font = ("Garamond",17), bg = "aliceblue", fg = "midnightblue").pack( pady =10)
    footerframe = Frame(root,bg = "snow", height = 200)
    footerframe.pack(fill = X)
    footerframe.pack_propagate(False)
    cardsframe = Frame(footerframe,bg = "snow")
    cardsframe.pack(expand = True)

    card1 = Frame(cardsframe, bg="aliceblue", bd = 1, relief = "solid", padx = 20, pady = 15)
    card1.pack(side=LEFT, padx=20, pady=20)
    Label(card1,text="📦",font=("Segoe UI Emoji", 28),bg="aliceblue",fg="midnightblue").pack()
    Label(card1,text="Pocket Inventory",font=("Garamond", 16, "bold"),bg="aliceblue",fg="midnightblue").pack(pady = (5,0))
    Label(card1,text="Keep track of\nstudent belongings.",font=("Calibri", 10),bg = "aliceblue",fg="grey26",justify="center").pack(pady=(5,0))

    card2 = Frame(cardsframe, bg="mintcream", bd=1, relief="solid", padx=20, pady=15)
    card2.pack(side=LEFT, padx=20, pady=20)
    Label(card2,text="🔒",font=("Segoe UI Emoji", 28),bg="mintcream",fg="darkslategrey").pack()
    Label(card2,text="Protected Data",font=("Garamond", 16, "bold"),bg="mintcream",fg="darkslategrey").pack(pady=(5,0))
    Label(card2,text="Secure storage\nfor all records.",font=("Calibri", 10),bg="mintcream",fg="grey26",justify="center").pack(pady=(5,0))

    card4 = Frame(cardsframe, bg="aliceblue", bd=1, relief="solid", padx=20, pady=15)
    card4.pack(side=LEFT, padx=20, pady=20)
    Label(card4,text="⚡",font=("Segoe UI Emoji", 28),bg="aliceblue",fg="midnightblue").pack()
    Label(card4,text="Easy Management",font=("Garamond", 16, "bold"),bg="aliceblue",fg="midnightblue").pack(pady=(5,0))
    Label(card4,text="Quickly manage\nall inventory items.", font=("Calibri", 10),bg="aliceblue",fg="grey26",justify="center").pack(pady=(5,0))

    card3 = Frame(cardsframe, bg="mintcream", bd=1, relief="solid", padx=20, pady=15)
    card3.pack(side=LEFT, padx=20, pady=20)
    Label(card3, text="📊",font=("Segoe UI Emoji", 28),bg="mintcream",fg="darkslategrey").pack()
    Label(card3,text="Statistical Analysis",font=("Garamond", 16, "bold"),bg="mintcream",fg="darkslategrey").pack(pady=(5,0))
    Label(card3,text="View inventory\nstatistics easily.",font=("Calibri", 10),bg="mintcream",fg="grey26",justify="center").pack(pady=(5,0))

   
def signup():
    global mainframe
    global footerframe
    global firstname
    global lastname
    global studentid
    global password
    global email
    footerframe.destroy()
    mainframe.destroy()
    mainframe = Frame(root, bg = "aliceblue")
    mainframe.pack(fill = BOTH, expand = True)
    Label(mainframe, text = "NEW USER SIGNUP", font = ("Garamond", 18, "bold"), bg = "aliceblue", fg = "midnightblue").pack(pady = 10)
    Label(mainframe, text = "First Name:", font = ("Garamond",17), bg = "aliceblue", fg = "midnightblue").pack(pady = 5)
    firstname = Entry(mainframe, text = "", font = ("Garamond",17), bg = "snow", fg = "midnightblue")
    firstname.pack(pady = 5)
    Label(mainframe, text = "Last Name:", font = ("Garamond",17), bg = "aliceblue", fg = "midnightblue").pack(pady = 5)
    lastname = Entry(mainframe, text = "", font = ("Garamond",17), bg = "snow", fg = "midnightblue")
    lastname.pack(pady = 5)
    Label(mainframe, text = "Email Address:", font = ("Garamond",17), bg ="aliceblue", fg ="midnightblue").pack(pady = 5)
    email = Entry(mainframe, text = "", font = ("Garamond",17), bg = "snow", fg = "midnightblue")
    email.pack(pady =5)
    Label(mainframe, text = "Student ID:", font = ("Garamond",17), bg = "aliceblue", fg = "midnightblue").pack(pady = 5)
    studentid = Entry(mainframe, text = "", font = ("Garamond",17), bg = "snow", fg = "midnightblue")
    studentid.pack(pady = 5)
    Label(mainframe, text = "Password:", font = ("Garamond",17), bg = "aliceblue", fg = "midnightblue").pack(pady = 5)
    password = Entry(mainframe, text = "", font = ("Garamond",17), bg = "snow", fg = "midnightblue")
    password.pack(pady = 5)

    def clear():
        firstname.delete(0,END)
        lastname.delete(0,END)
        studentid.delete(0,END)
        password.delete(0,END)
        email.delete(O,END)

    buttonframe = Frame(mainframe, bg = "aliceblue")
    buttonframe.pack()
    Button(buttonframe, text = "Back", font = ("Garamond",17), width = 10, bg = "midnightblue", fg = "snow", activebackground = "lightskyblue1", activeforeground = "midnightblue",command = start).pack(side =LEFT, pady = 10, padx = 10)
    Button(buttonframe, text = "Clear Data", font =("Garamond",17), command = clear,width = 10, bg = "midnightblue", fg = "snow", activebackground = "lightskyblue1", activeforeground = "midnightblue").pack(side = LEFT, pady =10, padx = 10)
    Button(buttonframe, text = "Sign Up", font = ("Garamond",17), width = 10, bg = "midnightblue", fg = "snow", activebackground = "lightskyblue1", activeforeground ="midnightblue", command = login).pack(side =LEFT, pady = 10, padx = 10)

    footerframe = Frame(root,bg = "snow", height = 200)
    footerframe.pack(fill = X)
    footerframe.pack_propagate(False)
    cardsframe = Frame(footerframe,bg = "snow")
    cardsframe.pack(expand = True)

    card1 = Frame(cardsframe, bg="aliceblue", bd = 1, relief = "solid", padx = 20, pady = 15)
    card1.pack(side=LEFT, padx=20, pady=20)
    Label(card1,text="📦",font=("Segoe UI Emoji", 28),bg="aliceblue",fg="midnightblue").pack()
    Label(card1,text="Pocket Inventory",font=("Garamond", 16, "bold"),bg="aliceblue",fg="midnightblue").pack(pady = (5,0))
    Label(card1,text="Keep track of\nstudent belongings.",font=("Calibri", 10),bg = "aliceblue",fg="grey26",justify="center").pack(pady=(5,0))

    card2 = Frame(cardsframe, bg="mintcream", bd=1, relief="solid", padx=20, pady=15)
    card2.pack(side=LEFT, padx=20, pady=20)
    Label(card2,text="🔒",font=("Segoe UI Emoji", 28),bg="mintcream",fg="darkslategrey").pack()
    Label(card2,text="Protected Data",font=("Garamond", 16, "bold"),bg="mintcream",fg="darkslategrey").pack(pady=(5,0))
    Label(card2,text="Secure storage\nfor all records.",font=("Calibri", 10),bg="mintcream",fg="grey26",justify="center").pack(pady=(5,0))

    card4 = Frame(cardsframe, bg="aliceblue", bd=1, relief="solid", padx=20, pady=15)
    card4.pack(side=LEFT, padx=20, pady=20)
    Label(card4,text="⚡",font=("Segoe UI Emoji", 28),bg="aliceblue",fg="midnightblue").pack()
    Label(card4,text="Easy Management",font=("Garamond", 16, "bold"),bg="aliceblue",fg="midnightblue").pack(pady=(5,0))
    Label(card4,text="Quickly manage\nall inventory items.", font=("Calibri", 10),bg="aliceblue",fg="grey26",justify="center").pack(pady=(5,0))

    card3 = Frame(cardsframe, bg="mintcream", bd=1, relief="solid", padx=20, pady=15)
    card3.pack(side=LEFT, padx=20, pady=20)
    Label(card3, text="📊",font=("Segoe UI Emoji", 28),bg="mintcream",fg="darkslategrey").pack()
    Label(card3,text="Statistical Analysis",font=("Garamond", 16, "bold"),bg="mintcream",fg="darkslategrey").pack(pady=(5,0))
    Label(card3,text="View inventory\nstatistics easily.",font=("Calibri", 10),bg="mintcream",fg="grey26",justify="center").pack(pady=(5,0))


def homepage():
    footerframe.destroy()
    mainframe.destroy()

    mainframe = Frame(root, bg = "aliceblue")

start()


root.mainloop()
