import random
from datetime import datetime, timedelta
from mysql_database import connect_to_mysql

# Function to generate dummy data for orders
def generate_orders_data(num_orders):
    orders_data = []
    conn = connect_to_mysql()
    cursor = conn.cursor()
    for _ in range(num_orders):
        order_date = datetime.now() - timedelta(days=random.randint(1, 30))
        customer_id = random.choice(customer_ids)
        cursor.execute("INSERT INTO orders (order_date, customer_id) VALUES (%s, %s)", (order_date, customer_id))
        order_id = cursor.lastrowid
        orders_data.append({'order_id': order_id, 'order_date': order_date, 'customer_id': customer_id})
    conn.commit()
    conn.close()
    return orders_data

# Function to generate dummy data for order items
def generate_order_items_data(orders_data):
    order_items_data = []
    conn = connect_to_mysql()
    cursor = conn.cursor()
    for order in orders_data:
        num_items = random.randint(1, 5)
        for _ in range(num_items):
            item_id = random.choice(inventory_item_ids)
            quantity = random.randint(1, 10)
            price = round(random.uniform(10, 100), 2)
            cursor.execute("INSERT INTO order_items (order_id, item_id, quantity, price) VALUES (%s, %s, %s, %s)",
                           (order['order_id'], item_id, quantity, price))
            order_items_data.append({'order_id': order['order_id'], 'item_id': item_id, 'quantity': quantity, 'price': price})
    conn.commit()
    conn.close()
    return order_items_data

# Define the range of customer IDs and inventory item IDs
customer_ids = [1, 2, 3, 7]
inventory_item_ids = list(range(1, 12))

# Example usage
num_orders = 20  # You can adjust the number of orders as needed
orders_data = generate_orders_data(num_orders)
order_items_data = generate_order_items_data(orders_data)

print("Data insertion complete.")
