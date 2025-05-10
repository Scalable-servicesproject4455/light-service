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


def get_all_lights():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM light_service")
        rows = cursor.fetchall()
        return [dict(room_id=row[0], brightness=row[1]) for row in rows]
    except Error as e:
        logger.error(f"Error fetching all lights: {e}")
        raise e
    finally:
        if conn.is_connected():
            conn.close()


def get_light_by_id(room_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM light_service WHERE room_id = %s", (room_id,))
        row = cursor.fetchone()
        return dict(room_id=row[0], brightness=row[1]) if row else None
    except Error as e:
        logger.error(f"Error fetching light by ID: {e}")
        raise e
    finally:
        if conn.is_connected():
            conn.close()


def get_lights_by_brightness(level):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM light_service WHERE brightness = %s", (level,))
        rows = cursor.fetchall()
        return [dict(room_id=row[0], brightness=row[1]) for row in rows]
    except Error as e:
        logger.error(f"Error fetching lights by brightness: {e}")
        raise e
    finally:
        if conn.is_connected():
            conn.close()


def get_light_count():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM light_service")
        count = cursor.fetchone()[0]
        return count
    except Error as e:
        logger.error(f"Error getting light count: {e}")
        raise e
    finally:
        if conn.is_connected():
            conn.close()
