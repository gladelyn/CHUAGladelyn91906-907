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
        self.root.title("Inventory Management System")
        self.root.state("zoomed")
        self.root.configure(bg="aliceblue" )

        self.title_frame = Frame(self.root,bg="midnightblue",height=80)
        self.title_frame.pack(fill=X)
        self.title_frame.pack_propagate(False)
        Label(self.title_frame,text="INVENTORY MANAGEMENT SYSTEM",font=("Garamond", 24, "bold"),bg="midnightblue",fg="white").pack(pady=20)

        self.main_frame = Frame(self.root,bg="aliceblue")
        self.main_frame.pack(fill=BOTH,expand=True)

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
        Entry(self.main_frame,width=30,show="*").pack(pady=)
        Button(self.main_frame,text="Login",width=20).pack(pady=20)
        Button(self.main_frame,text="Create Account",width=20,command=self.show_signup).pack()

        # Footer is only displayed on login
        self.create_footer()


    def show_signup(self):
        self.clear_main_frame()
        self.clear_footer()
        Label(self.main_frame,text="CREATE ACCOUNT",font=("Garamond", 28, "bold"),bg="aliceblue",fg="midnightblue").pack(pady=50)

       
        Button(self.main_frame,text="Back to Login",command=self.show_login).pack(pady=20)

    def create_footer(self):
        cards = [
            ("📦","Easy Inventory","Keep track of your items."),

            ("🔒","Secure","Your information is protected."),

            ("🔔","Notifications","Stay updated about your items."),

            ( "📊","Reports","Analyse inventory trends."
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