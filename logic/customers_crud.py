from .mysql_database import connect_to_mysql
from tkinter import ttk, messagebox

def create_customer(first_name, last_name, email, contact_number, address, city, country):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = '''INSERT INTO customers (first_name, last_name, email, contact_number, address, city, country)
               VALUES (%s, %s, %s, %s, %s, %s, %s)'''
    values = (first_name, last_name, email, contact_number, address, city, country)

    cursor.execute(query, values)
    conn.commit()
    conn.close()

def get_customer(customer_id):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = "SELECT * FROM customers WHERE customer_id = %s"
    cursor.execute(query, (customer_id,))
    customer = cursor.fetchone()

    conn.close()
    return customer
def get_customers():
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = "SELECT customer_id,first_name, last_name , email ,contact_number,address , city , country FROM customers "
    cursor.execute(query)
    customer = cursor.fetchall()

    conn.close()
    return customer

def update_customer(customer_id, first_name, last_name, email, contact_number, address, city, country):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = '''UPDATE customers 
               SET first_name = %s, last_name = %s, email = %s, contact_number = %s, 
                   address = %s, city = %s, country = %s 
               WHERE customer_id = %s'''
    values = (first_name, last_name, email, contact_number, address, city, country, customer_id)

    cursor.execute(query, values)
    conn.commit()
    conn.close()
def has_pending_orders(customer_id,conn):
  
  cursor = conn.cursor()
  query = "SELECT count(*) FROM orders WHERE customer_id = %s"
  cursor.execute(query, (customer_id,))
  result = cursor.fetchone()
  return result[0] > 0  # Check if count is greater than 0 (has orders)




def delete_customer(customer_id):
    conn = connect_to_mysql()
    if not has_pending_orders(customer_id, conn):
        cursor = conn.cursor()

        query = "DELETE FROM customers WHERE customer_id = %s"
        cursor.execute(query, (customer_id,))
        return True
    else:
        messagebox.showerror("Error", "Customer has pending orders. Cannot delete.")
    conn.commit()
    conn.close()


