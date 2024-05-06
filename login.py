from cards import Card 
from tkinter import *
from tkinter import messagebox

class LoginWindow(Tk):

    def login(self, event = None):
        if self.password.get() == "jack":
            self.player = self.username.get()
            self.quit()
        else:
            messagebox.showerror("Error", "Invalid password")

    def cancel(self, event = None):
        self.quit()

    def __init__(self):
        Tk.__init__(self)
        self.player = None

        self.title("Black Jack Login")
        self.geometry("300x150")
        self.eval('tk::PlaceWindow . center')
        self.bind('<Return>', self.login)
        self.bind('<Escape>', self.cancel)
        Label(self, text="Username:").grid(row = 0, column = 0, padx = 15, pady = 15)
        Label(self, text="Password:").grid(row = 1, column = 0, padx = 15, pady = 15)
        self.username = Entry(self)
        self.password = Entry(self, show = "*")
        self.username.grid(row = 0, column = 1)
        self.password.grid(row = 1, column = 1)
        Button(self, width = 12, text = "Login", command = self.login, default = "active").grid(row = 2, column = 1, pady = 5)        
        self.username.focus_set()

    def getUsername(self):
        self.mainloop()
        self.destroy()
        return self.player
