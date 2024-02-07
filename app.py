import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

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
        
        tk.Label(self, text="Product ID:").grid(row=0, column=0, sticky="e")
        tk.Entry(self, textvariable=self.product_id_var).grid(row=0, column=1)
        tk.Label(self, text="Product Type:").grid(row=1, column=0, sticky="e")
        tk.Entry(self, textvariable=self.product_type_var).grid(row=1, column=1)
        tk.Label(self, text="Model ID:").grid(row=2, column=0, sticky="e")
        tk.Entry(self, textvariable=self.model_id_var).grid(row=2, column=1)
        tk.Label(self, text="Manufacturer:").grid(row=3, column=0, sticky="e")
        tk.Entry(self, textvariable=self.manufacturer_var).grid(row=3, column=1)
        tk.Label(self, text="Department:").grid(row=4, column=0, sticky="e")
        tk.Entry(self, textvariable=self.department_var).grid(row=4, column=1)
        tk.Label(self, text="Location:").grid(row=5, column=0, sticky="e")
        tk.Entry(self, textvariable=self.location_var).grid(row=5, column=1)
        tk.Label(self, text="Incharge:").grid(row=6, column=0, sticky="e")
        tk.Entry(self, textvariable=self.incharge_var).grid(row=6, column=1)
        tk.Label(self, text="Comment:").grid(row=7, column=0, sticky="e")
        tk.Entry(self, textvariable=self.comment_var).grid(row=7, column=1)
        
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
        
        # Add the product to the SQLite database
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("INSERT INTO products (product_id, product_type, model_id, manufacturer, department, location, incharge, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (product_id, product_type, model_id, manufacturer, department, location, incharge, comment))
        conn.commit()
        conn.close()
        
        # Refresh the treeview in the main window
        self.parent.refresh_treeview()
        
        self.destroy()

class InventoryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Management")
        
        self.tree = ttk.Treeview(self, columns=("Product ID", "Product Type", "Model ID", "Manufacturer", "Department", "Location", "Incharge", "Comment"))
        self.tree.heading('#0', text='ID')
        self.tree.heading('#1', text='Product ID')
        self.tree.heading('#2', text='Product Type')
        self.tree.heading('#3', text='Model ID')
        self.tree.heading('#4', text='Manufacturer')
        self.tree.heading('#5', text='Department')
        self.tree.heading('#6', text='Location')
        self.tree.heading('#7', text='Incharge')
        self.tree.heading('#8', text='Comment')
        
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
        
        # Load data from SQLite database
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        products = c.fetchall()
        conn.close()
        
        # Insert data into treeview
        for product in products:
            self.tree.insert('', 'end', values=product)
    
    def edit_product(self):
        # Implement logic to edit a product
        pass
    
    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a product to delete.")
            return
        confirmed = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected product?")
        if confirmed:
            # Delete the product from the SQLite database
            conn = sqlite3.connect('inventory.db')
            c = conn.cursor()
            c.execute("DELETE FROM products WHERE rowid=?", (selected_item[0],))
            conn.commit()
            conn.close()
            
            # Refresh the treeview
            self.refresh_treeview()
            messagebox.showinfo("Deleted", "Product deleted successfully.")
        else:
            messagebox.showinfo("Cancelled", "Deletion cancelled.")

# Create SQLite database and table if they don't exist
conn = sqlite3.connect('inventory.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS products
             (product_id TEXT, product_type TEXT, model_id TEXT, manufacturer TEXT, department TEXT, location TEXT, incharge TEXT, comment TEXT)''')
conn.commit()
conn.close()

if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()
