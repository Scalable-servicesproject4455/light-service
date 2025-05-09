import mysql.connector
from mysql.connector import Error
from flask import Flask
import logging
 
app = Flask(__name__)
 
# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
 
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host='mysql-db',
            port=3306,
            user='root',
            password='root',
            database='temp_db'
        )
 
        if conn.is_connected():
            print("Connected to MySQL from service 1")
            cursor = conn.cursor()
 
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS temp_service (
                    room_id INT AUTO_INCREMENT PRIMARY KEY,
                    temperature INT
                )
            """)
 
            cursor.execute("SELECT COUNT(*) FROM temp_service")
            count = cursor.fetchone()[0]
 
            if count == 0:
                print("No temperature records found. Inserting initial data...")
                cursor.executemany("INSERT INTO temp_service (temperature) VALUES (%s)", [
                    (25,),
                    (28,),
                    (30,)
                ])
                conn.commit()
 
            # Fetch rows
            cursor.execute("SELECT * FROM temp_service")
            rows = cursor.fetchall()
 
            return [dict(room_id=row[0], temperature=row[1]) for row in rows]
 
    except Error as e:
        print(f"Error: {e}")
        raise e
    finally:
        if conn.is_connected():
            conn.close()
            print("Connection closed")
 
 