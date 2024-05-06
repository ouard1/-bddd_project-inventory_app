from pymongo import MongoClient
from datetime import datetime
import base64
import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pymongo import MongoClient

# Encryption/Decryption key generation
def generate_key(password):
    salt = b'f'
    password_bytes = password.encode('utf-8')  # Encode the password to bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=salt,
        length=32,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    return key




def decrypt_url(encrypted_url, key):
   
    if isinstance(encrypted_url, bytes):
        encrypted_url = encrypted_url.decode()
    f = Fernet(key)
    decrypted_url = f.decrypt(encrypted_url).decode()
    return decrypted_url

mongodb_connection = None
def connect_to_mongodb(decrypted_url):
  # Establish connection to MongoDB database
    global mongodb_connection
    mongodb_connection = MongoClient(decrypted_url)['inventory']



def get_mongodb_connection():
    global mongodb_connection
    return mongodb_connection



def store_supplier_location(supplier_id, address_with_coordinates):
    # Split the address to extract the address details and coordinates
    address_parts = address_with_coordinates.split("coordinates:")
    address = address_parts[0].strip()  # Extract the address
    coordinates_str = address_parts[1].strip().strip("()")  # Extract the coordinates as string

    # Convert the coordinates string to a tuple of floats
    coordinates = tuple(map(float, coordinates_str.split(",")))

    # the GeoJSON object
    location = {
        "type": "Point",
        "coordinates": coordinates
    }

    # Connect to MongoDB and insert the document
    db = get_mongodb_connection()
    supplier_locations_collection = db['supplier_locations']
    supplier_location = {
        "supplier_id": supplier_id,
        "address": address,
        "location": location
    }
    result = supplier_locations_collection.insert_one(supplier_location)
    return result.inserted_id

def update_supplier_address(supplier_id, new_address):
    print(new_address)
    # Check if "coordinates : " substring exists in the new_address string
    if "coordinates: " in new_address:
        # Split the address to extract the address details and coordinates
        address_parts = new_address.split("coordinates: ")
        
        # Extract the address
        address = address_parts[0].strip()

        # Extract the coordinates as string
        coordinates_str = address_parts[1].strip().strip("()")
        
        # Convert the coordinates string to a tuple of floats
        coordinates = tuple(map(float, coordinates_str.split(",")))
        print(address ,"coord",coordinates)
    else:
        # If "coordinates : " is not found, set address and coordinates to None
        address = new_address.strip()
        coordinates = None

    # Connect to MongoDB and access the collection
    db = get_mongodb_connection()
    supplier_locations_collection = db['supplier_locations']

    # Update address and coordinates for the supplier with matching ID
    update_result = supplier_locations_collection.update_one(
        {'supplier_id': supplier_id},
        {'$set': {'address': address, 'location.coordinates': coordinates}}
    )

    # Check update result
    if update_result.matched_count > 0:
        return print("success")  # Update successful
    else:
        return print("faulure")  # Supplier with the given ID not found

  
def get_supplier_address(supplier_id):
    db = get_mongodb_connection()
    supplier_locations_collection = db['supplier_locations']
    supplier_location = supplier_locations_collection.find_one({"supplier_id": supplier_id})
    if supplier_location:
        return supplier_location.get("address")
    else:
        return None


def get_supplier_coordinates():
    # Connect to MongoDB
    db = get_mongodb_connection()
    supplier_locations_collection = db['supplier_locations'] 

    # Query MongoDB to fetch all documents
    cursor = supplier_locations_collection.find({}, {'_id': 0, 'location.coordinates': 1})

    # Extract coordinates from cursor
    coordinates_list = []
    for doc in cursor:
        if 'location' in doc and 'coordinates' in doc['location']:
            coordinates_list.append(doc['location']['coordinates'])

    return coordinates_list



def insert_analytics(analytics):
    # Store in MongoDB
        db = get_mongodb_connection()
        collection = db['analytics']
        collection.insert_one(analytics)
      


def insert_daily_sales_data(orders_data):
    mongodb_client = get_mongodb_connection()
    sales_collection = mongodb_client['sales_performance']

    for order in orders_data:
        period = order['order_date'].strftime('%Y-%m-%d')
        total_revenue = float(order['total_revenue'])
        total_quantity_sold = float(order['total_quantity_sold'])
        average_order_value = float(order['average_order_value'])
        number_of_orders = float(order['num_orders'])


        # Create document
        sales_document = {
            'period': period,
            'total_revenue': total_revenue,
            'total_quantity_sold': total_quantity_sold,
            'average_order_value': average_order_value,
            'number_of_orders': number_of_orders
        }

        # Insert document into MongoDB
        sales_collection.insert_one(sales_document)

 
def store_low_stock_items(low_stk_items):
    """
    Stores low stock items data along with the timestamp in the MongoDB collection.
    Each day's low stock items are stored as a separate document.
    """
    # Connect to MongoDB
    db = get_mongodb_connection()
    low_stock_collection = db['low_stock_items']  # Your MongoDB collection

    # Get current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Check if data for the current date already exists in the collection
    existing_data = low_stock_collection.find_one({'date': current_date})

    if existing_data:
        print("Low stock items data for today already exists.")
        return

    # Identify low stock items (adjust the threshold as needed)
    threshold = 10
    low_stock_items = low_stk_items

    # Create a document to store low stock items data for the current date
    document = {
        'date': current_date,
        'low_stock_items': low_stock_items
    }

    # Insert the document into the collection
    low_stock_collection.insert_one(document)

    print("Low stock items data stored successfully for today.")

#deleting a supplier
def delete_supplier_mg(supplier_id):
    db=get_mongodb_connection()
    collection=db['supplier_locations']
    collection.delete_one({'_id': supplier_id})
        
    