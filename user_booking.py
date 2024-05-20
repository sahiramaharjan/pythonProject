from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview

import mysql
from tkcalendar import DateEntry
from time import strftime

import connection
import data_storage


class UserBooking:
    def __init__(self, window):
        self._connection_ = connection.Database_connect.saaa()
        self.window = window
        self.window.title('Customer Dashboard')
        self.window.geometry('800x500')
        self.window.config(background="#1e1e1c")
        self.ui()
        self.booking_id = 0

    def ui(self):
        self.dash = Label(self.window, text='USER DASHBOARD', bg="#1e1e1c", fg="#f1b842", font=('Times New Roman', 40))
        self.dash.place(x=160, y=5)

        self.menu_frame = Frame(self.window, width=100, height=600, bg="#f1b842", relief='groove')
        self.menu_frame.place(x=10, y=60)

        photo = PhotoImage(file='profile.png')
        # Create a label to display the image
        self.profile_button = Button(self.menu_frame, text="My Profile", font=("Times New Roman", 9), bg="#f1b842",
                                     fg="black", image=photo, compound='top', relief='flat',
                                     command=self.show_main_frame)
        self.profile_button.image = photo  # Keep a reference to the PhotoImage to prevent garbage collection
        self.profile_button.place(x='20', y='30')

        photo2 = PhotoImage(file='view_booking_icon.png')
        # Create a label to display the image
        self.view_button = Button(self.menu_frame, text="View Booking", font=("Times New Roman", 9), bg="#f1b842",
                                  fg="black", image=photo2, compound='top', relief='flat', command=self.show_view)
        self.view_button.image = photo2 # Keep a reference to the PhotoImage to prevent garbage collection
        self.view_button.place(x='20', y='130')

        photo3 = PhotoImage(file='billing_icon.png')
        # Create a label to display the image
        self.receipt_button = Button(self.menu_frame, text="Receipt", font=("Times New Roman", 9), bg="#f1b842",
                                     fg="black", image=photo3, compound='top', relief='flat')
        self.receipt_button.image = photo3  # Keep a reference to the PhotoImage to prevent garbage collection
        self.receipt_button.place(x='20', y='230')

        photo4 = PhotoImage(file='logout_icon.png')
        # Create a label to display the image
        self.logout_button = Button(self.menu_frame, text="Log Out", font=("Times New Roman", 9), bg="#f1b842",
                                    fg="black", image=photo4, compound='top', relief='flat', command=self.button_click)
        self.logout_button.image = photo4  # Keep a reference to the PhotoImage to prevent garbage collection
        self.logout_button.place(x='20', y='330')

        # main-frame
        self.main_frame = Frame(self.window, width=650, height=600, bg="#f1b842")
        self.main_frame.place(x=130, y=60)

        # under book frame
        self.heading = Label(self.main_frame, text='Book Your Ride!!', bg="#f1b842", font=('Times New Roman', 25))
        self.heading.place(x=10, y=5)
        self.date = Label(self.main_frame, text='Date :', bg="#f1b842", font=('Times New Roman', 14))
        self.date.place(x=0, y=55)
        self.date_entry = DateEntry(self.main_frame, selectmode='day', width=15, height=10, background='darkblue',
                                    foreground='white', borderwidth=2)
        self.date_entry.place(x=50, y=57)

        self.time = Label(self.main_frame, text='Time :', bg="#f1b842", font=('Times New Roman', 14))
        self.time.place(x=250, y=55)
        self.show_time = Label(self.main_frame, font=('calibri', 20, 'bold'), background='#f1b842', foreground='white')
        self.show_time.place(x=530, y=0)
        self.display_time()

        self.spinbox_hours = Spinbox(self.main_frame, from_=1, to=12, width=5)
        self.spinbox_hours.place(x=320, y=60)

        self.spinbox_minutes = Spinbox(self.main_frame, from_=0, to=59, width=5)
        self.spinbox_minutes.place(x=370, y=60)
        # am and pm
        self.spinbox_am_pm = Spinbox(self.main_frame, values=("AM", "PM"), width=5)
        self.spinbox_am_pm.place(x=420, y=60)

        self.spinbox_no = Spinbox(self.main_frame, from_=1, to=4, width=5)
        self.spinbox_no.place(x=175, y=146)

        self.pick_from = Label(self.main_frame, text='Pick-up address:', bg="#f1b842", font=('Times New Roman', 14))
        self.pick_from.place(x=0, y=95)
        self.pick_address = Entry(self.main_frame, font=('Times New Roman', 15))
        self.pick_address.place(x=150, y=95, width=150, height=30)

        self.drop_to = Label(self.main_frame, text='Drop-off address:', bg="#f1b842", font=('Times New Roman', 14))
        self.drop_to.place(x=0, y=135)
        self.drop_address = Entry(self.main_frame, font=('Times New Roman', 15))
        self.drop_address.place(x=150, y=135, width=150, height=30)

        self.label_pay = Label(self.main_frame, text="Payment Method:", font=('Times New Roman', 14), bg='#f1b842',
                               fg='black')
        self.label_pay.place(x=0, y=180)
        self.option = StringVar()
        self.option.set("Select payment method")
        self.label_pay = OptionMenu(self.main_frame,self.option, "Cash", "Bank Transfer", "Esewa",
                                    "Khalti")
        self.label_pay.place(x=150, y=180, width=170, height=30)

        self.confirm = Button(self.main_frame, text='Confirm', width=8, height=1, font=('Times New Roman', 12),
                              bg='#895D2D', activebackground='#5271ff', activeforeground='black',
                              command=self.booking_success)
        self.confirm.place(x=550, y=240)

        # view frame
        self.view_frame = Frame(self.window, width=650, height=600, bg="#f1b842")
        self.view_frame.place(x=130, y=60)
        self.show_main_frame()

        self.date = Label(self.view_frame, text='Date :', bg="#f1b842", font=('Times New Roman', 14))
        self.date.place(x=0, y=35)
        self.view_date_entry = DateEntry(self.view_frame, selectmode='day', width=15, height=10, background='darkblue', 
                                         foreground='white', borderwidth=2)
        self.view_date_entry.place(x=50, y=35)

        self.time = Label(self.view_frame, text='Time :', bg="#f1b842", font=('Times New Roman', 14))
        self.time.place(x=350, y=115)
        self.show_time = Label(self.view_frame, font=('calibri', 20, 'bold'), background='#f1b842', foreground='white')
        self.show_time.place(x=530, y=0)
        self.display_time()

        self.view_spinbox_hours = Spinbox(self.view_frame, from_=1, to=12, width=5)
        self.view_spinbox_hours.place(x=410, y=115)

        self.view_spinbox_minutes = Spinbox(self.view_frame, from_=0, to=59, width=5)
        self.view_spinbox_minutes.place(x=460, y=115)
        # am and pm
        self.view_spinbox_am_pm = Spinbox(self.view_frame, values=("AM", "PM"), width=5)
        self.view_spinbox_am_pm.place(x=520, y=115)

        self.view_pick_from = Label(self.view_frame, text='Pick-up address:', bg="#f1b842", font=('Times New Roman', 14))
        self.view_pick_from.place(x=0, y=65)
        self.view_pick_address = Entry(self.view_frame, font=('Times New Roman', 15))
        self.view_pick_address.place(x=150, y=65, width=150, height=30)

        self.view_drop_to = Label(self.view_frame, text='Drop-off address:', bg="#f1b842", font=('Times New Roman', 14))
        self.view_drop_to.place(x=320, y=65)
        self.view_drop_address = Entry(self.view_frame, font=('Times New Roman', 15))
        self.view_drop_address.place(x=470, y=65, width=150, height=30)

        self.label_pay = Label(self.view_frame, text="Payment Method:", font=('Times New Roman', 14), bg='#f1b842',
                               fg='black')
        self.label_pay.place(x=0, y=115)
        self.view_option = StringVar()
        self.view_option.set("Select payment method")
        self.label_pay = OptionMenu(self.view_frame, self.view_option, "Cash", "Bank Transfer", "Esewa",
                                    "Khalti")
        self.label_pay.place(x=150, y=115, width=170, height=30)

        self.update = Button(self.view_frame, text='update', width=8, height=1, font=('Times New Roman', 12),
                             bg='#895D2D', activebackground='#5271ff', activeforeground='black',
                             command=self.update_bookings)
        self.update.place(x=350, y=160)

        self.can = Button(self.view_frame, text='Cancel', width=8, height=1, font=('Times New Roman', 12), bg='#895D2D',
                          activebackground='#5271ff', activeforeground='black', command=self.cancel)
        self.can.place(x=450, y=160)

        column = ("ID", "Pick-up Address", "Drop-off Address", "Date", "Payment Method", "Time", "status")
        self.tree_booking = Treeview(self.view_frame, columns=column, show="headings", height=8)
        self.tree_booking.bind("<<TreeviewSelect>>", self.selectedRow)
        for i in column:
            self.tree_booking.heading(i, text=i, anchor="center")
            self.tree_booking.column(i, anchor="center", width=90)
            self.tree_booking.place(x=15, y=200)
            self.showBook()

    def showBook(self):

        try:
            id = data_storage.customer[0]
            with self._connection_.cursor() as cursor:
                query = f"SELECT * FROM bookings where User_id={id}"
                cursor.execute(query)

                rows = cursor.fetchmany(size=10)

            for item in self.tree_booking.get_children():
                self.tree_booking.delete(item)

            for row in rows:
                self.tree_booking.insert(parent='', index='end',
                                         values=(row[0], row[1], row[2], row[3], row[4], row[5],row[6]))

        except Exception as err:
            print(f"Error: {err}")
            messagebox.showerror("Taxi", f"Error fetching bookings: {err}")

    def booking_success(self):
        self.time = f"{self.spinbox_hours.get()}hr:{self.spinbox_minutes.get()}min {self.spinbox_am_pm.get()}"
        self.User_id = data_storage.customer[0]

        try:
            with self._connection_.cursor() as cursor:

                query = (f"INSERT INTO `bookings`(`Booking_id`, `pick_up`, `drop_off`, `booking_date`,`payment_method`,"
                         f"`pickup_time`,`User_id`) VALUES ('{self.booking_id}','{self.pick_address.get()}','"
                         f"{self.drop_address.get()}','{self.date_entry.get_date()}','{self.option.get()}','"
                         f"{self.time}','{self.User_id}')")
                cursor.execute(query)
                self._connection_.commit()
                self.showBook()
            messagebox.showinfo("Taxi", "Booked")
        except Exception as err:
            print(f"Error: {err}")
            messagebox.showerror("Taxi", f"Booking Failure: {err}")

    def show_main_frame(self):
        self.main_frame.place(x=130, y=60)
        self.view_frame.place_forget()

    def log(self):
        import Login
        self.window.destroy()
        new_window = Tk()
        Login.LoginWindow(new_window)
        new_window.mainloop()

    def show_view(self):
        self.view_frame.place(x=130, y=60)
        self.main_frame.place_forget()

    def button_click(self):
        result = messagebox.askquestion("Popup", "Do you want to log out?", icon='warning')

        if result == 'yes':
            self.log()
        else:
            messagebox.showinfo("Info", "You chose not to log out.")

    def display_time(self):
        self.time_string = strftime('%I:%M %p')
        self.show_time.config(text=self.time_string)
        self.show_time.after(1000, self.display_time)

    def selectedRow(self, event):
        selected_item = self.tree_booking.focus()
        values = self.tree_booking.item(selected_item, "values")
        self.id = StringVar()
        self.book_id = Entry(textvariable=self.id)
        self.book_id.place_forget()
        if values:

            self.id.set(values[0])

            self.view_pick_address.delete(0, "end")
            self.view_pick_address.insert(0, values[1])

            self.view_drop_address.delete(0, "end")
            self.view_drop_address.insert(0, values[2])

            self.view_option.set(values[4])

            self.view_date_entry.delete(0,"end")
            self.view_date_entry.insert(0,values[3])

    def update_bookings(self):
        try:
            self.time = f"{self.spinbox_hours.get()}hr:{self.spinbox_minutes.get()}min {self.spinbox_am_pm.get()}"

            with self._connection_.cursor() as cursor:
                query = (f"UPDATE `bookings` SET `pick_up`='{self.view_pick_address.get()}',`drop_off`='"
                         f"{self.view_drop_address.get()}',`booking_date`='{self.view_date_entry.get_date()}',"
                         f"`payment_method`='{self.view_option.get()}',`pickup_time`='{self.time}' WHERE Booking_id = "
                         f"{self.id.get()}")
                cursor.execute(query)
            # Commit the transaction
            self._connection_.commit()
            self.showBook()

            messagebox.showinfo("Taxi", "Updated bookings")

        except Exception as err:
            print(f"Error: {err}")
            messagebox.showerror("Taxi", f"Update Failure: {err}")

    def cancel(self):
        try:
            with self._connection_.cursor() as cursor:
                query = f"DELETE FROM `bookings`  WHERE Booking_id = {self.id.get()}"
                cursor.execute(query)
            # Commit the transaction
            self._connection_.commit()
            self.showBook()

            messagebox.showinfo("Taxi", "delete bookings")
        except Exception as err:
            print(f"Error: {err}")
            messagebox.showerror("Taxi", f"Update Failure: {err}")


if __name__ == "__main__":
    window = Tk()
    user_dashboard = UserBooking(window)
    window.mainloop()