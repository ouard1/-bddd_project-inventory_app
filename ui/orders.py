import tkinter as tk
from tkinter import Label, Entry, Button, OptionMenu, StringVar,Listbox,messagebox
from logic import orders_crud
from tkinter import ttk 


class OrdersWindow(tk.Toplevel):
    def __init__(self, master):  
        super().__init__(master)
        self.title("Orders")
        self.geometry("400x300")
        customer_names = orders_crud.get_customer_names()
        customer_name_combo = ttk.Combobox(self, values=customer_names)
        customer_name_label = Label(self, text="Customer Name:")
        customer_name_combo.grid(row=0, column=1)
        customer_name_label.grid(row=0, column=0)

        order_date_label = Label(self, text="Order Date (YYYY-MM-DD):")
        order_date_entry = Entry(self)
        order_date_label.grid(row=1, column=0)
        order_date_entry.grid(row=1, column=1)

        status_label = Label(self, text="Status:")
        status_var = StringVar(self)
        status_var.set("placed")  # Default status
        status_options = ['placed', 'fulfilled', 'canceled']
        status_menu = OptionMenu(self, status_var, *status_options)
        status_label.grid(row=2, column=0)
        status_menu.grid(row=2, column=1)

        products = orders_crud.get_products()

        # Product selection
        product_label = Label(self, text="Product:")
        product_var = StringVar(self)
        product_menu = OptionMenu(self, product_var, *products)
        product_label.grid(row=3, column=0)
        product_menu.grid(row=3, column=1)

        # Quantity entry
        quantity_label = Label(self, text="Quantity:")
        quantity_entry = Entry(self)
        quantity_label.grid(row=4, column=0)
        quantity_entry.grid(row=4, column=1)
        
        order_items = []

        item_listbox = Listbox(self)
        item_listbox.grid(row=0, column=6, columnspan=2)
        def add_order_item():
            selected_product = product_var.get()
            quantity = quantity_entry.get()
            # Validate input (check if quantity is a number)
            if quantity.isdigit():
                order_items.append({"product": selected_product, "quantity": int(quantity)})
                update_item_listbox()
                quantity_entry.delete(0, "end")  # Clear quantity entry for next item
        def update_item_listbox():
            item_listbox.delete(0, tk.END)
            for item in order_items:
                item_listbox.insert(tk.END, f"{item['product']} - {item['quantity']}")

               

        def create_full_order():
            selected_customer_name = customer_name_combo.get()

          # Retrieve the corresponding customer ID from the database
            customer_id = orders_crud.get_customer_id(selected_customer_name)
            order_date = order_date_entry.get()
            status = status_var.get()

            if customer_id and order_date:
                order_id = orders_crud.create_order(customer_id, order_date, status)
                for item in order_items:
                    orders_crud.create_order_item(order_id, item["product"], item["quantity"])
                order_items.clear()  
                update_item_listbox()
                messagebox.showinfo("Success", "Order created successfully!")

            
            self.destroy()
                
        # Add item button
        add_item_button = Button(self, text="Add Item", command=add_order_item)
        add_item_button.grid(row=5, column=0, columnspan=2)

        # Create order button
        create_order_button = Button(self, text="Create Order", command=create_full_order)
        create_order_button.grid(row=6, column=0, columnspan=2)
