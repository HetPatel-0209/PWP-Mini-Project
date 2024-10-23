import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from Feedback_Page import feedback
from TMS import TaskManagementSystem
import mysql.connector 
import os
import shutil

class TaskPage():
    def __init__(self, current_user):
        self.wintask = tk.Tk()
        self.wintask.title("Task Page")
        self.wintask.geometry("400x350")
        self.wintask.configure(bg='#2a475e')
        self.wintask.state("zoomed")
        self.wintask.resizable(0,0)
        self.current_user = current_user
        
        # Database connection
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dbpro1"
        )
        self.db_cursor = self.db_connection.cursor()
        
        # UI setup (head frames, buttons, etc.)
        self.setup_ui()
        
        self.load_groups()
        
        self.wintask.mainloop()
    
    def setup_ui(self):
        # Head frame setup
        self.head_frame = tk.Frame(self.wintask, bg='#1b2838', highlightbackground='#c7d5e0', highlightthickness=1)
        self.toggle_btn = tk.Button(self.head_frame, text='☰', bg='#1b2838', fg='#c7d5e0', font=('Bold',20), bd=0, activebackground='#1b2838', activeforeground='#c7d5e0', command=self.toggle_menu)
        self.toggle_btn.pack(side=tk.LEFT)
        self.title_lbl = tk.Label(self.head_frame, text='MENU', bg='#1b2838', fg='#c7d5e0', font=('Bold',20))
        self.title_lbl.pack(side=tk.LEFT)
        self.head_frame.pack(side=tk.TOP, fill=tk.X)
        self.head_frame.pack_propagate(False)
        self.head_frame.configure(height=50)
        
        # Main content frame
        self.content_frame = tk.Frame(self.wintask, bg='#1b2838', highlightbackground='#c7d5e0', highlightthickness=1)
        self.content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Group list
        self.lblgrp = tk.Label(self.content_frame, text="Group List:", bg='#1b2838', fg='#c7d5e0', font=('Bold',15))
        self.lblgrp.pack(padx=1, pady=1)
        self.lbgroup = tk.Listbox(self.content_frame, bg='#c7d5e0', fg='#1b2838', font=('Bold',16), bd=1, height=5)
        self.lbgroup.pack(padx=5, pady=5, expand=True, fill=tk.BOTH)
        self.lbgroup.bind('<<ListboxSelect>>', self.on_group_select)
        
        # Member list
        self.lblmem = tk.Label(self.content_frame, text="Member List:", bg='#1b2838', fg='#c7d5e0', font=('Bold',15))
        self.lblmem.pack(padx=1, pady=1)
        self.lbmem = tk.Listbox(self.content_frame, bg='#c7d5e0', fg='#1b2838', font=('Bold',16), bd=1, height=5)
        self.lbmem.pack(padx=5, pady=5, expand=True, fill=tk.BOTH)
        self.lbmem.bind('<<ListboxSelect>>', self.on_member_select)
        
        # Task list
        self.lbltask = tk.Label(self.content_frame, text="Task List:", bg='#1b2838', fg='#c7d5e0', font=('Bold',15))
        self.lbltask.pack(padx=1, pady=1)
        self.lbtask = tk.Listbox(self.content_frame, bg='#c7d5e0', fg='#1b2838', font=('Bold',16), bd=1, height=5)
        self.lbtask.pack(padx=5, pady=5, expand=True, fill=tk.BOTH)
        
        # Buttons
        self.btn_allo_task = tk.Button(self.content_frame, text="Allocate Task", command=self.allo_task,bg='#1b2838',
            fg='#c7d5e0',
            font=('Bold', 14),
            bd=1,
            activebackground='#2a475e',
            activeforeground='#c7d5e0')
        self.btn_del_task = tk.Button(self.content_frame, text="Delete Task", command=self.del_task,bg='#1b2838',
            fg='#c7d5e0',
            font=('Bold', 14),
            bd=1,
            activebackground='#2a475e',
            activeforeground='#c7d5e0')
        self.btn_open_task = tk.Button(self.content_frame, text="Open Task", command=self.open_task,bg='#1b2838',
            fg='#c7d5e0',
            font=('Bold', 14),
            bd=1,
            activebackground='#2a475e',
            activeforeground='#c7d5e0')
        self.btn_com_task = tk.Button(self.content_frame, text="Complete Task", command=self.com_task,bg='#1b2838',
            fg='#c7d5e0',
            font=('Bold', 14),
            bd=1,
            activebackground='#2a475e',
            activeforeground='#c7d5e0')
        
        self.btn_allo_task.pack(side=tk.RIGHT, padx=10, pady=1)
        self.btn_del_task.pack(side=tk.RIGHT, padx=10, pady=1)
        self.btn_open_task.pack(side=tk.RIGHT, padx=10, pady=1)
        self.btn_com_task.pack(side=tk.RIGHT, padx=10, pady=1)

    def load_groups(self):
        self.lbgroup.delete(0, tk.END)
        self.db_cursor.execute("SELECT group_name FROM main")
        groups = self.db_cursor.fetchall()
        for group in groups:
            self.lbgroup.insert(tk.END, group[0])
            
    def on_group_select(self, event):
        self.lbmem.delete(0, tk.END)
        self.lbtask.delete(0, tk.END)
        selected_group = self.lbgroup.get(tk.ACTIVE)
        if selected_group:
            self.db_cursor.execute("SELECT member_name FROM grp_mem WHERE group_name = %s", (selected_group,))
            members = self.db_cursor.fetchall()
            for member in members:
                self.lbmem.insert(tk.END, member[0])

    def on_member_select(self, event):
        selected_group = self.lbgroup.get(tk.ACTIVE)
        selected_member = self.lbmem.get(tk.ACTIVE)
        if selected_group and selected_member:
            self.load_tasks(selected_group, selected_member)

    def load_tasks(self, group, member):
        self.lbtask.delete(0, tk.END)
        self.db_cursor.execute("""
            SELECT task_name FROM task 
            WHERE group_name = %s AND mem_name = %s
        """, (group, member))
        tasks = self.db_cursor.fetchall()
        for task in tasks:
            self.lbtask.insert(tk.END, task[0])

    def allo_task(self):
        selected_group = self.lbgroup.get(tk.ACTIVE)
        selected_member = self.lbmem.get(tk.ACTIVE)
        
        if not selected_group or not selected_member:
            messagebox.showerror("Error", "Please select a group and a member.")
            return
        
        # Check if the current user is the group leader
        self.db_cursor.execute("SELECT leader_name FROM main WHERE group_name = %s", (selected_group,))
        leader = self.db_cursor.fetchone()
        
        if leader and leader[0] == self.current_user:
            if selected_member == leader[0]:
                messagebox.showerror("Error", "Leaders cannot allocate tasks to themselves.")
                return
            
            # Open file dialog to select a file
            file_path = filedialog.askopenfilename()
            if file_path:
                file_name = os.path.basename(file_path)
                
                # Insert task information into the database
                self.db_cursor.execute("""
                    INSERT INTO task (group_name, mem_name, task_path, task_name)
                    VALUES (%s, %s, %s, %s)
                """, (selected_group, selected_member, file_path, file_name))
                self.db_connection.commit()
                
                if self.db_cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Task allocated successfully.")
                    self.load_tasks(selected_group, selected_member)
                else:
                    messagebox.showerror("Error", "Failed to allocate task.")
            else:
                messagebox.showerror("Error", "No file selected.")
        else:
            messagebox.showerror("Error", "Only the group leader can allocate tasks.")

    def open_task(self):
        selected_group = self.lbgroup.get(tk.ACTIVE)
        selected_member = self.lbmem.get(tk.ACTIVE)
        selected_task = self.lbtask.get(tk.ACTIVE)
        
        if not selected_group or not selected_member or not selected_task:
            messagebox.showerror("Error", "Please select a group, member, and task.")
            return
        
        # Check if the current user is the group leader or the assigned member
        self.db_cursor.execute("SELECT leader_name FROM main WHERE group_name = %s", (selected_group,))
        leader = self.db_cursor.fetchone()
        
        if leader and (leader[0] == self.current_user or selected_member == self.current_user):
            # Retrieve the task file path
            self.db_cursor.execute("""
                SELECT task_path FROM task 
                WHERE group_name = %s AND mem_name = %s AND task_name = %s
            """, (selected_group, selected_member, selected_task))
            task_path = self.db_cursor.fetchone()
            
            if task_path:
                try:
                    os.startfile(task_path[0])
                except:
                    messagebox.showerror("Error", "Unable to open the file.")
            else:
                messagebox.showerror("Error", "Task file not found.")
        else:
            messagebox.showerror("Error", "You don't have permission to open this task.")

    def com_task(self):
        selected_group = self.lbgroup.get(tk.ACTIVE)
        selected_member = self.lbmem.get(tk.ACTIVE)
        selected_task = self.lbtask.get(tk.ACTIVE)
        
        if not selected_group or not selected_member or not selected_task:
            messagebox.showerror("Error", "Please select a group, member, and task.")
            return
        
        # Check if the current user is the group leader or the assigned member
        self.db_cursor.execute("SELECT leader_name FROM main WHERE group_name = %s", (selected_group,))
        leader = self.db_cursor.fetchone()
        
        if leader[0] == self.current_user:  # Leader action
            if messagebox.askyesno("Confirm", "Do you want to mark this task as completed?"):
                self.db_cursor.execute("""
                    DELETE FROM task 
                    WHERE group_name = %s AND mem_name = %s AND task_name = %s
                """, (selected_group, selected_member, selected_task))
                self.db_connection.commit()
                messagebox.showinfo("Success", "Task finished and removed from the list.")
                self.load_tasks(selected_group, selected_member)
            else:
                self.db_cursor.execute("""
                    DELETE FROM task 
                    WHERE group_name = %s AND mem_name = %s AND task_name = %s
                """, (selected_group, selected_member, selected_task))
                self.db_connection.commit()
                messagebox.showinfo("Rejected", "Task solution rejected. The task will be reallocated.")
                # Here you would add logic to revert the task to its original state if needed
                file_path = filedialog.askopenfilename()
                if file_path:
                    file_name = os.path.basename(file_path)
                    
                    # Insert task information into the database
                    self.db_cursor.execute("""
                        INSERT INTO task (group_name, mem_name, task_path, task_name)
                        VALUES (%s, %s, %s, %s)
                    """, (selected_group, selected_member, file_path, file_name))
                    self.db_connection.commit()
                    
                    if self.db_cursor.rowcount > 0:
                        messagebox.showinfo("Success", "Task reallocated successfully.")
                        self.load_tasks(selected_group, selected_member)
                    else:
                        messagebox.showerror("Error", "Failed to reallocate task.")
                else:
                    messagebox.showerror("Error", "No file selected.")
        elif selected_member == self.current_user:  # Member action
            if messagebox.askyesno("Confirm", "Do you want to submit the completed task?"):
                new_file_path = filedialog.askopenfilename()
                if new_file_path:
                    new_file_name = os.path.basename(new_file_path)
                    self.db_cursor.execute("""
                        UPDATE task 
                        SET task_path = %s, task_name = %s
                        WHERE group_name = %s AND mem_name = %s AND task_name = %s
                    """, (new_file_path, new_file_name, selected_group, selected_member, selected_task))
                    self.db_connection.commit()
                    messagebox.showinfo("Success", "Task updated successfully.")
                    self.load_tasks(selected_group, selected_member)
                else:
                    messagebox.showerror("Error", "No file selected.")
        else:
            messagebox.showerror("Error", "You don't have permission to complete this task.")

    def del_task(self):
        selected_group = self.lbgroup.get(tk.ACTIVE)
        selected_member = self.lbmem.get(tk.ACTIVE)
        selected_task = self.lbtask.get(tk.ACTIVE)

        if not selected_group or not selected_member or not selected_task:
            messagebox.showerror("Error", "Please select a group, member, and task.")
            return

        # Check if the current user is the leader of the group
        self.db_cursor.execute("SELECT leader_name FROM main WHERE group_name = %s", (selected_group,))
        leader = self.db_cursor.fetchone()

        if leader and leader[0] == self.current_user:
            # Delete the task from the database
            self.db_cursor.execute("""
                DELETE FROM task
                WHERE group_name = %s AND mem_name = %s AND task_name = %s
            """, (selected_group, selected_member, selected_task))
            self.db_connection.commit()

            if self.db_cursor.rowcount > 0:
                messagebox.showinfo("Success", "Task deleted successfully.")
                self.load_tasks(selected_group, selected_member)
            else:
                messagebox.showerror("Error", "Failed to delete the task. Please try again.")
        else:
            messagebox.showerror("Error", "Only the group leader can delete tasks.")
                                                    
    def toggle_menu(self): 
        """Toggle the side menu."""
        if hasattr(self, 'toggle_menu_fm') and self.toggle_menu_fm.winfo_exists():
            self.collapse_menu()
            return
        
        self.toggle_menu_fm = tk.Frame(self.wintask, bg='#1b2838')
        self.window_height = self.wintask.winfo_height()
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
            command=self.open_home
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
            command=self.collapse_menu
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
        
    def open_home(self):
        self.wintask.destroy()
        TaskManagementSystem(current_user=self.current_user)
            
    def open_feed(self):
        self.wintask.destroy()
        from Feedback_Page import feedback
        feedback()
        
    def open_Login(self):
        self.wintask.destroy()
        from Login_Page import LoginPage
        LoginPage()
        
    def open_register(self):
        self.wintask.destroy()
        from Register_Page import RegistrationPage
        RegistrationPage()        

if __name__ == '__main__':
    TaskPage(current_user="harman")    