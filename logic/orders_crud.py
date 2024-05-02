from mysql_database import connect_to_mysql

def create_order(customer_id, order_date, status):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = '''INSERT INTO orders (customer_id, order_date, status)
               VALUES (%s, %s, %s)'''
    values = (customer_id, order_date, status)

    cursor.execute(query, values)
    conn.commit()
    conn.close()

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



def create_order_item(order_id, item_id, quantity, price):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = '''INSERT INTO order_items (order_id, item_id, quantity, price)
               VALUES (%s, %s, %s, %s)'''
    values = (order_id, item_id, quantity, price)

    cursor.execute(query, values)
    conn.commit()
    conn.close()

def get_order_item(order_item_id):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = "SELECT * FROM order_items WHERE order_item_id = %s"
    cursor.execute(query, (order_item_id,))
    order_item = cursor.fetchone()

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

