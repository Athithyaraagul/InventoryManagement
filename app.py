import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psycopg2

class AddProductDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Product")
        self.parent = parent
        
        self.product_id_var = tk.StringVar()
        self.product_type_var = tk.StringVar()
        self.model_id_var = tk.StringVar()
        self.manufacturer_var = tk.StringVar()
        self.department_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.incharge_var = tk.StringVar()
        self.comment_var = tk.StringVar()
        
        # Function to center-align text in entry fields
        center_align = {'justify': 'center'}
        
        tk.Label(self, text="Product ID:").grid(row=0, column=0, sticky="e")
        tk.Entry(self, textvariable=self.product_id_var, **center_align).grid(row=0, column=1)
        tk.Label(self, text="Product Type:").grid(row=1, column=0, sticky="e")
        tk.Entry(self, textvariable=self.product_type_var, **center_align).grid(row=1, column=1)
        tk.Label(self, text="Model ID:").grid(row=2, column=0, sticky="e")
        tk.Entry(self, textvariable=self.model_id_var, **center_align).grid(row=2, column=1)
        tk.Label(self, text="Manufacturer:").grid(row=3, column=0, sticky="e")
        tk.Entry(self, textvariable=self.manufacturer_var, **center_align).grid(row=3, column=1)
        tk.Label(self, text="Department:").grid(row=4, column=0, sticky="e")
        tk.Entry(self, textvariable=self.department_var, **center_align).grid(row=4, column=1)
        tk.Label(self, text="Location:").grid(row=5, column=0, sticky="e")
        tk.Entry(self, textvariable=self.location_var, **center_align).grid(row=5, column=1)
        tk.Label(self, text="Incharge:").grid(row=6, column=0, sticky="e")
        tk.Entry(self, textvariable=self.incharge_var, **center_align).grid(row=6, column=1)
        tk.Label(self, text="Comment:").grid(row=7, column=0, sticky="e")
        tk.Entry(self, textvariable=self.comment_var, **center_align).grid(row=7, column=1)
        
        tk.Button(self, text="Add", command=self.add_product).grid(row=8, columnspan=2, pady=5)
    
    def add_product(self):
        # Get values from entry fields
        product_id = self.product_id_var.get()
        product_type = self.product_type_var.get()
        model_id = self.model_id_var.get()
        manufacturer = self.manufacturer_var.get()
        department = self.department_var.get()
        location = self.location_var.get()
        incharge = self.incharge_var.get()
        comment = self.comment_var.get()
        
        # Check if any field is empty
        if not all([product_id, product_type, model_id, manufacturer, department, location, incharge, comment]):
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return
        
        # Establish connection to PostgreSQL database
        conn = psycopg2.connect(
            dbname="inventorymanagement",
            user="athithyaraagul",
            password="Athithya@2004$$",
            host="localhost",
            port="5000"
        )
        cursor = conn.cursor()

        # Insert data into the table
        cursor.execute("INSERT INTO inventorymanagement (product_id, product_type, model_id, manufacturer, department, location, incharge, comment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                   (product_id, product_type, model_id, manufacturer, department, location, incharge, comment))
        conn.commit()
        conn.close()
        
        # Refresh the treeview in the main window
        self.parent.refresh_treeview()
        
        self.destroy()

class EditProductDialog(tk.Toplevel):
    def __init__(self, parent, product_id):
        super().__init__(parent)
        self.title("Edit Product")
        self.parent = parent
        self.product_id = product_id
        
        # Initialize variables for entry fields
        self.product_type_var = tk.StringVar()
        self.model_id_var = tk.StringVar()
        self.manufacturer_var = tk.StringVar()
        self.department_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.incharge_var = tk.StringVar()
        self.comment_var = tk.StringVar()
        
        # Fetch existing data for the selected product
        self.fetch_product_data()
        
        # Create and layout widgets
        self.create_widgets()
        
    def fetch_product_data(self):
        # Fetch data for the selected product from the database
        conn = psycopg2.connect(
            dbname="inventorymanagement",
            user="athithyaraagul",
            password="Athithya@2004$$",
            host="localhost",
            port="5000"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventorymanagement WHERE product_id=%s", (self.product_id,))
        product_data = cursor.fetchone()
        conn.close()
        
        # Populate entry fields with existing data
        if product_data:
            self.product_type_var.set(product_data[1])
            self.model_id_var.set(product_data[2])
            self.manufacturer_var.set(product_data[3])
            self.department_var.set(product_data[4])
            self.location_var.set(product_data[5])
            self.incharge_var.set(product_data[6])
            self.comment_var.set(product_data[7])
    
    def create_widgets(self):
        # Function to center-align text in entry fields
        center_align = {'justify': 'center'}
        
        # Labels and entry fields
        tk.Label(self, text="Product Type:").grid(row=0, column=0, sticky="e")
        tk.Entry(self, textvariable=self.product_type_var, **center_align).grid(row=0, column=1)
        tk.Label(self, text="Model ID:").grid(row=1, column=0, sticky="e")
        tk.Entry(self, textvariable=self.model_id_var, **center_align).grid(row=1, column=1)
        tk.Label(self, text="Manufacturer:").grid(row=2, column=0, sticky="e")
        tk.Entry(self, textvariable=self.manufacturer_var, **center_align).grid(row=2, column=1)
        tk.Label(self, text="Department:").grid(row=3, column=0, sticky="e")
        tk.Entry(self, textvariable=self.department_var, **center_align).grid(row=3, column=1)
        tk.Label(self, text="Location:").grid(row=4, column=0, sticky="e")
        tk.Entry(self, textvariable=self.location_var, **center_align).grid(row=4, column=1)
        tk.Label(self, text="Incharge:").grid(row=5, column=0, sticky="e")
        tk.Entry(self, textvariable=self.incharge_var, **center_align).grid(row=5, column=1)
        tk.Label(self, text="Comment:").grid(row=6, column=0, sticky="e")
        tk.Entry(self, textvariable=self.comment_var, **center_align).grid(row=6, column=1)
        
        # Button to update product
        tk.Button(self, text="Update", command=self.update_product).grid(row=7, columnspan=2, pady=5)
    
    def update_product(self):
        # Get updated values from entry fields
        product_type = self.product_type_var.get()
        model_id = self.model_id_var.get()
        manufacturer = self.manufacturer_var.get()
        department = self.department_var.get()
        location = self.location_var.get()
        incharge = self.incharge_var.get()
        comment = self.comment_var.get()
        
        # Update the product in the database
        conn = psycopg2.connect(
            dbname="inventorymanagement",
            user="athithyaraagul",
            password="Athithya@2004$$",
            host="localhost",
            port="5000"
        )
        cursor = conn.cursor()
        cursor.execute("UPDATE inventorymanagement SET product_type=%s, model_id=%s, manufacturer=%s, department=%s, location=%s, incharge=%s, comment=%s WHERE product_id=%s",
                       (product_type, model_id, manufacturer, department, location, incharge, comment, self.product_id))
        conn.commit()
        conn.close()
        
        # Refresh the treeview in the main window
        self.parent.refresh_treeview()
        
        self.destroy()

class DeleteProductDialog(tk.Toplevel):
    def __init__(self, parent, product_id):
        super().__init__(parent)
        self.title("Delete Product")
        self.parent = parent
        self.product_id = product_id
        
        # Label to confirm deletion
        label_text = f"Are you sure you want to delete the product with ID: {product_id}?"
        tk.Label(self, text=label_text).pack(pady=10)
        
        # Add buttons for confirmation and cancellation
        tk.Button(self, text="Delete", command=self.delete_product).pack(side=tk.LEFT, padx=10)
        tk.Button(self, text="Cancel", command=self.cancel_deletion).pack(side=tk.RIGHT, padx=10)
    
    def delete_product(self):
        # Delete the product from the database
        conn = psycopg2.connect(
            dbname="inventorymanagement",
            user="athithyaraagul",
            password="Athithya@2004$$",
            host="localhost",
            port="5000"
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventorymanagement WHERE product_id=%s", (self.product_id,))
        conn.commit()
        conn.close()
        
        # Refresh the treeview in the main window
        self.parent.refresh_treeview()
        
        # Close the dialog window
        self.destroy()
    
    def cancel_deletion(self):
        # Close the dialog window without deleting the product
        self.destroy()

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psycopg2

class AddProductDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Product")
        self.parent = parent
        
        self.product_id_var = tk.StringVar()
        self.product_type_var = tk.StringVar()
        self.model_id_var = tk.StringVar()
        self.manufacturer_var = tk.StringVar()
        self.department_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.incharge_var = tk.StringVar()
        self.comment_var = tk.StringVar()
        
        # Function to center-align text in entry fields
        center_align = {'justify': 'center'}
        
        tk.Label(self, text="Product ID:").grid(row=0, column=0, sticky="e")
        tk.Entry(self, textvariable=self.product_id_var, **center_align).grid(row=0, column=1)
        tk.Label(self, text="Product Type:").grid(row=1, column=0, sticky="e")
        tk.Entry(self, textvariable=self.product_type_var, **center_align).grid(row=1, column=1)
        tk.Label(self, text="Model ID:").grid(row=2, column=0, sticky="e")
        tk.Entry(self, textvariable=self.model_id_var, **center_align).grid(row=2, column=1)
        tk.Label(self, text="Manufacturer:").grid(row=3, column=0, sticky="e")
        tk.Entry(self, textvariable=self.manufacturer_var, **center_align).grid(row=3, column=1)
        tk.Label(self, text="Department:").grid(row=4, column=0, sticky="e")
        tk.Entry(self, textvariable=self.department_var, **center_align).grid(row=4, column=1)
        tk.Label(self, text="Location:").grid(row=5, column=0, sticky="e")
        tk.Entry(self, textvariable=self.location_var, **center_align).grid(row=5, column=1)
        tk.Label(self, text="Incharge:").grid(row=6, column=0, sticky="e")
        tk.Entry(self, textvariable=self.incharge_var, **center_align).grid(row=6, column=1)
        tk.Label(self, text="Comment:").grid(row=7, column=0, sticky="e")
        tk.Entry(self, textvariable=self.comment_var, **center_align).grid(row=7, column=1)
        
        tk.Button(self, text="Add", command=self.add_product).grid(row=8, columnspan=2, pady=5)
    
    def add_product(self):
        # Get values from entry fields
        product_id = self.product_id_var.get()
        product_type = self.product_type_var.get()
        model_id = self.model_id_var.get()
        manufacturer = self.manufacturer_var.get()
        department = self.department_var.get()
        location = self.location_var.get()
        incharge = self.incharge_var.get()
        comment = self.comment_var.get()
        
        # Check if any field is empty
        if not all([product_id, product_type, model_id, manufacturer, department, location, incharge, comment]):
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return
        
        # Establish connection to PostgreSQL database
        conn = psycopg2.connect(
            dbname="inventorymanagement",
            user="athithyaraagul",
            password="Athithya@2004$$",
            host="localhost",
            port="5000"
        )
        cursor = conn.cursor()

        # Insert data into the table
        cursor.execute("INSERT INTO inventorymanagement (product_id, product_type, model_id, manufacturer, department, location, incharge, comment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                   (product_id, product_type, model_id, manufacturer, department, location, incharge, comment))
        conn.commit()
        conn.close()
        
        # Refresh the treeview in the main window
        self.parent.refresh_treeview()
        
        self.destroy()

class EditProductDialog(tk.Toplevel):
    def __init__(self, parent, product_id):
        super().__init__(parent)
        self.title("Edit Product")
        self.parent = parent
        self.product_id = product_id
        
        # Initialize variables
        self.product_type_var = tk.StringVar()
        self.model_id_var = tk.StringVar()
        self.manufacturer_var = tk.StringVar()
        self.department_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.incharge_var = tk.StringVar()
        self.comment_var = tk.StringVar()
        
        # Fetch existing data for the selected product
        self.fetch_product_data()
        
        # Create and layout widgets
        self.create_widgets()
        
    def fetch_product_data(self):
        # Fetch data for the selected product from the database
        conn = psycopg2.connect(
            dbname="inventorymanagement",
            user="athithyaraagul",
            password="Athithya@2004$$",
            host="localhost",
            port="5000"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventorymanagement WHERE product_id=%s", (self.product_id,))
        product_data = cursor.fetchone()
        conn.close()
        
        # Populate entry fields with existing data
        if product_data:
            self.product_type_var.set(product_data[1])
            self.model_id_var.set(product_data[2])
            self.manufacturer_var.set(product_data[3])
            self.department_var.set(product_data[4])
            self.location_var.set(product_data[5])
            self.incharge_var.set(product_data[6])
            self.comment_var.set(product_data[7])
    
    def create_widgets(self):
        # Function to center-align text in entry fields
        center_align = {'justify': 'center'}
        
        # Labels and entry fields
        tk.Label(self, text="Product Type:").grid(row=0, column=0, sticky="e")
        tk.Entry(self, textvariable=self.product_type_var, **center_align).grid(row=0, column=1)
        tk.Label(self, text="Model ID:").grid(row=1, column=0, sticky="e")
        tk.Entry(self, textvariable=self.model_id_var, **center_align).grid(row=1, column=1)
        tk.Label(self, text="Manufacturer:").grid(row=2, column=0, sticky="e")
        tk.Entry(self, textvariable=self.manufacturer_var, **center_align).grid(row=2, column=1)
        tk.Label(self, text="Department:").grid(row=3, column=0, sticky="e")
        tk.Entry(self, textvariable=self.department_var, **center_align).grid(row=3, column=1)
        tk.Label(self, text="Location:").grid(row=4, column=0, sticky="e")
        tk.Entry(self, textvariable=self.location_var, **center_align).grid(row=4, column=1)
        tk.Label(self, text="Incharge:").grid(row=5, column=0, sticky="e")
        tk.Entry(self, textvariable=self.incharge_var, **center_align).grid(row=5, column=1)
        tk.Label(self, text="Comment:").grid(row=6, column=0, sticky="e")
        tk.Entry(self, textvariable=self.comment_var, **center_align).grid(row=6, column=1)
        
        # Button to update product
        tk.Button(self, text="Update", command=self.update_product).grid(row=7, columnspan=2, pady=5)
    
    def update_product(self):
        # Get updated values from entry fields
        product_type = self.product_type_var.get()
        model_id = self.model_id_var.get()
        manufacturer = self.manufacturer_var.get()
        department = self.department_var.get()
        location = self.location_var.get()
        incharge = self.incharge_var.get()
        comment = self.comment_var.get()
        
        # Update the product in the database
        conn = psycopg2.connect(
            dbname="inventorymanagement",
            user="athithyaraagul",
            password="Athithya@2004$$",
            host="localhost",
            port="5000"
        )
        cursor = conn.cursor()
        cursor.execute("UPDATE inventorymanagement SET product_type=%s, model_id=%s, manufacturer=%s, department=%s, location=%s, incharge=%s, comment=%s WHERE product_id=%s",
                       (product_type, model_id, manufacturer, department, location, incharge, comment, self.product_id))
        conn.commit()
        conn.close()
        
        # Refresh the treeview in the main window
        self.parent.refresh_treeview()
        
        self.destroy()

class DeleteProductDialog(tk.Toplevel):
    def __init__(self, parent, product_id):
        super().__init__(parent)
        self.title("Delete Product")
        self.parent = parent
        self.product_id = product_id
        
        # Label to confirm deletion
        label_text = f"Are you sure you want to delete the product with ID: {product_id}?"
        tk.Label(self, text=label_text).pack(pady=10)
        
        # Add buttons for confirmation and cancellation
        tk.Button(self, text="Delete", command=self.delete_product).pack(side=tk.LEFT, padx=10)
        tk.Button(self, text="Cancel", command=self.cancel_deletion).pack(side=tk.RIGHT, padx=10)
    
    def delete_product(self):
        # Delete the product from the database
        conn = psycopg2.connect(
            dbname="inventorymanagement",
            user="athithyaraagul",
            password="Athithya@2004$$",
            host="localhost",
            port="5000"
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventorymanagement WHERE product_id=%s", (self.product_id,))
        conn.commit()
        conn.close()
        
        # Refresh the treeview in the main window
        self.parent.refresh_treeview()
        
        # Close the dialog window
        self.destroy()
    
    def cancel_deletion(self):
        # Close the dialog window without deleting the product
        self.destroy()

class InventoryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Management")
        
        # Create treeview widget
        self.tree = ttk.Treeview(self, columns=("Product ID", "Product Type", "Model ID", "Manufacturer", "Department", "Location", "Incharge", "Comment"))
        self.tree.heading('#1', text='Product ID')
        self.tree.heading('#2', text='Product Type')
        self.tree.heading('#3', text='Model ID')
        self.tree.heading('#4', text='Manufacturer')
        self.tree.heading('#5', text='Department')
        self.tree.heading('#6', text='Location')
        self.tree.heading('#7', text='Incharge')
        self.tree.heading('#8', text='Comment')
        
        # Add treeview to window
        self.tree.pack(fill=tk.BOTH, expand=1)
        
        # Add buttons
        add_button = ttk.Button(self, text="Add Product", command=self.open_add_product_dialog)
        add_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        edit_button = ttk.Button(self, text="Edit Product", command=self.edit_product)
        edit_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        delete_button = ttk.Button(self, text="Delete Product", command=self.delete_product)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Add sample data
        self.refresh_treeview()
    
    def open_add_product_dialog(self):
        dialog = AddProductDialog(self)
        dialog.grab_set()  # Prevent interaction with main window while dialog is open
    
    def refresh_treeview(self):
        # Clear existing items in treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Establish connection to PostgreSQL database
        conn = psycopg2.connect(
            dbname="inventorymanagement",
            user="athithyaraagul",
            password="Athithya@2004$$",
            host="localhost",
            port="5000"
        )
        cursor = conn.cursor()

        # Fetch data from the table
        cursor.execute("SELECT * FROM inventorymanagement")
        products = cursor.fetchall()
        conn.close()
        
        # Insert data into treeview
        for product in products:
            self.tree.insert('', 'end', values=product)
    
    def edit_product(self):
        # Get the selected item from the treeview
        selected_item = self.tree.selection()
        
        # Check if an item is selected
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a product to edit.")
            return
        
        # Open a dialog for editing the selected product
        dialog = EditProductDialog(self, selected_item[0])
        dialog.grab_set()  # Prevent interaction with main window while dialog is open
    
    def delete_product(self):
        # Get the selected item from the treeview
        selected_item = self.tree.selection()
        
        # Check if an item is selected
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a product to delete.")
            return
        
        # Open a dialog for confirming deletion
        dialog = DeleteProductDialog(self, selected_item[0])
        dialog.grab_set()  # Prevent interaction with main window while dialog is open

if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()
