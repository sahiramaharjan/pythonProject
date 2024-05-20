import tkinter as tk
from tkinter import *
from tkinter import messagebox

import connection
import data_storage
import user_booking


class LoginWindow:
    def __init__(self, window):
        self._connection_ = connection.Database_connect.saaa()
        self.window = window
        self.window.geometry("800x500")
        self.window.title(" Welcome to Quick Cabs")
        self.window.config(background="#1e1e1c")
        self.design()

    def design(self):
        # Convert the image to a PhotoImage object
        photo = PhotoImage(file='taxi2.png')
        # Create a label to display the image
        label_img = Label(self.window, bg="#1e1e1c", image=photo)
        label_img.image = photo  # Keep a reference to the PhotoImage to prevent garbage collection
        label_img.place(x='-190', y='0')

        self.label_text1 = Label(self.window, text="LOGIN", font=('Times New Roman', 38, 'bold'), fg='#f1b842',
                                 bg='#1e1e1c')
        self.label_text1.place(x=430, y=10)

        # Create a frame for login form
        self.frame = tk.Frame(self.window, width=347, height=361, bg='#f1b842')
        self.frame.place(x=340, y=80)

        # Create labels and entries for username and password in frame
        self.label_username = Label(self.frame, text="Username", font=('Times New Roman', 10, 'bold'), bg='#f1b842',
                                    fg='white')
        self.label_username.place(x=60, y=30)
        self.label_password = Label(self.frame, text="Password", font=('Times New Roman', 10, 'bold'), bg='#f1b842',
                                    fg='white')
        self.label_password.place(x=60, y=120)
        self.user_entry = Entry(self.frame, font=("Times New Roman", 15))
        self.user_entry.place(x=60, y=50, width=220, height=40)
        self.pass_entry = Entry(self.frame, show="*")
        self.pass_entry.place(x=60, y=140, width=220, height=40)

        self.log_button = Button(self.frame, text="Login", height=2, width=12, borderwidth=2, relief="raised",
                                 bg="#d9d9d9", fg="black", activebackground='#5271ff', activeforeground='#d9d9d9',
                                 command=self.login)
        self.log_button.place(x=50, y=230)
        self.register_button = Button(self.frame, text="Register", height=2, width=12, borderwidth=2, relief="raised",
                                      bg="#d9d9d9", fg="black", activebackground='#5271ff', activeforeground='#d9d9d9',
                                      command=self.reg_log)
        self.register_button.place(x=200, y=230)
        self.back_button = Button(self.frame, text="BACK", font=('Times New Roman', 10, 'bold'), height=2, width=12,
                                  borderwidth=0, relief="raised", bg="#f1b842", fg="white", activebackground='#f1b842',
                                  activeforeground='black', command=self.main)
        self.back_button.place(x=130, y=290)

    def login(self):
        try:
            email = self.user_entry.get()
            password = self.pass_entry.get()

            # Check if email and password are not empty
            if email == '' and password == '':
                messagebox.showerror("Taxi", "Please enter both email and password.")

            elif email == '':

                messagebox.showerror("Taxi", "Please enter email ")

            elif password == '':
                messagebox.showerror("Taxi", "Please enter  password")

            elif email != '' and password != '':

                with self._connection_.cursor() as cursor:
                    cursor.execute("SELECT * FROM user_register WHERE Email=%s AND Password=%s", (email, password))
                    record = cursor.fetchone()

                    cursor.execute("SELECT * FROM driver_register WHERE Email=%s AND Password=%s", (email, password))
                    driver = cursor.fetchone()

                    cursor.execute("SELECT * FROM admin WHERE email=%s AND password=%s", (email, password))
                    admin = cursor.fetchone()

                    if record:
                        messagebox.showinfo("Taxi", "Login successful")
                        data_storage.customer = record
                        self.window.destroy()
                        new_window = Tk()
                        user_booking.UserBooking(new_window)
                        new_window.mainloop()
                    elif driver:
                        import driver_booking
                        data_storage.Driver = driver
                        messagebox.showinfo("Taxi", "Driver Login Successful")
                        self.window.destroy()
                        new_window = Tk()
                        driver_booking.DriverBooking(new_window)
                        new_window.mainloop()
                    elif admin:
                        import admin_dashboard
                        data_storage.Admin = admin
                        messagebox.showinfo("Taxi", "Admin Login Successful")
                        self.window.destroy()
                        new_window = Tk()
                        admin_dashboard.AdminDashboard(new_window)
                        new_window.mainloop()

                    else:
                        messagebox.showerror("Taxi", "Invalid email or password")
        except Exception as e:
            print(e)


    def reg_log(self):
        import User_register
        self.window.destroy()
        new_window = Tk()
        User_register.RegisterWindow(new_window)
        new_window.mainloop()

    def main(self):
        import main
        self.window.destroy()
        new_window = Tk()
        main.MainWindow(new_window)
        new_window.mainloop()


if __name__ == "__main__":
    window = Tk()
    login_window = LoginWindow(window)
    window.mainloop()