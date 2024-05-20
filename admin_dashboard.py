from tkinter import *
from tkinter.ttk import Treeview
import data_storage
from tkinter import messagebox
import connection
class AdminDashboard:
    def __init__(self,window):
        self.window = window
        self.window.title('Admin Dashboard')
        self.window.geometry('800x500')
        self.window.config(background='#1e1e1c')
        self._connection_ = connection.Database_connect.saaa()
        self.design()

    def design(self):
        self.label_title = Label(self.window, text='ADMIN DASHBOARD', font=('Times New Roman', 40), bg='#1e1e1c',
                                 fg='#f1b842')
        self.label_title.place(x=160, y=5)

        self.frame = Frame(self.window, width=750, height=400, bg='#f1b842', relief='groove')
        self.frame.place(x=20, y=70)

        self.user_id = Label(self.frame, text='Booking ID', font=('Times New Roman', 15), bg='#f1b842')
        self.user_id.place(x=50, y=50)
        self.user_entry = Entry(self.frame, font=("Times New Roman", 15))
        self.user_entry.place(x=200, y=50)

        self.come_driverid()
        self.driver_id = Label(self.frame, text='Driver ID', font=('Times New Roman', 15), bg='#f1b842')
        self.driver_id.place(x=460, y=20)
        self.veiw_deriverid = StringVar()
        self.veiw_deriverid.set("select driver")
        self.label_driver = OptionMenu(self.frame, self.veiw_deriverid, *self.mylist)
        self.label_driver.place(x=480, y=50, width=170, height=30)

        self.label_pay = Label(self.frame, text="Booking Status:", font=('Times New Roman', 14), bg='#f1b842',
                               fg='black')
        self.label_pay.place(x=50, y=100)
        self.veiw_option = StringVar()
        self.veiw_option.set("pending")
        self.label_pay_opt = OptionMenu(self.frame, self.veiw_option, "pending", "booked")
        self.label_pay_opt.place(x=200, y=100, width=170, height=30)

        self.assign_btn = Button(self.frame,text="assign",command=self.assign_driver)
        self.assign_btn.place(x=600,y=150)
        column = ("Booking Id", "Name","phone","pickup_address", "dropoff_address", "date","time","Booking Status")
        self.tree_booking = Treeview(self.frame, columns=column, show="headings", height=8)
        self.tree_booking.bind("<<TreeviewSelect>>", self.selectedRow)
        for i in column:
            self.tree_booking.heading(i, text=i, anchor="center")
            self.tree_booking.column(i, anchor="center", width=120)
        self.tree_booking.place(x=15, y=200)
        self.showBook()


    def showBook(self):

        try:
            with self._connection_.cursor() as cursor:
                query = ''' SELECT bookings.Booking_id,CONCAT(user_register.FirstName," ",user_register.LastName),
                user_register.Phone,bookings.pick_up,bookings.drop_off,bookings.booking_date,bookings.pickup_time,
                bookings.booking_status FROM user_register JOIN bookings ON bookings. User_id = user_register.User_id 
                WHERE bookings.booking_status = "pending"
                      '''
                cursor.execute(query)

                rows = cursor.fetchmany(size=10)

            for item in self.tree_booking.get_children():
                self.tree_booking.delete(item)

            for row in rows:
                self.tree_booking.insert(parent='', index='end',
                                         values=(row[0], row[1], row[2], row[3], row[4], row[5],row[6],row[7]))

        except Exception as err:
            print(f"Error: {err}")
            messagebox.showerror("Taxi", f"Error fetching bookings: {err}")

    def selectedRow(self, event):
        selected_item = self.tree_booking.focus()
        values = self.tree_booking.item(selected_item, "values")

        if values:
            self.user_entry.delete(0, "end")
            self.user_entry.insert(0,values[0])
            self.veiw_option.set(values[7])

    def assign_driver(self):
        try:
            with self._connection_.cursor() as cursor:
                query = (f"UPDATE `bookings` SET `booking_status`='booked',`Driver_id`='{self.veiw_deriverid.get()}' "
                         f"WHERE `Booking_id` ='{self.user_entry.get()}'")
                result = cursor.execute(query)
                query1 = f"UPDATE `driver_register` SET status='inactive' where `Driver_id`={self.veiw_deriverid.get()}"
                result1 = cursor.execute(query1)
                self._connection_.commit()
                self.showBook()
                self.come_driverid()
                messagebox.showinfo("Taxi", "Driver Assigned")
        except Exception as err:
            print(f"Error: {err}")
            messagebox.showerror("Taxi", f"Assigned Failure: {err}")
    def come_driverid(self):
        try:
            with self._connection_.cursor() as cursor:
                query = "SELECT `Driver_id` from driver_register where `status`='active' "
                cursor.execute(query)
                mydata = cursor.fetchall()

            self.mylist = [r for r, in mydata]
        except Exception as err:
            print(f"Error: {err}")
            messagebox.showerror("Taxi", f"Error fetching bookings: {err}")


if __name__ == "__main__":
    window = Tk()
    admin_dashboard = AdminDashboard(window)
    window.mainloop()