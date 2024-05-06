import bcrypt
from .mysql_database import connect_to_mysql



def authenticate_user(username, password):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    # Use prepared statements to prevent SQL injection
    query = "SELECT * FROM admin WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    if user:
        hashed_password = user[1]  
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            conn.close()
            return True
    conn.close()
    return False

def hash_password(password):
    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password


