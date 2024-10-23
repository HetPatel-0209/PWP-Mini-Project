import tkinter as tk
from tkinter import messagebox
from TMS import TaskManagementSystem

class feedback:
    def __init__(self,current_user):
        # Main application window
        self.winfeed = tk.Tk()
        self.winfeed.title("Feedback Page")
        self.winfeed.geometry("400x400")
        self.winfeed.config(bg="#2a475e")
        self.winfeed.state("zoomed")
        self.winfeed.resizable(0,0)
        self.current_user = current_user
        
        self.head_frame = tk.Frame(self.winfeed,bg='#1b2838',highlightbackground='#c7d5e0',highlightthickness=1)
        self.head_frame.pack(side=tk.TOP,fill=tk.X)
        self.head_frame.pack_propagate(False)
        self.head_frame.configure(height=50)
        self.toggle_btn = tk.Button(self.head_frame,text='☰',bg='#1b2838',fg='#c7d5e0',font=('Bold',20),bd=0,activebackground='#1b2838',activeforeground='#c7d5e0',command=self.toggle_menu) 
        self.toggle_btn.pack(side=tk.LEFT)

        # Create and place the widgets
        self.title_label = tk.Label(self.winfeed, text="Feedback Form", font=("Arial", 16, "bold"), bg="#2a475e", fg="#c7d5e0")
        self.title_label.pack(pady=10)

        # Name entry
        self.name_label = tk.Label(self.winfeed, text="Username:", font=("Arial", 14), bg="#2a475e", fg="#c7d5e0")
        self.name_label.pack(anchor="w", padx=20, pady=(15, 0))
        self.name_entry = tk.Entry(self.winfeed, font=("Arial", 14), width=40)
        self.name_entry.pack(padx=20, pady=5)

        # Feedback text box
        self.feedback_label = tk.Label(self.winfeed, text="Your Feedback:", font=("Arial", 14), bg="#2a475e", fg="#c7d5e0")
        self.feedback_label.pack(anchor="w", padx=20, pady=(15, 0))
        self.feedback_text = tk.Text(self.winfeed, font=("Arial", 14), height=5, width=40)
        self.feedback_text.pack(padx=20, pady=5)

        # Submit button
        self.submit_button = tk.Button(self.winfeed, text="Submit", font=("Arial", 14, "bold"), bg="#1b2838", fg="#c7d5e0", width=15, command=self.submit_feedback)
        self.submit_button.pack(pady=20)
        
        # Start the main loop
        self.winfeed.mainloop()
        
    def toggle_menu(self): 
        """Toggle the side menu."""
        if hasattr(self, 'toggle_menu_fm') and self.toggle_menu_fm.winfo_exists():
            self.collapse_menu()
            return
        
        self.toggle_menu_fm = tk.Frame(self.winfeed, bg='#1b2838')
        self.window_height = self.winfeed.winfo_height()
        self.toggle_menu_fm.place(x=0, y=60, height=self.window_height - 60, width=200)
        
        self.toggle_btn.config(text='X')
        self.toggle_btn.config(command=self.collapse_menu)

        # Side Menu Buttons
        self.home_btn = tk.Button(
            self.toggle_menu_fm,
            text='Home',
            font=('Bold', 16),
            bd=0,
            bg='#1b2838',
            fg='#c7d5e0',
            activebackground='#1b2838',
            activeforeground='#c7d5e0',
            command=self.home
        )
        self.home_btn.place(x=20, y=20)
        
        self.task_btn = tk.Button(
            self.toggle_menu_fm,
            text='Tasks',
            font=('Bold', 16),
            bd=0,
            bg='#1b2838',
            fg='#c7d5e0',
            activebackground='#1b2838',
            activeforeground='#c7d5e0',
            command=self.task_open
        )
        self.task_btn.place(x=20, y=70)
        
        self.Logout_btn = tk.Button(
            self.toggle_menu_fm,
            text='Log Out',
            font=('Bold', 16),
            bd=0,
            bg='#1b2838',
            fg='#c7d5e0',
            activebackground='#1b2838',
            activeforeground='#c7d5e0',
            command=self.open_Login
        )
        self.Logout_btn.place(x=20, y=120)
        
        self.Regist_btn = tk.Button(
            self.toggle_menu_fm,
            text='Register',
            font=('Bold', 16),
            bd=0,
            bg='#1b2838',
            fg='#c7d5e0',
            activebackground='#1b2838',
            activeforeground='#c7d5e0',
            command=self.open_register
        )
        self.Regist_btn.place(x=20, y=170)
        
        self.feedback_btn = tk.Button(
            self.toggle_menu_fm,
            text='Feedback',
            font=('Bold', 16),
            bd=0,
            bg='#1b2838',
            fg='#c7d5e0',
            activebackground='#1b2838',
            activeforeground='#c7d5e0',
            command=self.open_feed
        )
        self.feedback_btn.place(x=20, y=220)
        
    def collapse_menu(self):
        """Collapse the side menu."""
        if hasattr(self, 'toggle_menu_fm') and self.toggle_menu_fm.winfo_exists():
            self.toggle_menu_fm.destroy()        
        self.toggle_btn.config(text='☰')
        self.toggle_btn.config(command=self.toggle_menu)

        # Function to handle the feedback submission
    def submit_feedback(self):
        name = self.name_entry.get()
        feedback = self.feedback_text.get("1.0", tk.END).strip()

        if not name or not feedback:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
        else:
            messagebox.showinfo("Feedback Received", f"Thank you for your feedback, {name}!")
            # Clear all the fields after submission
            self.name_entry.delete(0, tk.END)
            self.feedback_text.delete("1.0", tk.END)
            
    def home(self):
        self.winfeed.destroy()
        TaskManagementSystem(current_user=self.current_user)
        
    def task_open(self):
        self.winfeed.destroy()
        from Task_Page import TaskPage
        TaskPage(current_user=self.current_user)
      
if __name__ == '__main__':
    feedback(current_user="harman")            