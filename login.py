from cards import Card 
import tkinter as tk
from tkinter import messagebox

class LoginWindow:

    def login(self, event=None):
        if self.password.get() == "bJack":
            self.username = self.username.get()
            self.win.destroy()
        else:
            messagebox.showerror("Error", "Invalid password")

    def cancel(self, event=None):
        self.username = None
        self.win.destroy()

    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Black Jack Login")
        self.win.geometry("300x150")
        self.win.bind('<Return>', self.login)
        self.win.bind('<Escape>', self.cancel)
        tk.Label(self.win, text="Username:").grid(row=0, column=0,padx=15, pady=15)
        tk.Label(self.win, text="Password:").grid(row=1, column=0,padx=15, pady=15)
        self.username = tk.Entry(self.win)
        self.password = tk.Entry(self.win, show="*")
        self.username.grid(row=0, column=1)
        self.password.grid(row=1, column=1)

        tk.Button(
            self.win, 
            width=12,
            text = "Login", 
            command = self.login,
            default = "active").grid(row=2, column=1, pady=5)
        
        self.username.focus_set()

    def getUsername(self):
        self.win.mainloop()
        return self.username
