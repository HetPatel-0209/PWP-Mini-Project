import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector 
import mysql.connector as Error

class RegistrationPage:
    def __init__(self):
        self.win2 = tk.Tk()
        self.win2.title("Registration Page")
        self.win2.geometry("400x350")
        self.win2.state("zoomed")
        self.win2.resizable(0,0)
        self.win2.configure(bg='#2a475e')
        self.lblusr=tk.Label(self.win2,text="Username:", bg='#1b2838', fg='#c7d5e0', font=('Bold',15))
        self.lblusr.pack(pady=10)
        self.usrentry=tk.Entry(self.win2)
        self.usrentry.pack(pady=5)
        
        self.lblpswd=tk.Label(self.win2,text="Password:", bg='#1b2838', fg='#c7d5e0', font=('Bold',15))   
        self.lblpswd.pack(pady=10)
        self.pswdentry=tk.Entry(self.win2,show="*")
        self.pswdentry.pack(pady=5)
        
        self.lblpswdcon=tk.Label(self.win2,text="Confirm Password:", bg='#1b2838', fg='#c7d5e0', font=('Bold',15))   
        self.lblpswdcon.pack(pady=10)
        self.pswdentrycon=tk.Entry(self.win2,show="*")
        self.pswdentrycon.pack(pady=5)
        
        self.btnReg=tk.Button(self.win2,text="Register",command=self.open_tms,bg='#1b2838',
            fg='#c7d5e0',
            font=('Bold', 14),
            bd=0,
            activebackground='#2a475e',
            activeforeground='#c7d5e0')
        self.btnReg.pack(pady=20)
        
        self.btnOpenLogIn=tk.Button(self.win2,text="Already have an account? Login",command=self.open_Login,bg='#1b2838',
            fg='#c7d5e0',
            font=('Bold', 14),
            bd=0,
            activebackground='#2a475e',
            activeforeground='#c7d5e0')
        self.btnOpenLogIn.pack(pady=20)
        
        self.win2.mainloop()

    def connect_db(self):
        """Establishes a connection to the MySQL database."""
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # XAMPP typically uses an empty password by default
                database="dbpro1"  # Make sure this matches your database name in XAMPP
            )
            if con.is_connected():
                return con
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")
            return None
        
    def open_tms(self):
        con=self.connect_db()
        cur=con.cursor()
        self.q="insert into register values(%s,%s)"
        usrnm=self.usrentry.get()
        pswd=self.pswdentry.get()
        pswdcon=self.pswdentrycon.get()
        
        if not usrnm or not pswd or not pswdcon:
            messagebox.showerror("Error", "All fields are required!")
            return
        elif len(pswd) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long!")
            return
        elif pswd != pswdcon:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        else:
            try:
                self.data = (usrnm, pswd)
                cur.execute(self.q, self.data)
                con.commit()
                messagebox.showinfo("Success", "Registration successful!")
                cur.close()
                con.close()
                self.win2.destroy()
                from TMS import TaskManagementSystem
                TaskManagementSystem(current_user=usrnm)
            except mysql.connector.Error as err:
                if err.errno == 1062:  # Duplicate entry error
                    messagebox.showerror("Error", "Account already exists! Please choose a different username or Log In.")
                else:
                    messagebox.showerror("Database Error", f"An error occurred: {err}")
                cur.close()
                con.close()
    
    def open_Login(self):
        self.win2.destroy()
        from Login_Page import LoginPage
        LoginPage()
    
if __name__ == '__main__':
    RegistrationPage()