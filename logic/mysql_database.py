import mysql.connector

#connexion avec MySQL database 
def connect_to_mysql(): 
    return mysql.connector.connect(
        host = "localhost",
        user = "ouarda",
        password = "02152002",
        database = "inventory"
    )


#function to create suppliers table
def create_suppliers_table():
    conn = connect_to_mysql()
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Suppliers (
                        supplier_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255),
                        contact_person VARCHAR(255),
                        contact_number VARCHAR(20),
                        email VARCHAR(100),
                        address VARCHAR(255),
                        city VARCHAR(100),
                        country VARCHAR(100)
                     )''')

    conn.commit()
    conn.close()

# Function to create Customers table
def create_customers_table():
    conn = connect_to_mysql()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                        customer_id INT AUTO_INCREMENT PRIMARY KEY,
                        first_name VARCHAR(50),
                        last_name VARCHAR(50),
                        email VARCHAR(100),
                        contact_number VARCHAR(15),
                        address VARCHAR(255),
                        city VARCHAR(100),
                        country VARCHAR(100)
                     )''')

    conn.commit()
    conn.close()


#function to create orders table
def create_orders_table():
    conn = connect_to_mysql()
    cursor = conn.cursor()
    print(conn)
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        order_id INT AUTO_INCREMENT PRIMARY KEY,
                        customer_id INT,
                        order_date DATE,
                        status ENUM('placed', 'fulfilled', 'canceled'),
                        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                     )''')

    conn.commit()
    conn.close()

#function to create inventory items table

def create_inventory_items_table():
    conn = connect_to_mysql()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS InventoryItems (
                        item_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255),
                        description TEXT,
                        category VARCHAR(100),
                        price DECIMAL(10, 2),
                        quantity INT,
                        supplier_id INT,
                        FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
                     )''')

    conn.commit()
    conn.close()





# Function to create Order Items table

def create_order_items_table():
    conn = connect_to_mysql()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS order_items (
                        order_item_id INT AUTO_INCREMENT PRIMARY KEY,
                        order_id INT,
                        item_id INT,
                        quantity INT,
                        price DECIMAL(10, 2),
                        FOREIGN KEY (order_id) REFERENCES orders(order_id),
                        FOREIGN KEY (item_id) REFERENCES InventoryItems(item_id)  
                     )''')

    conn.commit()
    conn.close()


create_customers_table()
create_suppliers_table()
create_inventory_items_table()
create_orders_table()
create_order_items_table()
