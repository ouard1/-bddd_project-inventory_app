from mysql_database import connect_to_mysql

def create_inventory_item(name, description, category, price, quantity, supplier_id):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = '''INSERT INTO InventoryItems (name, description, category, price, quantity, supplier_id)
               VALUES (%s, %s, %s, %s, %s, %s)'''
    values = (name, description, category, price, quantity, supplier_id)

    cursor.execute(query, values)
    conn.commit()
    conn.close()

def get_inventory_item(item_id):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = "SELECT * FROM InventoryItems WHERE item_id = %s"
    cursor.execute(query, (item_id,))
    inventory_item = cursor.fetchone()

    conn.close()
    return inventory_item

def update_inventory_item(item_id, name, description, category, price, quantity, supplier_id):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = '''UPDATE InventoryItems 
               SET name = %s, description = %s, category = %s, price = %s, 
                   quantity = %s, supplier_id = %s 
               WHERE item_id = %s'''
    values = (name, description, category, price, quantity, supplier_id, item_id)

    cursor.execute(query, values)
    conn.commit()
    conn.close()

def delete_inventory_item(item_id):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query = "DELETE FROM InventoryItems WHERE item_id = %s"
    cursor.execute(query, (item_id,))
    conn.commit()
    conn.close()


