from datetime import datetime
import tkinter as tk
import tkintermapview
import sys 
sys.path.append('../') 

from ui import clients,suppliers
from clients import ClientsWindow
from tkinter import ttk, messagebox
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


#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
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Main Window")
        self.geometry("1000x500") 
        style =ttk.Style()
        style.theme_use("default")
        sidebar_frame = tk.Frame(self, bg="lightgrey", width=100)
        sidebar_frame.pack(fill=tk.Y, side=tk.LEFT)

# Buttons on the sidebar
        suppliers_button = tk.Button(sidebar_frame, text="Suppliers", command=self.show_suppliers)
        suppliers_button.pack(pady=10)

        clients_button = tk.Button(sidebar_frame, text="Clients", command=self.show_clients)
        clients_button.pack(pady=10)

        items_button = tk.Button(sidebar_frame, text="Inventory Items", command=self.show_items)
        items_button.pack(pady=10)
        orders_button = tk.Button(sidebar_frame, text=" Orders", command=self.show_orders)
        orders_button.pack(pady=10)


        content_frame = tk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True)

       
       

       

# Analytics frame
        analytics_frame = tk.Frame(content_frame, bg="lightblue", relief=tk.RAISED, bd=2)
        analytics_frame.grid(row=0, column=0, padx=20, pady=20)

        

        # Title for analytics
        analytics_title_label = tk.Label(analytics_frame, text="Top Selling Items", font=("Arial", 14, "bold"))
        analytics_title_label.grid(pady=10)

        # Fetch top-selling items data
        top_selling_items = analytics.calculate_top_selling_items()

        def convert_decimal_to_float(item):
            return {'item_name': item['item_name'], 'total_quantity': float(item['total_quantity'])}

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

        # Create a matplotlib figure
        fig = Figure(figsize=(4, 2))

        # Add subplot to the figure
        ax = fig.add_subplot(111)

        # Extract item names and total quantities from fetched data
        item_names = [item['item_name'] for item in top_selling_items]
        total_quantities = [item['total_quantity'] for item in top_selling_items]

        # Create a bar chart
        ax.bar(item_names, total_quantities, color='skyblue')

        # Set labels and title for the chart
        ax.set_xlabel('Items')
        ax.set_ylabel('Total Quantity')
        ax.set_title('Top Selling Items')

        # Embed the plot into a Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=analytics_frame)
        canvas.draw()
        canvas.get_tk_widget().grid()

        sales_performance_frame = tk.Frame(content_frame, bg="lightblue", relief=tk.RAISED, bd=2)
        sales_performance_frame.grid(row=0, column=1, padx=20, pady=20)

        # Title for sales performance
        sales_performance_title_label = tk.Label(sales_performance_frame, text="Sales Performance",
                                                  font=("Arial", 14, "bold"))
        sales_performance_title_label.grid(pady=10)

        # Define the desired period (e.g., last 7 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        orders_data = analytics.fetch_orders_data(start_date, end_date)
        mongodb_database.insert_daily_sales_data(orders_data)
# Extract dates and revenue from orders data
        dates = [order['order_date'] for order in orders_data]
        revenue = [order['total_revenue'] for order in orders_data]

        # Visualize sales trends
        fig_sales = Figure(figsize=(4, 2))
        ax_sales = fig_sales.add_subplot(111)
        ax_sales.plot(dates, revenue, marker='o', color='skyblue')
        ax_sales.set_xlabel('Date')
        ax_sales.set_ylabel('Total Sales Revenue')
        ax_sales.set_title('Sales Trends')
        ax_sales.xaxis.set_tick_params(rotation=45)
        ax_sales.grid(True)

        # Embed the plot into a Tkinter canvas
        canvas_sales = FigureCanvasTkAgg(fig_sales, master=sales_performance_frame)
        canvas_sales.draw()
        canvas_sales.get_tk_widget().grid()
        # Map frame
        map_frame = tk.Frame(content_frame, bg="lightblue", relief=tk.RAISED, bd=2)
        map_frame.grid(row=1, columnspan=2, padx=40, pady=20)

        # Add a map widget
        map_widget = tkintermapview.TkinterMapView(map_frame, width=600, height=300)
        map_widget.set_address("algeria")
        map_widget.set_zoom(3)
        map_widget.pack()

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
        
        
        # Low Stock Items frame
        low_stock_frame = tk.Frame(content_frame, bg="lightblue", relief=tk.RAISED, bd=2)
        low_stock_frame.grid(row=2, columnspan=2, padx=40, pady=20)

        # Title for low stock items
        low_stock_title_label = tk.Label(low_stock_frame, text="Low Stock Items",
                                         font=("Arial", 14, "bold"))
        low_stock_title_label.grid(pady=10)

        # Create a Listbox for displaying low stock items
        low_stock_listbox = tk.Listbox(low_stock_frame, width=50, height=10)
        low_stock_listbox.grid()

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
        orders.geometry("1000x500")
        orders.grab_set()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
