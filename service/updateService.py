import mysql.connector
from mysql.connector import Error
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_connection():
    return mysql.connector.connect(
        host='mysql-db',
        port=3306,
        user='root',
        password='root',
        database='light_db'
    )


def update_brightness_by_id(room_id, new_brightness):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE light_service SET brightness = %s WHERE room_id = %s",
            (new_brightness, room_id)
        )
        conn.commit()
        logger.info(f"Updated room_id {room_id} to brightness '{new_brightness}'")
        return cursor.rowcount  # Returns number of rows updated
    except Error as e:
        logger.error(f"Error updating brightness: {e}")
        raise e
    finally:
        if conn.is_connected():
            conn.close()


def bulk_update_brightness(old_value, new_value):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE light_service SET brightness = %s WHERE brightness = %s",
            (new_value, old_value)
        )
        conn.commit()
        logger.info(f"Bulk updated brightness from '{old_value}' to '{new_value}'")
        return cursor.rowcount
    except Error as e:
        logger.error(f"Error in bulk update: {e}")
        raise e
    finally:
        if conn.is_connected():
            conn.close()
