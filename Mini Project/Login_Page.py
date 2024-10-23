import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
import mysql.connector as Error
from Register_Page import RegistrationPage

class LoginPage(RegistrationPage):
    def __init__(self):
        self.win =  tk.Tk()
        self.win.state("zoomed")
        self.win.resizable(0,0)
        
        self.win.title("Login Page")
        self.win.geometry("400x350")      
        self.win.configure(bg='#2a475e')
        self.lblusr=tk.Label(self.win,text="Username:", bg='#1b2838', fg='#c7d5e0', font=('Bold',15))
        self.lblusr.pack(pady=10)
        self.usrentry=tk.Entry(self.win)
        self.usrentry.pack(pady=5)
        
        self.lblpswd=tk.Label(self.win,text="Password:", bg='#1b2838', fg='#c7d5e0', font=('Bold',15))   
        self.lblpswd.pack(pady=10)
        self.pswdentry=tk.Entry(self.win,show="*")
        self.pswdentry.pack(pady=5)
        
        self.btnLogIn=tk.Button(self.win,text="Log In",command=self.open_tms,bg='#1b2838',
            fg='#c7d5e0',
            font=('Bold', 14),
            bd=0,
            activebackground='#2a475e',
            activeforeground='#c7d5e0')
        self.btnLogIn.pack(pady=20)
        
        self.btnOpenReg=tk.Button(self.win,text="No Account? Register",command=self.open_register,bg='#1b2838',
            fg='#c7d5e0',
            font=('Bold', 14),
            bd=0,
            activebackground='#2a475e',
            activeforeground='#c7d5e0')
        self.btnOpenReg.pack(pady=20)
        
        self.win.mainloop()
    
    def connect_db(self):
        """Establishes a connection to the MySQL database."""
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # XAMPP typically uses an empty password by default
                database="dbpro1"  # Make sure this matches your database name in XAMPP
            )
            if connection.is_connected():
                return connection
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")
            return None
    
    def open_tms(self):
        
        usrnm=self.usrentry.get()
        pswd=self.pswdentry.get()
        
        if not usrnm or not pswd:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        connection = self.connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT * FROM register WHERE user_name = %s AND pswd = %s"
                cursor.execute(query, (usrnm, pswd))
                user = cursor.fetchone()

                if user:
                    messagebox.showinfo("Success", "Log In successful!")
                    self.win.destroy()
                    from TMS import TaskManagementSystem
                    TaskManagementSystem(current_user=usrnm)
                else:
                    messagebox.showerror("Login Failed", "Invalid username or password!")

            except Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
            finally:
                cursor.close()
                connection.close()
        
    def open_register(self):
        self.win.destroy()
        RegistrationPage()
        
if __name__ == '__main__':
    LoginPage()        