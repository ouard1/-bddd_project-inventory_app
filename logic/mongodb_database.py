from pymongo import MongoClient

# Connect to MongoDB database
def connect_to_mongodb():
    return MongoClient('mongodb+srv://ouarda:02152002@cluster.fgy4xro.mongodb.net/')['inventory']

def store_supplier_location(supplier_id, name, location):
    db = connect_to_mongodb()
    supplier_locations_collection = db['supplier_locations']
    supplier_location = {
        "supplier_id": supplier_id,
        "address": location
    }
    result = supplier_locations_collection.insert_one(supplier_location)
    return result.inserted_id

def update_supplier_address(supplier_id, new_address):
    
    db = connect_to_mongodb()
    supplier_locations_collection = db['supplier_locations']

    # Update address for the supplier with matching ID
    update_result = supplier_locations_collection.update_one(
        {'supplier_id': supplier_id}, {'$set': {'address': new_address}}
    )

    # Check update result
    if update_result.matched_count > 0:
        return True  
    else:
        return False  



'''# Function to store customer locations
def store_customer_location(customer_id, first_name, last_name, location):
    db = connect_to_mongodb()
    customer_locations_collection = db['customer_locations']
    customer_location = {
        "customer_id": customer_id,
        "address": location
    }
    result = customer_locations_collection.insert_one(customer_location)
    return result.inserted_id'''

'''# Function to store sales analytics data
def store_sales_analytics(date, total_sales, sales_by_category, average_order_value, customer_lifetime_value, conversion_rate):
    db = connect_to_mongodb()
    sales_analytics_collection = db['sales_analytics']
    sales_analytics = {
        "date": date,
        "total_sales": total_sales,
        "sales_by_category": sales_by_category,
        "average_order_value": average_order_value,
        "customer_lifetime_value": customer_lifetime_value,
        "conversion_rate": conversion_rate
    }
    result = sales_analytics_collection.insert_one(sales_analytics)
    return result.inserted_id

# Function to store inventory alerts 
def store_inventory_alert(item_id, alert_type, quantity_threshold, timestamp):
    db = connect_to_mongodb()
    inventory_alerts_collection = db['inventory_alerts']
    inventory_alert = {
        "item_id": item_id,
        "alert_type": alert_type,
        "quantity_threshold": quantity_threshold,
        "timestamp": timestamp
    }
    result = inventory_alerts_collection.insert_one(inventory_alert)
    return result.inserted_id'''