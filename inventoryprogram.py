#Inventory Program Version 3 (GUI transition)
#import libraries
from tkinter import*
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk

#inventory main app class
class InventoryApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System" )
        self.root.state("zoomed")
        self.root.configure(bg = "aliceblue")
        # Stores the frame currently being displayed
        self.current_frame = None
        self.show_start()

#clearing the current frame (reset)
    def clear_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = Frame(self.root,bg="aliceblue" )
        self.current_frame.pack(fill=BOTH,expand=True)


#start menu
    def show_start(self):
        self.clear_frame()
        Label(self.current_frame,text="INVENTORY MANAGEMENT SYSTEM",font=("Garamond", 28, "bold"),bg="aliceblue",fg="midnightblue").pack(pady=80)
        Button(self.current_frame,text="Login",font=("Garamond", 16),width=20,height=2,command=self.show_login).pack(pady=10)
        Button(self.current_frame,text="Sign Up",font=("Garamond", 16),width=20,height=2,command=self.show_signup).pack(pady=10)
        Button(self.current_frame,text="Exit",font=("Garamond", 16),width=20,height=2,command=self.root.destroy).pack(pady=10)

#login page
    def show_login(self):
        self.clear_frame()
        Label(self.current_frame,text="LOGIN",font=("Garamond", 26, "bold"),bg="aliceblue",fg="midnightblue").pack(pady=60)
        Label(self.current_frame,text="Student ID",bg="aliceblue").pack()
        student_id_entry = Entry(self.current_frame,width=30)
        student_id_entry.pack(pady=10)
        Label(self.current_frame,text="Password",bg="aliceblue").pack()
        password_entry = Entry(self.current_frame,width=30,show="*" )
        password_entry.pack(pady=10)
        Button(self.current_frame,text="Login",command=lambda: messagebox.showinfo("Login","Login will be added in Commit 3.")).pack(pady=20)
        Button(self.current_frame,text="Back",command=self.show_start).pack()

   #signup page
    def show_signup(self):
        self.clear_frame()
        Label(self.current_frame,text="CREATE ACCOUNT",font=("Garamond", 26, "bold"),bg="aliceblue",fg="midnightblue").pack(pady=60)
        Label(self.current_frame,text="Signup will be added in Commit 3.",bg="aliceblue").pack()
        Button(self.current_frame,text="Back",command=self.show_start).pack(pady=20)


#start the program
root = Tk()
app = InventoryApp(root)
root.mainloop()