from .mysql_database import connect_to_mysql
from tkinter import ttk, messagebox
from .mongodb_database import store_supplier_location,update_supplier_address,get_supplier_address,delete_supplier_mg


def create_supplier(name, contact_person, contact_number, email, address):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = '''INSERT INTO Suppliers (name, contact_person, contact_number, email)
               VALUES (%s, %s, %s, %s)'''
    values = (name, contact_person, contact_number, email)

    cursor.execute(query, values)
    # Get the newly created supplier ID from MySQL
    cursor.execute("SELECT LAST_INSERT_ID()")
    supplier_id = cursor.fetchone()[0]

    # Store address in MongoDB using supplier ID
    store_supplier_location(supplier_id, address)
    conn.commit()
    conn.close()

def get_suppliers():
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = "SELECT * FROM Suppliers "
    cursor.execute(query)
    supplier = cursor.fetchall()

    conn.close()
    return supplier

def update_supplier(supplier_id, name, contact_person, contact_number, email,address):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = '''UPDATE Suppliers 
               SET name = %s, contact_person = %s, contact_number = %s, email = %s
               WHERE supplier_id = %s'''
    values = (name, contact_person, contact_number, email, supplier_id)
    update_supplier_address(supplier_id ,address)

    cursor.execute(query, values)
    conn.commit()
    conn.close()


def get_address(supplier_id):
    return get_supplier_address(supplier_id)

def has_inventory_stock(supplier_id,conn):
  
  cursor = conn.cursor()
  query = "SELECT count(*) FROM inventoryitems WHERE supplier_id = %s"
  cursor.execute(query, (supplier_id,))
  result = cursor.fetchone()
  return result[0] > 0  # Check if count is greater than 0 (has items in inventory)


def delete_supplier(supplier_id):
    conn = connect_to_mysql()
    if not has_inventory_stock(supplier_id, conn):
        cursor = conn.cursor()

        query = "DELETE FROM Suppliers WHERE supplier_id = %s"
        cursor.execute(query, (supplier_id,))
        delete_supplier_mg(supplier_id)
        return True
    else:
        messagebox.showerror("Error", "Supplier has items in stock .Cannot delete.")
    conn.commit()
    conn.close()
