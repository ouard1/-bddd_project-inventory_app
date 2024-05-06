from datetime import datetime
import tkinter as tk
import tkintermapview
import sys 
sys.path.append('../') 

import os
from clients import ClientsWindow
from tkinter import ttk, CENTER,Toplevel,Button,Entry,Label
from suppliers import SuppliersWindow
from inventoryItems import ItemsWindow
from logic import analytics
from logic import mongodb_database
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from orders import OrdersWindow
from customtkinter import CTk,CTkComboBox,CTkFrame,CTkButton,CTkLabel,CTkCanvas,CTkImage
from PIL import Image,ImageTk




class MainWindow(CTk):
    def __init__(self):
        super().__init__()
       
        self.title("Main Window")
        self.geometry("1100x700") 
        style =ttk.Style()
        style.theme_use("default")
        
        
        num_rows = 8
        num_cols = 13
        cell_size = 83  # Pixels

        # Configure rows
        for i in range(num_rows):
            self.rowconfigure(i, weight=1, minsize=cell_size)

        # Configure columns
        for i in range(num_cols):
            self.columnconfigure(i, weight=1, minsize=cell_size)

       # Buttons on the sidebar
        sidebar_frame =  CTkFrame(self, fg_color="#6665DD")
        sidebar_frame.grid(column=0,columnspan=2,row=0,rowspan=12,sticky='nsew')

      
        

        header_frame =  CTkFrame(self,fg_color="#FAFAFF")
        header_frame.grid(column=2,columnspan=11,row=0,sticky='nsew')
        home_label = CTkLabel(
         header_frame, text="Home", font=("Arial", 25, "bold"),fg_color='#FAFAFF')
        home_label.pack(side='left',ipadx=30)

        supplier_image = ImageTk.PhotoImage(Image.open("C:/Users/ouarda/Desktop/bddd projet/inventory management system/ui/media/Image (3).png").resize((20,20)))
        orders_image =ImageTk.PhotoImage(Image.open("C:/Users/ouarda/Desktop/bddd projet/inventory management system/ui/media/Image.png").resize((20,20)))
        clients_image =ImageTk.PhotoImage(Image.open("C:/Users/ouarda/Desktop/bddd projet/inventory management system/ui/media/Image (5).png").resize((20,21)))
        items_image =ImageTk.PhotoImage(Image.open("C:/Users/ouarda/Desktop/bddd projet/inventory management system/ui/media/Image (4).png").resize((20,20)))
    
        suppliers_button = CTkButton(sidebar_frame,image=supplier_image, text="Suppliers", command=self.show_suppliers,hover=False,text_color="#1C1C1C",fg_color='transparent',compound="left",width=83,corner_radius=0,anchor="w",border_spacing=8)
        suppliers_button.grid(row=7 , column=0,columnspan=2,sticky='nsew',padx=40,pady=10)

        clients_button = CTkButton(sidebar_frame, image=clients_image,text="Clients", command=self.show_clients,hover=False,text_color="#1C1C1C",fg_color='transparent',compound="left",width=83,anchor="w",border_spacing=8,corner_radius=0)
        clients_button.grid(row=8 , column=0,columnspan=2,sticky='nsew',padx=40,pady=10)

        items_button = CTkButton(sidebar_frame, text="Inventory", image=items_image,command=self.show_items,hover=False,text_color="#1C1C1C",fg_color='transparent',compound="left",width=83,corner_radius=0,anchor="w",border_spacing=8)
        items_button.grid(row=9, column=0,columnspan=2,sticky='nsew',padx=40,pady=10)

        orders_button = CTkButton(sidebar_frame, text=" Orders", image=orders_image,command=self.show_orders,hover=False,text_color="#1C1C1C",fg_color='transparent',compound="left",width=83,corner_radius=0,anchor="w",border_spacing=8)
        orders_button.grid(row=10, column=0,columnspan=2,sticky='nsew',padx=40,pady=10)


       
       

        num_rows = 2
        num_cols = 2
        cell_size = 400  
        content_frame = CTkFrame(self, fg_color="#EAEAF4")
        content_frame.grid(row=1, column=2, columnspan=11, rowspan=8, sticky='nsew')
        for i in range(num_rows):
            content_frame.grid_rowconfigure(i, weight=1)
        for i in range(num_cols):
            content_frame.grid_columnconfigure(i, weight=1)

        # Create and position the 4 frames
        padding = 10 # Adjust padding between frames as desired

        analytics_frame = CTkFrame(content_frame, fg_color="#FAFAFF", corner_radius=16)
        analytics_frame.grid(row=0, column=0, padx=padding, pady=padding, sticky="nsew")
        sales_performance_frame = CTkFrame(content_frame, fg_color="#FAFAFF", corner_radius=16)
        sales_performance_frame.grid(row=0, column=1, columnspan= 2,padx=padding, pady=padding, sticky="nsew")
        map_frame = CTkFrame(content_frame, fg_color="#FAFAFF", corner_radius=16)
        map_frame.grid(row=1, column=0, columnspan=2, padx=padding, pady=padding, sticky="nsew")
        low_stock_frame = CTkFrame(content_frame, fg_color="#FAFAFF", corner_radius=16)
        low_stock_frame.grid(row=1, column=2, columnspan=1, padx=padding, pady=padding, sticky="nsew")


        

        def convert_decimal_to_float(item):
            return {'item_name': item['item_name'], 'total_quantity': float(item['total_quantity'])}

        

      

        analytics_title_label = CTkLabel(analytics_frame, text="Top Selling Items",font=("Arial", 14, "bold"))
        analytics_title_label.grid(pady=5)

        top_selling_items = analytics.calculate_top_selling_items()

        item_names = [item['item_name'] for item in top_selling_items]
        total_quantities = [item['total_quantity'] for item in top_selling_items]

        fig = Figure(figsize=(5, 3),facecolor="#FAFAFF")
        ax = fig.add_subplot(111)
        colors = ["#EAEAF4", "#6665DD", "#119DA4", "#230C33", "black", "white"]
        
        def autopct_format(value):
            return f'{value:.1f}%'

        ax.pie(total_quantities, labels=item_names, autopct=autopct_format, startangle=140, colors=colors, pctdistance=1.5)
        ax.axis('equal')

        canvas = FigureCanvasTkAgg(fig, master=analytics_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(sticky="nsew")
        def mongodb_store_analytics(top_selling_items):
            top_selling_items = [convert_decimal_to_float(item) for item in top_selling_items]

            timestamp = datetime.now()
            analytics_data = {
                'timestamp': timestamp,
                'top_selling_items': top_selling_items
            }
            # Store analytics data in MongoDB
            mongodb_database.insert_analytics(analytics_data)

        mongodb_store_analytics(top_selling_items)

        # Title for sales performance
        sales_performance_title_label = CTkLabel(sales_performance_frame, text="Sales Performance",
                                                  font=("Arial", 14, "bold"),)
        sales_performance_title_label.grid()

        # Define the desired period (e.g., last 7 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        orders_data = analytics.fetch_orders_data(start_date, end_date)
        mongodb_database.insert_daily_sales_data(orders_data)
# Extract dates and revenue from orders data
        dates = [order['order_date'] for order in orders_data]
        revenue = [order['total_revenue'] for order in orders_data]

        # Visualize sales trends
        fig_sales = Figure(figsize=(5, 3),facecolor="#FAFAFF",layout="tight")
        ax_sales = fig_sales.add_subplot(111)
        ax_sales.plot(dates, revenue, marker='o', color='#230C33')
        ax_sales.set_xlabel('Date')
        ax_sales.set_ylabel('Total Sales Revenue')
        ax_sales.set_title('Sales Trends')
        ax_sales.xaxis.set_tick_params(rotation=45)
        ax_sales.grid(True)

        # Embed the plot into a Tkinter canvas
        canvas_sales = FigureCanvasTkAgg(fig_sales, master=sales_performance_frame)
        canvas_sales.draw()
        canvas_sales.get_tk_widget().grid(pady=10)
        
        # Add a map widget
        map_widget = tkintermapview.TkinterMapView(map_frame, width=540, height=366,corner_radius=16)
        map_widget.set_address("algeria")
        map_widget.set_zoom(3)
        map_widget.pack(side="left",pady=3)

        # Function to add markers to the map
        def add_markers_to_map():
            # Retrieve supplier coordinates from the database
            supplier_coordinates = mongodb_database.get_supplier_coordinates()

            # Create markers for each supplier coordinate
            for coordinates in supplier_coordinates:
                latitude, longitude = coordinates
                map_widget.set_marker(latitude, longitude)

        # Call the function to add markers to the map
        add_markers_to_map()
        

        # Title for low stock items
        low_stock_title_label = CTkLabel(low_stock_frame, text="Low Stock Items",
                                         font=("Arial", 14, "bold"))
        low_stock_title_label.grid(pady=10)

        # Create a Listbox for displaying low stock items
     
        low_stock_listbox = tk.Listbox(low_stock_frame, width=86, height=10,bg="#FAFAFF",highlightcolor= "#6665DD")
        low_stock_listbox.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")  # Adjust padding and alignment


        # Function to populate low stock items in the Listbox
        def populate_low_stock_items():
            reorder_point = 10  # Set your reorder point threshold here
            low_stock_items =analytics.get_items_below_quantity(reorder_point)
            mongodb_database.store_low_stock_items(low_stock_items)
            for item in low_stock_items:
                low_stock_listbox.insert(tk.END, f"{item['name']} - Quantity: {item['quantity']}")

        # Call the function to populate low stock items
        populate_low_stock_items()
        

        
    def show_suppliers(self):
        suppliers_window = SuppliersWindow(self)
        suppliers_window.title("Suppliers")
        suppliers_window.geometry("1000x500")
        suppliers_window.grab_set()

    def show_clients(self):
        clients_window = ClientsWindow(self)
        clients_window.title("Clients")
        clients_window.geometry("1000x500")
        clients_window.grab_set()
    def show_items(self):
        clients_window = ItemsWindow(self)
        clients_window.title("Items")
        clients_window.geometry("1000x500")
        clients_window.grab_set()
    def show_orders(self):
        orders= OrdersWindow(self)  # Pass self as the master
        orders.title("Orders")
        orders.grab_set()

       


if __name__ == "__main__":
   
    app = MainWindow()
    

    app.mainloop()

