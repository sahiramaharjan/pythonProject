import tkinter as tk
from tkinter import *
from tkinter import messagebox
import User_register

class MainWindow:
    def __init__(self, window):
        self.window = window
        self.window.geometry("800x500")
        self.window.title("Quick Cabs")
        self.window.config(background="#1e1e1c")

        # Converting the image to a PhotoImage object
        photo=PhotoImage(file='taxi.png')
        # Creating a label to display the image
        label_img = Label(window,bg="#1e1e1c", image=photo)
        label_img.image = photo  # Keep a reference to the PhotoImage to prevent garbage collection
        label_img.place(x='540', y='0')

        # Creating a label to display text
        label_text1 = Label(self.window, text="QUICK CABS", font=('Times New Roman', 38, 'bold'), fg='#f1b842',
                            bg='#1e1e1c')
        label_text1.place(x=40, y=300)

        label_text2 = Label(self.window, text="Quick and Reliable. Anytime Anywhere ", font=('Kollektif', 19), fg='white',
                            bg='#1e1e1c')
        label_text2.place(x=40, y=360)

        # Creating buttons for login and register
        self.button1 = Button(self.window, text="Login", height=0, width=7, borderwidth=1, relief="groove", bg="#d9d9d9",
                         fg="black",
                         activebackground='#f1b842', activeforeground='white', command=self.log)
        self.button1.place(x=40, y=400)

        self.button2 = Button(self.window, text="Register", height=0, width=7, borderwidth=1, relief="groove", bg="#d9d9d9",
                         fg="black",
                         activebackground='#f1b842', activeforeground='white', command=self.register_user)
        self.button2.place(x=140, y=400)

    def log(self):
        import Login
        self.window.destroy()
        new_window = Tk()
        Login.LoginWindow(new_window)
        new_window.mainloop()

    def register_user(self):
        import User_register
        self.window.destroy()
        new_window = Tk()
        User_register.RegisterWindow(new_window)
        new_window.mainloop()


if __name__ == "__main__":
    window = tk.Tk()
    main_window = MainWindow(window)
    window.mainloop()