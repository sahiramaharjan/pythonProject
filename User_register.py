import tkinter as tk
from tkinter import *
from tkinter import messagebox
import re
import Driver_register
import Login
import connection


class RegisterWindow:
    def __init__(self, reg_window):
        self._connection_ = connection.Database_connect.saaa()
        self.reg_window = reg_window
        self.reg_window.geometry("800x500")
        self.reg_window.title(" Welcome to Quick Cabs")
        self.reg_window.config(background="#1e1e1c")
        self.design()

    def design(self):
        self.frame = tk.Frame(self.reg_window, width=720, height=420, bg='#f1b842')
        self.frame.place(x=40, y=40)

        # Create and place labels and entry boxes
        self.label_text1 = Label(self.reg_window, text="USER REGISTER", font=('Times New Roman', 38, 'bold'),
                                 fg='#f1b842', bg='#1e1e1c')
        self.label_text1.place(x=100, y=5)

        self.label_firstname = Label(self.frame, text="First Name", font=('Times New Roman', 10), bg='#f1b842',
                                     fg='white')
        self.label_firstname.place(x=60, y=55)
        self.firstname_entry = Entry(self.frame, font=('Times New Roman', 15))
        self.firstname_entry.place(x=60, y=75, width=200, height=40)

        self.label_surname = Label(self.frame, text="Last Name", font=('Times New Roman', 10), bg='#f1b842', fg='white')
        self.label_surname.place(x=400, y=55)
        self.surname_entry = Entry(self.frame, font=('Times New Roman', 15))
        self.surname_entry.place(x=400, y=75, width=200, height=40)

        self.label_address = Label(self.frame, text="Address", font=('Times New Roman', 10), bg='#f1b842', fg='white')
        self.label_address.place(x=60, y=130)
        self.address_entry = Entry(self.frame, font=('Times New Roman', 15))
        self.address_entry.place(x=60, y=150, width=200, height=40)

        self.label_phone = Label(self.frame, text="Mobile No.", font=('Times New Roman', 10), bg='#f1b842', fg='white')
        self.label_phone.place(x=400, y=130)
        self.phone_entry = Entry(self.frame, font=('Times New Roman', 15))
        self.phone_entry.place(x=400, y=150, width=200, height=40)

        self.label_email = Label(self.frame, text="Email Address", font=('Times New Roman', 10), bg='#f1b842',
                                 fg='white')
        self.label_email.place(x=60, y=205)
        self.email_entry = Entry(self.frame, font=('Times New Roman', 15))
        self.email_entry.place(x=60, y=225, width=290, height=40)

        self.label_password = Label(self.frame, text="Password", font=('Times New Roman', 10), bg='#f1b842', fg='white')
        self.label_password.place(x=400, y=205)
        self.pass_entry = Entry(self.frame, font=('Times New Roman', 15))
        self.pass_entry.place(x=400, y=225, width=200, height=40)
        # Create submit button
        self.submit_button = Button(self.frame, text="REGISTER", font=('Times New Roman', 10, 'bold'), height=2,
                                    width=12, borderwidth=1, relief="raised", bg="white", fg="black",
                                    activebackground='#5271ff', activeforeground='black', command=self.register)
        self.submit_button.place(x=570, y=320)

        self.switch_var = tk.IntVar()

        self.label = tk.Label(self.frame, text="Switch to Driver", bg='#f1b842')
        self.label.place(x=510, y=30)

        self.switch_button = tk.Checkbutton(self.frame, bg='#f1b842', variable=self.switch_var,
                                            command=self.switch_registration)
        self.switch_button.place(x=480, y=30)

    def switch_registration(self):
        if self.switch_var.get() == 1:
            self.reg_window.destroy()
            new_window = Tk()
            Driver_register.DriverRegister(new_window)
            new_window.mainloop()


    def register(self):
        if not (self.firstname_entry.get() and self.surname_entry.get() and self.address_entry.get() and
                self.phone_entry.get() and self.email_entry.get() and self.pass_entry.get()):
            messagebox.showinfo("Error", "Please fill in all the fields")
            return
        if self.checkemail(self.email_entry.get()) == True:
            try:
                with self._connection_.cursor() as cursor:
                    query = ("INSERT INTO `user_register`(`Firstname`, `Lastname`, `Address`, `Phone`, `Email`, `Password`) "
                            "VALUES(%s,%s,%s,%s,%s,%s)")
                    data = (self.firstname_entry.get(),self.surname_entry.get(),self.address_entry.get(),
                            self.phone_entry.get(), self.email_entry.get(), self.pass_entry.get())
                    cursor.execute(query, data)
                    self._connection_.commit()
                    messagebox.showinfo("Success", "Registration")
                    self.reg_window.destroy()
                    new_window = Tk()
                    Login.LoginWindow(new_window)
                    new_window.mainloop()

            except Exception as e:
                print(e)
                messagebox.showerror("Taxi","Registration Error")
        else:
            messagebox.showerror("Taxi","Fill the valid email")

    def checkemail(self,email):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(regex, email):
            emailResult=True

        else:
            emailResult=False

        return emailResult
    
if __name__ == "__main__":
    reg_window = Tk()
    register_reg_window = RegisterWindow(reg_window)
    reg_window.mainloop()