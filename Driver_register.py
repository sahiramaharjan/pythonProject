import tkinter as tk
from tkinter import *
from tkinter import messagebox

from tkcalendar import DateEntry

import Login
import mysql.connector
import connection


class DriverRegister:
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
        self.label_text1 = Label(self.reg_window, text="DRIVER REGISTER", font=('Times New Roman', 38, 'bold'),
                                 fg='#f1b842', bg='#1e1e1c')
        self.label_text1.place(x=100, y=5)

        self.label_name = Label(self.frame, text="Full Name", font=('Times New Roman', 10), bg='#f1b842', fg='white')
        self.label_name.place(x=60, y=55)
        self.name_entry = Entry(self.frame, font=('Times New Roman', 15))
        self.name_entry.place(x=120, y=55, width=150, height=30)

        self.label_dob = Label(self.frame, text="Date of Birth", font=('Times New Roman', 10), bg='#f1b842', fg='white')
        self.label_dob.place(x=400, y=55)
        self.dob_entry = DateEntry(self.frame, selectmode='day', width=15, height=10, bg='darkblue', fg='white',
                                   borderwidth=2)
        self.dob_entry.place(x=480, y=55)

        self.label_address = Label(self.frame, text="Address", font=('Times New Roman', 10), bg='#f1b842',
                                       fg='white')
        self.label_address.place(x=60, y=110)
        self.address_entry = Entry(self.frame, font=('Times New Roman', 15))
        self.address_entry.place(x=120, y=110, width=150, height=30)

        self.label_phone = Label(self.frame, text="Mobile No.", font=('Times New Roman', 10), bg='#f1b842',
                                     fg='white')
        self.label_phone.place(x=400, y=110)
        self.phone_entry = Entry(self.frame, font=('Times New Roman', 15))
        self.phone_entry.place(x=480, y=110, width=150, height=30)

        self.label_email = Label(self.frame, text="Email", font=('Times New Roman', 10), bg='#f1b842',
                                     fg='white')
        self.label_email.place(x=60, y=165)
        self.email_entry = Entry(self.frame, font=('Times New Roman', 15))
        self.email_entry.place(x=120, y=165, width=290, height=30)

        self.label_password = Label(self.frame, text="Password", font=('Times New Roman', 10), bg='#f1b842', fg='white')
        self.label_password.place(x=60, y=220)
        self.pass_entry = Entry(self.frame, font=('Times New Roman', 15))
        self.pass_entry.place(x=120, y=220, width=150, height=30)

        self.label_gender = Label(self.frame, text="Gender", font=('Times New Roman', 10), bg='#f1b842', fg='white')
        self.label_gender.place(x=400, y=220)
        self.gender = StringVar()
        self.gender_radio1 = Radiobutton(self.frame, text="Male", variable=self.gender, value="Male", bg='#f1b842')
        self.gender_radio1.place(x=450, y=220)
        self.gender_radio2= Radiobutton(self.frame, text="Female", variable=self.gender, value="Female", bg='#f1b842')
        self.gender_radio2.place(x=550, y=220)

        self.license = Label(self.frame, text="License Number", font=('Times New Roman', 10), bg='#f1b842', fg='white')
        self.license.place(x=400, y=275)
        self.license_entry = Entry(self.frame, font=('Times New Roman', 15))
        self.license_entry.place(x=500, y=275, width=150, height=30)

        self.label_vehicle = Label(self.frame, text="Vehicle", font=('Times New Roman', 10), bg='#f1b842', fg='white')
        self.label_vehicle.place(x=60, y=275)
        self.option = StringVar()
        self.option.set("Select your vehicle")
        self.vehicle = OptionMenu(self.frame, self.option, "Two-Wheeler", "Four-wheeler")
        self.vehicle.place(x=120, y=275, width=170, height=30)

            # Create submit button
        self.submit_button = Button(self.frame, text="REGISTER", font=('Times New Roman', 10, 'bold'), height=2,
                                        width=12, borderwidth=1, relief="raised", bg="white", fg="black",
                                        activebackground='#5271ff', activeforeground='black', command=self.register)
        self.submit_button.place(x=570, y=320)

    def register(self):
        try:
            with self._connection_.cursor() as cursor:
                query = (f"INSERT INTO `driver_register`(`Fullname`, `Dob`, `Address`, `Phone`, `Email`, `Password`, "
                         f"`Gender`, `License_no`, `Vehicle`) VALUES('{self.name_entry.get()}','{self.dob_entry.get_date()}"
                         f"','{self.address_entry.get()}','{self.phone_entry.get()}','{self.email_entry.get()}','"
                         f"{self.pass_entry.get()}','{self.gender.get()}', '{self.license_entry.get()}','{self.option.get()}')")

                cursor.execute(query)
                self._connection_.commit()
                messagebox.showinfo("Success", "Registration")

                self.reg_window.destroy()
                new_window = Tk()
                Login.LoginWindow(new_window)
                new_window.mainloop()

        except Exception as e:
            print(e)
            messagebox.showerror("Taxi", "Registration Error")


if __name__ == "__main__":
    reg_window = tk.Tk()
    register_reg_window = DriverRegister(reg_window)
    reg_window.mainloop()
