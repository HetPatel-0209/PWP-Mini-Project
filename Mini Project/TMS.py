import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
from mysql.connector import Error
from Register_Page import RegistrationPage  # Removed inheritance

class TaskManagementSystem:
    def __init__(self, current_user):
        self.current_user = current_user  # Store the logged-in user
        self.win3 = tk.Tk()
        
        self.win3.title("Task Management System")
        self.win3.geometry("800x600")  # Adjusted for better visibility
        self.win3.configure(bg='#2a475e')
        self.win3.state("zoomed")
        self.win3.resizable(0, 0)
        
        self.groups = {}  # Dictionary to store group data
        
        # Header Frame
        self.head_frame = tk.Frame(self.win3, bg='#1b2838', highlightbackground='#c7d5e0', highlightthickness=1)
        
        self.toggle_btn = tk.Button(
            self.head_frame,
            text='☰',
            bg='#1b2838',
            fg='#c7d5e0',
            font=('Bold', 20),
            bd=0,
            activebackground='#1b2838',
            activeforeground='#c7d5e0',
            command=self.toggle_menu
        )
        self.toggle_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.title_lbl = tk.Label(
            self.head_frame,
            text='MENU',
            bg='#1b2838',
            fg='#c7d5e0',
            font=('Bold', 20)
        )
        self.title_lbl.pack(side=tk.LEFT, padx=10)
        
        self.head_frame.pack(side=tk.TOP, fill=tk.X)
        self.head_frame.pack_propagate(False)
        self.head_frame.configure(height=60)
        
        # Group Listbox
        self.lbgroup = tk.Listbox(
            self.win3,
            bg='#c7d5e0',
            fg='#1b2838',
            font=('Bold', 16),
            bd=1,
            height=10
        )
        self.lbgroup.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.lbgroup.bind("<<ListboxSelect>>", self.show_group_details)
        
        # Group Details Label
        self.lbl = tk.Label(
            self.win3,
            text="",
            bg='#2a475e',
            fg='#c7d5e0',
            font=('Bold', 20)
        )
        self.lbl.pack(pady=5)
        
        # Members Listbox
        self.lbmem = tk.Listbox(
            self.win3,
            bg='#c7d5e0',
            fg='#1b2838',
            font=('Bold', 16),
            bd=1,
            height=10
        )
        self.lbmem.pack(fill=tk.BOTH, expand=True, padx=20, pady=10) 
        
        # Action Buttons Frame
        self.btn_frame = tk.Frame(self.win3, bg='#2a475e')
        self.btn_frame.pack(pady=10)
        
        self.btn_grp_create = tk.Button(
            self.btn_frame,
            text='Create Group',
            command=self.create_group,
            bg='#1b2838',
            fg='#c7d5e0',
            font=('Bold', 14),
            bd=0,
            activebackground='#2a475e',
            activeforeground='#c7d5e0'
        )
        self.btn_grp_create.grid(row=0, column=0, padx=10)
        
        self.btn_add_mem = tk.Button(
            self.btn_frame,
            text='Add Member',
            command=self.add_member,
            bg='#1b2838',
            fg='#c7d5e0',
            font=('Bold', 14),
            bd=0,
            activebackground='#2a475e',
            activeforeground='#c7d5e0'
        )
        self.btn_add_mem.grid(row=0, column=1, padx=10)
        
        self.btn_del_group = tk.Button(
            self.btn_frame,
            text='Delete Group',
            command=self.del_group,
            bg='#1b2838',
            fg='#c7d5e0',
            font=('Bold', 14),
            bd=0,
            activebackground='#2a475e',
            activeforeground='#c7d5e0'
        )
        self.btn_del_group.grid(row=0, column=2, padx=10)
        
        self.btn_remove_mem = tk.Button(
            self.btn_frame,
            text='Remove Member',
            command=self.remove_member,
            bg='#1b2838',
            fg='#c7d5e0',
            font=('Bold', 14),
            bd=0,
            activebackground='#2a475e',
            activeforeground='#c7d5e0'
        )
        self.btn_remove_mem.grid(row=0, column=3, padx=10)
        
        # Initialize Groups from Database
        self.load_groups_from_db()
        
        self.win3.mainloop()
        
    def toggle_menu(self): 
        """Toggle the side menu."""
        if hasattr(self, 'toggle_menu_fm') and self.toggle_menu_fm.winfo_exists():
            self.collapse_menu()
            return
        
        self.toggle_menu_fm = tk.Frame(self.win3, bg='#1b2838')
        self.window_height = self.win3.winfo_height()
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
            command=self.collapse_menu
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
    
    def load_groups_from_db(self):
        """Fetch existing groups and their members from the database and populate the listboxes."""
        con = self.connect_db()
        if not con:
            return
        try:
            cur = con.cursor(dictionary=True)
            # Fetch all groups
            query_groups = "SELECT group_name, leader_name FROM main"
            cur.execute(query_groups)
            groups = cur.fetchall()
            for group in groups:
                group_name = group['group_name']
                leader_name = group['leader_name']
                # Fetch members for each group
                query_members = "SELECT member_name FROM grp_mem WHERE group_name = %s"
                cur.execute(query_members, (group_name,))
                members = [member['member_name'] for member in cur.fetchall()]
                self.groups[group_name] = {"leader": leader_name, "members": members}
                self.lbgroup.insert(tk.END, group_name)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching groups: {err}")
        finally:
            cur.close()
            con.close()
    
    def create_group(self):
        """Create a new group and insert it into the database."""
        group_name = simpledialog.askstring("Create Group", "Enter group name:")
        if group_name:
            con = self.connect_db()
            if not con:
                return
            try:
                cur = con.cursor()
                # Check if group already exists
                check_query = "SELECT COUNT(*) FROM main WHERE group_name = %s"
                cur.execute(check_query, (group_name,))
                count = cur.fetchone()[0]
                if count > 0:
                    messagebox.showerror("Error", f"Group '{group_name}' already exists!")
                    return
                # Assign the current user as the leader
                leader_name = self.current_user
                # Insert new group into main table
                insert_group_query = "INSERT INTO main (group_name, leader_name) VALUES (%s, %s)"
                cur.execute(insert_group_query, (group_name, leader_name))
                # Insert leader into grp_mem
                insert_member_query = "INSERT INTO grp_mem (group_name, member_name) VALUES (%s, %s)"
                cur.execute(insert_member_query, (group_name, leader_name))
                con.commit()
                # Update in-memory groups and listbox
                self.groups[group_name] = {"leader": leader_name, "members": [leader_name]}
                self.lbgroup.insert(tk.END, group_name)
                messagebox.showinfo("Success", f"Group '{group_name}' created with leader '{leader_name}'.")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error creating group: {err}")
            finally:
                cur.close()
                con.close()
    
    def show_group_details(self, event):
        """Display group details when a group is selected."""
        selected_group = self.lbgroup.get(tk.ACTIVE)
        if selected_group:
            group_data = self.groups.get(selected_group, {})
            leader = group_data.get("leader", "N/A")
            self.lbl.config(text=f"Group: {selected_group} (Leader: {leader})")
            self.lbmem.delete(0, tk.END)
            for member in group_data.get("members", []):
                self.lbmem.insert(tk.END, member)
    
    def add_member(self):
        """Add a new member to the selected group. Only the group leader can perform this action."""
        selected_group = self.lbgroup.get(tk.ACTIVE)
        if not selected_group:
            messagebox.showerror("Error", "Please select a group first.")
            return
        
        # Check if the current user is the group leader
        group_data = self.groups.get(selected_group, {})
        leader = group_data.get("leader", "")
        if leader != self.current_user:
            messagebox.showerror("Permission Denied", "Only the group leader can add members.")
            return
        
        new_member = simpledialog.askstring("Add Member", "Enter new member's username:")
        if new_member:
            con = self.connect_db()
            if not con:
                return
            try:
                cur = con.cursor()
                # Verify if new_member exists in register
                verify_member_query = "SELECT COUNT(*) FROM register WHERE user_name = %s"
                cur.execute(verify_member_query, (new_member,))
                member_count = cur.fetchone()[0]
                if member_count == 0:
                    messagebox.showerror("Error", f"User '{new_member}' does not exist. Please register first.")
                    return
                # Check if member is already in the group
                if new_member in self.groups[selected_group]["members"]:
                    messagebox.showwarning("Error", "Member already in the group!")
                    return
                # Insert new member into grp_mem
                insert_member_query = "INSERT INTO grp_mem (group_name, member_name) VALUES (%s, %s)"
                cur.execute(insert_member_query, (selected_group, new_member))
                con.commit()
                # Update in-memory groups and listbox
                self.groups[selected_group]["members"].append(new_member)
                self.lbmem.delete(0, tk.END)
                for member in self.groups[selected_group]["members"]:
                    self.lbmem.insert(tk.END, member)
                messagebox.showinfo("Success", f"Member '{new_member}' added to group '{selected_group}'.")
            except mysql.connector.Error as err:
                if err.errno == 1062:  # Duplicate entry
                    messagebox.showerror("Error", f"Member '{new_member}' is already in the group.")
                else:
                    messagebox.showerror("Database Error", f"Error adding member: {err}")
            finally:
                cur.close()
                con.close()
    
    def del_group(self):
        """Delete the selected group from the database (main and grp_mem tables) and in-memory data."""
        selected_group = self.lbgroup.get(tk.ACTIVE)
        if not selected_group:
            messagebox.showerror("Error", "Please select a group to delete.")
            return
        # Check if the current user is the leader of the group
        group_data = self.groups.get(selected_group, {})
        leader = group_data.get("leader", "")
        if leader != self.current_user:
            messagebox.showerror("Permission Denied", "Only the group leader can delete this group.")
            return
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete group '{selected_group}'?")
        if confirm:
            con = self.connect_db()
            if not con:
                return
            try:
                cur = con.cursor()
                
                # Delete from grp_mem table
                delete_grp_mem_query = "DELETE FROM grp_mem WHERE group_name = %s"
                cur.execute(delete_grp_mem_query, (selected_group,))
                
                # Delete from main table
                delete_main_query = "DELETE FROM main WHERE group_name = %s"
                cur.execute(delete_main_query, (selected_group,))
                
                con.commit()
                
                # Remove from in-memory groups and listbox
                del self.groups[selected_group]
                self.lbgroup.delete(tk.ACTIVE)
                self.lbmem.delete(0, tk.END)
                self.lbl.config(text="")
                messagebox.showinfo("Success", f"Group '{selected_group}' has been deleted from all tables.")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error deleting group: {err}")
            finally:
                cur.close()
                con.close()
    
    def remove_member(self):
        """Remove a member from the selected group. Only the group leader can perform this action."""
        selected_group = self.lbgroup.get(tk.ACTIVE)
        if not selected_group:
            messagebox.showerror("Error", "Please select a group first.")
            return
        
        # Check if the current user is the group leader
        group_data = self.groups.get(selected_group, {})
        leader = group_data.get("leader", "")
        if leader != self.current_user:
            messagebox.showerror("Permission Denied", "Only the group leader can remove members.")
            return
        
        selected_member = self.lbmem.get(tk.ACTIVE)
        if not selected_member:
            messagebox.showerror("Error", "Please select a member to remove.")
            return
        if selected_member == leader:
            messagebox.showwarning("Error", "Cannot remove the group leader.")
            return
        
        confirm = messagebox.askyesno("Confirm Remove", f"Are you sure you want to remove member '{selected_member}' from group '{selected_group}'?")
        if confirm:
            con = self.connect_db()
            if not con:
                return
            try:
                cur = con.cursor()
                delete_member_query = "DELETE FROM grp_mem WHERE group_name = %s AND member_name = %s"
                cur.execute(delete_member_query, (selected_group, selected_member))
                con.commit()
                # Update in-memory groups and listbox
                self.groups[selected_group]["members"].remove(selected_member)
                self.lbmem.delete(tk.ACTIVE)
                messagebox.showinfo("Success", f"Member '{selected_member}' removed from group '{selected_group}'.")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error removing member: {err}")
            finally:
                cur.close()
                con.close()
    
    def open_feed(self):
        """Open the feedback page."""
        self.win3.destroy()
        from Feedback_Page import feedback  # Ensure Feedback_Page.py exists
        feedback(current_user=self.current_user)
        
    def task_open(self):
        """Open the task page."""
        self.win3.destroy()
        from Task_Page import TaskPage  # Ensure Task_Page.py exists
        TaskPage(current_user=self.current_user)
        
    def open_Login(self):
        self.win3.destroy()
        from Login_Page import LoginPage
        LoginPage()
        
    def open_register(self):
        self.win3.destroy()
        from Register_Page import RegistrationPage
        RegistrationPage()                

if __name__ == '__main__':
    TaskManagementSystem(current_user="harman")
