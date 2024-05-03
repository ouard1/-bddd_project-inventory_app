from .mysql_database import connect_to_mysql
from tkinter import ttk, messagebox

def create_inventory_item(name, description, category, price, quantity, supplier_name):
  """
  Creates a new inventory item with the given details and retrieves the supplier ID 
  based on the provided supplier name.

  Args:
      name (str): Name of the inventory item.
      description (str): Description of the item.
      category (str): Category of the item.
      price (float): Price of the item.
      quantity (int): Quantity of the item in stock.
      supplier_name (str): Name of the supplier.

  Returns:
      bool: True if the item is created successfully, False otherwise.
  """
  conn = connect_to_mysql()
  cursor = conn.cursor()

  # Get the supplier ID based on the name
  query_supplier = """
      SELECT supplier_id FROM Suppliers WHERE name = %s
  """
  cursor.execute(query_supplier, (supplier_name,))
  supplier_data = cursor.fetchone()

  if not supplier_data:
      print(f"Error: Supplier '{supplier_name}' not found.")
      conn.close()
      return False

  supplier_id = supplier_data[0]

  # Insert the inventory item with the retrieved supplier ID
  query_inventory = '''
      INSERT INTO InventoryItems (name, description, category, price, quantity, supplier_id)
      VALUES (%s, %s, %s, %s, %s, %s)
  '''
  values = (name, description, category, price, quantity, supplier_id)

  try:
      cursor.execute(query_inventory, values)
      conn.commit()
      print("Inventory item created successfully!")
  except Exception as e:
      print(f"Error creating inventory item: {e}")
      conn.rollback()
  finally:
      conn.close()
      return True  # Assuming success unless exception occurs


def get_inventory_items():
  """
  Fetches all inventory items with supplier information.

  Returns:
      list: A list of dictionaries containing inventory item data (including supplier name).
  """
  conn = connect_to_mysql()
  cursor = conn.cursor()

  query = """
      SELECT i.item_id, i.name, i.description, i.category, i.price, i.quantity, s.name AS supplier_name
      FROM InventoryItems i
      INNER JOIN Suppliers s ON i.supplier_id = s.supplier_id
  """
  cursor.execute(query)
  inventory_items = cursor.fetchall()

  conn.close()

  return inventory_items




def update_inventory_item(item_id, name, description, category, price, quantity, supplier_name):
  """
  Updates an existing inventory item with the given details and retrieves the supplier ID 
  based on the provided supplier name.

  Args:
      item_id (int): ID of the inventory item to update.
      name (str): Name of the inventory item.
      description (str): Description of the item.
      category (str): Category of the item.
      price (float): Price of the item.
      quantity (int): Quantity of the item in stock.
      supplier_name (str): Name of the supplier.

  Returns:
      bool: True if the item is updated successfully, False otherwise.
  """
  conn = connect_to_mysql()
  cursor = conn.cursor()

  # Get the supplier ID based on the name
  query_supplier = """
      SELECT supplier_id FROM Suppliers WHERE name = %s
  """
  cursor.execute(query_supplier, (supplier_name,))
  supplier_data = cursor.fetchone()

  if not supplier_data:
      print(f"Error: Supplier '{supplier_name}' not found.")
      conn.close()
      return False

  supplier_id = supplier_data[0]

  # Update the inventory item with the retrieved supplier ID
  query_inventory = '''
      UPDATE InventoryItems 
      SET name = %s, description = %s, category = %s, price = %s, 
          quantity = %s, supplier_id = %s 
      WHERE item_id = %s
  '''
  values = (name, description, category, price, quantity, supplier_id, item_id)

  try:
      cursor.execute(query_inventory, values)
      conn.commit()
      print("Inventory item updated successfully!")
  except Exception as e:
      print(f"Error updating inventory item: {e}")
      conn.rollback()
  finally:
      conn.close()
      return True  

def figures_in_order(item_id,conn):
  
  cursor = conn.cursor()
  query = "SELECT count(*) FROM order_items WHERE item_id = %s"
  cursor.execute(query, (item_id,))
  result = cursor.fetchone()
  return result[0] > 0  # Check if count is greater than 0 (has items in inventory)


def delete_inventory_item(item_id):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    if not figures_in_order(item_id, conn):
        cursor = conn.cursor()

        query = "DELETE FROM InventoryItems WHERE item_id = %s"
        cursor.execute(query, (item_id,))
        return True
    else:
        messagebox.showerror("Error", " items figures in an order.Cannot delete.")
    conn.commit()
    conn.close()

