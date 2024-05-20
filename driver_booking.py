from tkinter import *
from tkinter import messagebox
import data_storage
import connection
from tkinter.ttk import Treeview


class DriverBooking:
    def __init__(self, window):
        self.window = window
        self.window.title('Driver Dashboard')
        self.window.geometry('800x500')
        self.window.config(background="#1e1e1c")
        self._connection_ = connection.Database_connect.saaa()
        self.design()

    def design(self):
        self.title = Label(self.window, text="DRIVER DASHBOARD", bg='#1e1e1c', fg='#f1b842', font=('Times New Roman', 40))
        self.title.place(x=160, y=5)
        self.frame1 = Frame(self.window, width=500, height=400, bg="#f1b842", relief='groove')
        self.frame1.place(x=20, y=70)
        self.frame2 = Frame(self.window, width=250, height=400, bg='#f1b842', relief='groove')
        self.frame2.place(x=530, y=70)

        self.label_name = Label(self.frame1, text="Customer Name", font=('Times New Roman', 10), bg='#f1b842',
                                fg='white')
        self.label_name.place(x=20, y=20)
        self.namestr = StringVar()
        self.name_entry = Entry(self.frame1, font=('Times New Roman', 15),textvariable=self.namestr)
        self.name_entry.place(x=20, y=40, width=150, height=30)

        self.label_payment = Label(self.frame1, text="Payment Method", font=('Times New Roman', 10), bg='#f1b842',
                                fg='white')
        self.label_payment.place(x=270, y=20)
        self.paystr = StringVar()
        self.payment_entry = Entry(self.frame1, font=('Times New Roman', 15), textvariable=self.paystr)
        self.payment_entry.place(x=270, y=40, width=150, height=30)

        self.label_pickup_address = Label(self.frame1, text="Pick-up Address", font=('Times New Roman', 10),
                                          bg='#f1b842', fg='white')
        self.label_pickup_address.place(x=20, y=100)
        self.pickstr = StringVar()
        self.pickup_address_entry = Entry(self.frame1, font=('Times New Roman', 15),textvariable=self.pickstr)
        self.pickup_address_entry.place(x=20, y=120, width=150, height=30)

        self.label_dropof_address = Label(self.frame1, text="Drop-off Address", font=('Times New Roman', 10),
                                          bg='#f1b842', fg='white')
        self.label_dropof_address.place(x=270, y=100)
        self.dropstr = StringVar()
        self.dropof_address_entry = Entry(self.frame1, font=('Times New Roman', 15), textvariable=self.dropstr)
        self.dropof_address_entry.place(x=270, y=120, width=150, height=30)

        self.label_date = Label(self.frame1, text="Pick-up Date", font=('Times New Roman', 10), bg='#f1b842',
                                fg='white')
        self.label_date.place(x=20, y=185)
        self.datestr = StringVar()
        self.date_entry = Entry(self.frame1, font=('Times New Roman', 15), textvariable=self.datestr)
        self.date_entry.place(x=20, y=205, width=150, height=30)

        self.label_time = Label(self.frame1, text="Pick-up Time", font=('Times New Roman', 10), bg='#f1b842',
                                fg='white')
        self.label_time.place(x=270, y=185)
        self.timestr = StringVar()
        self.time_entry = Entry(self.frame1, font=('Times New Roman', 15), textvariable=self.timestr)
        self.time_entry.place(x=270, y=205, width=150, height=30)

        self.button = Button(self.frame1, text="Complete", font=('Times New Roman', 15),command=self.compl_driver)
        self.button.place(x=360, y=290, width=100, height=30)

        self.button1 = Button(self.frame1, text="show", font=('Times New Roman', 15), command=self.complete)
        self.button1.place(x=220, y=290, width=100, height=30)
        self.cusid = StringVar()
        self.customerid = Entry(textvariable=self.cusid)
        self.customerid.place_forget()

        column = ("id","CustomerName", "Status")
        self.tree_booking = Treeview(self.frame2, columns=column, show="headings", height=40)
        self.tree_booking.bind("<<TreeviewSelect>>", self.selectedRow)
        for col in column:
            self.tree_booking.heading(col, text=col, anchor="center")
            self.tree_booking.column(col, anchor="center", width=85)
            self.veiw_trip()
        self.tree_booking.place(x=0, y=0)


    def veiw_trip(self):

        try:
            self.id = data_storage.Driver[0]
            with self._connection_.cursor() as cursor:
                query = (f"SELECT user_register.User_id,user_register.Firstname,bookings.Booking_id, bookings.pick_up, "
                         f"bookings.drop_off, bookings.booking_date, bookings.payment_method, bookings.pickup_time,"
                         f"bookings.booking_status FROM user_register JOIN bookings ON bookings. User_id = "
                         f"user_register.User_id WHERE bookings.Driver_id = {self.id} ")
                cursor.execute(query)
                mydata = cursor.fetchall()
            for item in self.tree_booking.get_children():
                self.tree_booking.delete(item)

            for row in mydata:
                self.tree_booking.insert(parent='', index='end',
                                         values=(row[2], row[1], row[8]))
        except Exception as err:
            print(f"Error: {err}")
            messagebox.showerror("Taxi", f"Error fetching bookings: {err}")

    def selectedRow(self,event):

        try:
            selected_item = self.tree_booking.focus()
            values = self.tree_booking.item(selected_item, "values")

            if values:
                self.cusid.set(values[0])
        except Exception as e:
            messagebox.showerror("Taxi", f"Error fetching bookings: {e}")

    def complete(self):
        try:
            with self._connection_.cursor() as cursor:
                query = (f"SELECT user_register.Firstname, bookings.pick_up, bookings.drop_off, bookings.booking_date, "
                         f"bookings.payment_method, bookings.pickup_time,bookings.booking_status FROM user_register "
                         f"JOIN bookings"
                           " ON bookings.User_id = "
                         f"user_register.User_id WHERE bookings.Booking_id ='{self.cusid.get()}'")
                cursor.execute(query)
                mydata = cursor.fetchall()
            for i in mydata:
                self.namestr.set(i[0])
                self.paystr.set(i[4])
                self.pickstr.set(i[1])
                self.dropstr.set(i[2])
                self.datestr.set(i[3])
                self.timestr.set(i[5])

        except Exception as err:
            print(f"Error: {err}")
            messagebox.showerror("Taxi", f"Error fetching bookings: {err}")

    def compl_driver(self):
        try:
            with self._connection_.cursor() as cursor:
                query = f"UPDATE bookings SET `booking_status`='completed' WHERE `Booking_id`={self.cusid.get()}"
                query1 = f"UPDATE driver_register SET `status`='active' where `Driver_id`='{self.id}'"
                cursor.execute(query)
                cursor.execute(query1)
            # Commit the transaction
            self._connection_.commit()
            self.complete()
            self.veiw_trip()
            messagebox.showinfo("Taxi", "Trip Completed")
        except Exception as err:
            print(f"Error: {err}")
            messagebox.showerror("Taxi", f"Update Failure: {err}")


if __name__ == "__main__":
    window = Tk()
    driver_dashboard = DriverBooking(window)
    window.mainloop()