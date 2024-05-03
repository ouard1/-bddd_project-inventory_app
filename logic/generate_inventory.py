from mysql_database import connect_to_mysql
from random import randint
from inventory_items_crud import create_inventory_item

def generate_dummy_inventory_items(num_items):
    """
    Generates dummy inventory items and inserts them into the database.

    Args:
        num_items (int): The number of dummy inventory items to generate.

    Returns:
        bool: True if the items are generated and inserted successfully, False otherwise.
    """
    conn = connect_to_mysql()
    cursor = conn.cursor()

    # Dummy data for inventory items
    dummy_items = [
        ("Laptop", "A high-performance laptop with advanced features.", "Electronics", 999.99, 10),
        ("Smartphone", "The latest smartphone model with a sleek design.", "Electronics", 599.99, 20),
        ("Headphones", "Premium wireless headphones with noise-canceling technology.", "Electronics", 199.99, 15),
        ("Keyboard", "Mechanical gaming keyboard with RGB lighting.", "Electronics", 79.99, 30),
        ("Mouse", "Ergonomic wireless mouse for improved productivity.", "Electronics", 49.99, 25)
    ]

    try:
        for _ in range(num_items):
            # Select a random dummy item
            item_name, description, category, price, max_quantity = dummy_items[randint(0, len(dummy_items) - 1)]

            # Generate a random quantity between 0 and max_quantity
            quantity = randint(0, max_quantity)

            # Insert the item into the database
            create_inventory_item(item_name, description, category, price, quantity, supplier_name="test")

        print(f"{num_items} dummy inventory items generated and inserted successfully!")
        return True

    except Exception as e:
        print(f"Error generating dummy inventory items: {e}")
        return False

generate_dummy_inventory_items(5)