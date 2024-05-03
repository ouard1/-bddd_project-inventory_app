import mysql.connector
from mysql_database import connect_to_mysql
def insert_dummy_customers():
    # Establish a connection to the MySQL database
    conn = connect_to_mysql()
    cursor = conn.cursor()

    # Dummy data to insert into the customers table
    dummy_customers = [
        ("John", "Doe", "john@example.com", "1234567890", "123 Main St", "New York", "USA"),
        ("Jane", "Smith", "jane@example.com", "0987654321", "456 Elm St", "Los Angeles", "USA"),
        ("Michael", "Johnson", "michael@example.com", "9876543210", "789 Oak St", "Chicago", "USA")
    ]

    # SQL query to insert data into the customers table
    insert_query = "INSERT INTO customers (first_name, last_name, email, contact_number, address, city, country) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    try:
        # Execute the SQL query for each dummy customer
        for customer in dummy_customers:
            cursor.execute(insert_query, customer)

        # Commit the transaction
        conn.commit()
        print("Dummy customers inserted successfully!")

    except mysql.connector.Error as error:
        # Rollback the transaction in case of any error
        conn.rollback()
        print("Error inserting dummy customers:", error)

    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

# Call the function to insert dummy customers
insert_dummy_customers()
