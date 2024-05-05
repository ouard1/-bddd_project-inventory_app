import tkinter as tk
from tkinter import Label, Entry, Button, OptionMenu, StringVar,Listbox,messagebox
from logic import orders_crud
from tkinter import ttk 


class OrdersWindow(tk.Toplevel):
    def __init__(self, master):  
        super().__init__(master)
        self.title("Orders")
        
        window_width = 550
        window_height = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.configure(background="#EAEAF4")

        # Create a frame for the content
        content_frame= tk.Frame(self, bg="#fafaff")
        content_frame.pack(padx=20, pady=20, fill="both", expand=True)

        customer_names = orders_crud.get_customer_names()
        customer_name_combo = ttk.Combobox(content_frame, values=customer_names)
        customer_name_label = Label(content_frame, text="Customer Name:",anchor="w",background="#fafaff")
        customer_name_combo.grid(row=0, column=1 , sticky="ew",pady=10,padx=7)
        customer_name_label.grid(row=0, column=0 ,pady=10,padx=20,sticky="ew")

        order_date_label = Label(content_frame, text="Order Date (YYYY-MM-DD):",anchor="w",background="#fafaff")
        order_date_entry = Entry(content_frame)
        order_date_label.grid(row=1, column=0,pady=4,padx=20,sticky="ew")
        order_date_entry.grid(row=1, column=1 ,pady=4,padx=7,sticky="ew")

        status_label = Label(content_frame, text="Status:",anchor="w",background="#fafaff")
        status_var = StringVar(content_frame)
        status_var.set("select status")  # Default status
        status_options = ['placed', 'fulfilled', 'canceled']
        status_menu = OptionMenu(content_frame, status_var, *status_options)
        status_menu.configure(background="#EAEAF4", activebackground="#EAEAF4")
        status_label.grid(row=2, column=0,pady=4,padx=20,sticky="ew")
        status_menu.grid(row=2, column=1 ,pady=4,padx=7,sticky="ew")

        products = orders_crud.get_products()

        # Product selection
        product_label = Label(content_frame, text="Product:",anchor="w",background="#fafaff")
        product_var = StringVar(content_frame)
        product_var.set("select product")
        product_menu = OptionMenu(content_frame, product_var, *products)
        product_menu.configure(background="#EAEAF4",activebackground="#EAEAF4")
        product_label.grid(row=3, column=0,pady=4,padx=20,sticky="ew")
        product_menu.grid(row=3, column=1 ,pady=4,padx=7,sticky="ew")

        # Quantity entry
        quantity_label = Label(content_frame, text="Quantity:",anchor="w",background="#fafaff")
        quantity_entry = Entry(content_frame)
        quantity_label.grid(row=4, column=0,pady=4,padx=20,sticky="ew")
        quantity_entry.grid(row=4, column=1 ,pady=4,padx=7,sticky="ew")
        
        order_items = []

        item_listbox = Listbox(content_frame)
        item_listbox.grid(row=0, column=12, columnspan=4 ,rowspan=7,padx= 20)
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

            
            content_frame.destroy()
                
        # Add item button
        add_item_button = Button(content_frame, text="Add Item", command=add_order_item,background="#EAEAF4",borderwidth=1,relief="raised")
        add_item_button.grid(row=5, column=0, columnspan=2,sticky="ew",pady=6,padx=12)

        # Create order button
        create_order_button = Button(content_frame, text="Create Order", command=create_full_order,background="#119DA4",borderwidth=1,relief="raised")
        create_order_button.grid(row=6, column=0, columnspan=2,sticky="ew",pady=6,padx=12)
