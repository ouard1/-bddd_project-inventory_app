from .mysql_database import connect_to_mysql
from tkinter import ttk, messagebox

def calculate_top_selling_items():
            conn = connect_to_mysql()
            cursor = conn.cursor(dictionary=True)

            # Query to fetch data and calculate top-selling items
            cursor.execute("""
                SELECT 
                    ii.name AS item_name, 
                    SUM(oi.quantity) AS total_quantity
                FROM 
                    order_items oi
                INNER JOIN 
                    InventoryItems ii ON oi.item_id = ii.item_id
                GROUP BY 
                    oi.item_id
                ORDER BY 
                    total_quantity DESC
                LIMIT 
                    5  
            """)
            top_selling_items = cursor.fetchall()

           
            cursor.close()
            conn.close()

            return top_selling_items

def fetch_orders_data(start_date, end_date):
    conn = connect_to_mysql()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            DATE(o.order_date) AS order_date, 
            SUM(oi.quantity * oi.price) AS total_revenue,
            SUM(oi.quantity) AS total_quantity_sold,
            AVG(oi.quantity * oi.price) AS average_order_value,
            COUNT(DISTINCT o.order_id) AS num_orders
        FROM 
            orders o
        INNER JOIN 
            order_items oi ON o.order_id = oi.order_id
        WHERE 
            o.order_date BETWEEN %s AND %s
        GROUP BY 
            DATE(o.order_date)
        ORDER BY 
            DATE(o.order_date)
    """, (start_date, end_date))
    orders_data = cursor.fetchall()
    conn.close()
    return orders_data



def get_items_below_quantity(reorder_point):
    """
    Retrieve items with quantities below the specified reorder point.

    Args:
    - reorder_point (int): The threshold quantity below which items are considered low in stock.

    Returns:
    - A list of dictionaries containing the details of low stock items.
    Each dictionary should contain at least the following keys:
        - 'name': The name of the item.
        - 'quantity': The current quantity of the item in stock.
    """
    conn = connect_to_mysql()
    cursor = conn.cursor()
    cursor.execute("SELECT name, quantity FROM InventoryItems WHERE quantity < %s", (reorder_point,))
    low_stock_items = cursor.fetchall()
    cursor.close()
    
    # Convert the results to a list of dictionaries
    low_stock_items_list = [{'name': row[0], 'quantity': row[1]} for row in low_stock_items]
    
    return low_stock_items_list