from .mysql_database import connect_to_mysql

     
def create_order(customer_id, order_date, status):
    print(status)
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = '''INSERT INTO orders (customer_id, order_date, status)
               VALUES (%s, %s, %s)'''
    values = (customer_id, order_date, status)

    cursor.execute(query, values)
    conn.commit()
    
    order_id = cursor.lastrowid

    conn.close()

    return order_id

def get_order(order_id):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = "SELECT * FROM orders WHERE order_id = %s"
    cursor.execute(query, (order_id,))
    order = cursor.fetchone()

    conn.close()
    return order

def update_order(order_id, customer_id, order_date, status):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = '''UPDATE orders 
               SET customer_id = %s, order_date = %s, status = %s
               WHERE order_id = %s'''
    values = (customer_id, order_date, status, order_id)

    cursor.execute(query, values)
    conn.commit()
    conn.close()

def delete_order(order_id):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = "DELETE FROM orders WHERE order_id = %s"
    cursor.execute(query, (order_id,))
    conn.commit()
    conn.close()
def get_products():
    conn = connect_to_mysql()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM InventoryItems")
    products = cursor.fetchall()

    conn.close()

    # Extract product names from the fetched data
    product_names = [product[0] for product in products]

    return product_names

def getresult(name):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = "SELECT price ,item_id FROM InventoryItems WHERE name = %s"
    cursor.execute(query, (name,))
    result = cursor.fetchone()
    
    conn.close()
    return result
     

def create_order_item(order_id, name, quantity):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    result = getresult(name)
    print("result" , result)
    # Check if item information is found
    if result:
        item_price, item_id = result
        item_price = float(item_price)

        # Calculate total price for the order item
        total_price = item_price * quantity

        # Insert order item with calculated total price
        query = '''INSERT INTO order_items (order_id, item_id, quantity, price)
                     VALUES (%s, %s, %s, %s)'''
        
        values = (order_id, item_id, quantity, total_price)
        print(values)
        cursor.execute(query, values)

        

    else:
        # Handle case where item price is not found (log error, display message)
        print("Error: Item price not found for", name)

    conn.commit()
    conn.close()


def get_customer_names():
    conn = connect_to_mysql()
    cursor = conn.cursor()

    # Execute the SELECT query to fetch customer names
    query = "SELECT first_name, last_name FROM customers"
    cursor.execute(query)

    # Fetch all the rows returned by the query
    customer_data = cursor.fetchall()

    # Process the fetched data to extract customer names
    customer_names = [" ".join((first_name, last_name)) for first_name, last_name in customer_data]

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    return customer_names

def get_customer_id(customer_name):
    conn = connect_to_mysql()  
    cursor = conn.cursor()

    query = "SELECT customer_id FROM customers WHERE CONCAT(first_name, ' ', last_name) = %s"
    cursor.execute(query, (customer_name,))
    result = cursor.fetchone()

    if result:
        customer_id = result[0]
        return customer_id
    else:
        return None

def get_order_items():
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = "SELECT * FROM order_items"
    cursor.execute(query)
    order_item = cursor.fetchall()

    conn.close()
    return order_item

def update_order_item(order_item_id, order_id, item_id, quantity, price):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = '''UPDATE order_items 
               SET order_id = %s, item_id = %s, quantity = %s, price = %s
               WHERE order_item_id = %s'''
    values = (order_id, item_id, quantity, price, order_item_id)

    cursor.execute(query, values)
    conn.commit()
    conn.close()

def delete_order_item(order_item_id):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = "DELETE FROM order_items WHERE order_item_id = %s"
    cursor.execute(query, (order_item_id,))
    conn.commit()
    conn.close()

