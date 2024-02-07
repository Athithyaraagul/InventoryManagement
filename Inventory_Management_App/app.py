import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class LoginDialog(tk.Toplevel):
    def __init__(self, parent, db_connection):
        super().__init__(parent)
        self.title("Login")
        self.parent = parent
        self.db_connection = db_connection
        
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        tk.Label(self, text="Username:").grid(row=0, column=0, sticky="e")
        tk.Entry(self, textvariable=self.username_var).grid(row=0, column=1)
        tk.Label(self, text="Password:").grid(row=1, column=0, sticky="e")
        tk.Entry(self, textvariable=self.password_var, show="*").grid(row=1, column=1)
        
        tk.Button(self, text="Login", command=self.login).grid(row=2, columnspan=2, pady=5)
    
    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        cursor = self.db_connection.cursor()
        # Modify the SQL query to check both username and password
        cursor.execute('''SELECT * FROM users WHERE username=? AND password=?''', (username, password))
        user = cursor.fetchone()
        if user:
            if user[1] == 'admin':
                self.parent.logged_in_as_admin = True
            else:
                self.parent.logged_in_as_admin = False
            self.parent.update_ui_after_login()  # Update UI after login
            self.destroy()
        else:
            messagebox.showerror("Error", "Invalid username or password")

class InventoryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Management")
        
        db_file_path = '/Users/Athithyaraagul/Developer/Projects/Inventory_Management_App/inventory.db'
        self.db_connection = sqlite3.connect(db_file_path)
        self.logged_in_as_admin = False
        
        self.login_dialog = LoginDialog(self, self.db_connection)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#ffffff", foreground="#333333", fieldbackground="#ffffff")
        style.map("Treeview", background=[("selected", "#007bff")])
        
        self.tree = ttk.Treeview(self, columns=("Product ID", "Product Type", "Model ID", "Manufacturer", "Department", "Location", "Incharge", "Comment"), show="headings", selectmode="browse")
        self.tree.heading('Product ID', text='Product ID')
        self.tree.heading('Product Type', text='Product Type')
        self.tree.heading('Model ID', text='Model ID')
        self.tree.heading('Manufacturer', text='Manufacturer')
        self.tree.heading('Department', text='Department')
        self.tree.heading('Location', text='Location')
        self.tree.heading('Incharge', text='Incharge')
        self.tree.heading('Comment', text='Comment')
        
        self.tree.pack(fill=tk.BOTH, expand=1)
        
        self.add_button = ttk.Button(self, text="Add Product", command=self.open_add_product_dialog, state=tk.DISABLED)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        edit_button = ttk.Button(self, text="Edit Product", command=self.edit_product)
        edit_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        delete_button = ttk.Button(self, text="Delete Product", command=self.delete_product)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.load_data_from_database()
    
    def update_ui_after_login(self):
        self.tree.delete(*self.tree.get_children())
        self.load_data_from_database()
        
        if self.logged_in_as_admin:
            self.add_button.config(state=tk.NORMAL)
    
    def open_add_product_dialog(self):
        dialog = AddProductDialog(self, self.db_connection)
        dialog.grab_set()  # Prevent interaction with main window while dialog is open
    
    def load_data_from_database(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''SELECT * FROM products''')
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert('', 'end', values=row)
    
    def edit_product(self):
        pass
    
    def delete_product(self):
        pass

if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()
