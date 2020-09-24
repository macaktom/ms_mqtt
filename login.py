from tkinter import *
import re

from app import AppFrame


class LoginFrame(Frame):
    def __init__(self, parent):
        super(LoginFrame, self).__init__(parent)  # Set __init__ to the master class
        self.parent = parent
        #self.parent.geometry("%dx%d+%d+%d" % self.get_center(self.width, self.height))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        #self.check_app()
        self.create_main()

    #def check_app(self):
        #for widget in self.parent.winfo_children():
            #if isinstance(widget, AppFrame):
                #widget.destroy()
            #else:
                #continue

    def create_main(self):
        self.title = Label(self, text="Login")
        self.title.grid(row=0, column=2)

        self.client_entry_label = Label(self, text="Client: ")
        self.client_entry_label.grid(row=1, column=1, sticky=W+E+N+S)

        self.client_entry = Entry(self)
        self.client_entry.grid(row=1, column=2, sticky=W+E+N+S)

        self.user_entry_label = Label(self, text="Username: ")
        self.user_entry_label.grid(row=2, column=1, sticky=W+E+N+S)

        self.user_entry = Entry(self)
        self.user_entry.grid(row=2, column=2, sticky=W+E+N+S)
        self.user_entry.insert(0, "mobilni")

        self.pass_entry_label = Label(self, text="Password: ")
        self.pass_entry_label.grid(row=3, column=1)

        self.pass_entry = Entry(self, show="*")
        self.pass_entry.grid(row=3, column=2, sticky=W+E+N+S)
        self.pass_entry.insert(0, "Systemy")

        self.sign_in_butt = Button(self, text="Sign In", command=self.logging_in)
        self.sign_in_butt.grid(row=6, column=2, sticky=W+E+N+S)

    def logging_in(self):
        client_name = self.client_entry.get()
        username = self.user_entry.get()
        password = self.pass_entry.get()

        if username == 'mobilni' and password == "Systemy" and re.search("^[a-z]{3}[0-9]{4}$", client_name):
            self.login_success(client_name)
            self.parent.username = username
            self.parent.password = password
        else:
            self.login_fail()

    def login_success(self, client):
        self.login_success_screen = Toplevel(self)
        #self.login_success_screen.geometry("%dx%d+%d+%d" % self.get_center(self.width, self.height))
        self.log_label = Label(self.login_success_screen, text=f"Client ID {client} is OK. Connecting to broker...").pack()
        self.log_button = Button(self.login_success_screen, text="OK", command=lambda: self.delete_login_success(client)).pack()

    def login_fail(self):
        self.login_fail_screen = Toplevel(self)
        self.login_fail_screen.title("Login failed")
        #self.login_fail_screen.geometry("%dx%d+%d+%d" % self.get_center(self.width, self.height))
        self.log_fail_label = Label(self.login_fail_screen, text=f"Login failed. Use different credentials").pack()
        self.log_fail_button = Button(self.login_fail_screen, text="OK", command=self.delete_login_fail).pack()

    def delete_login_success(self, client):
        self.client_entry.delete(0, 'end')
        #self.user_entry.delete(0, 'end')
        #self.pass_entry.delete(0, 'end')
        self.login_success_screen.destroy()
        self.parent.client_name = client
        self.parent.switch_frame("app", self)

    def delete_login_fail(self):
        self.client_entry.delete(0, 'end')
        #self.user_entry.delete(0, 'end')
        #self.pass_entry.delete(0, 'end')
        self.login_fail_screen.destroy()