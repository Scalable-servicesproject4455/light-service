from flask import Flask, request, jsonify
import pika
import traceback
import logging
import socket  # Import the socket module
import db.connectToDb
 
app = Flask(__name__)
 
# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
 
 
@app.route('/publish/', methods=['POST'])
def publish_message():
    logger.debug("Received request at /publish/")
    try:
        # Connect to RabbitMQ.  Use a try-except block for connection errors.
        try:
            # Resolve the hostname to an IP address *before* connecting.
            try:
                rabbitmq_ip = socket.gethostbyname('rabbitmq')
                logger.debug(f"Resolved 'rabbitmq' to IP address: {rabbitmq_ip}")
                connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_ip))
            except socket.gaierror as e:
                logger.error(f"DNS resolution failed for 'rabbitmq': {e}")
                return jsonify({"status": "error", "message": f"Could not resolve hostname 'rabbitmq'.  Check your network configuration or ensure RabbitMQ is accessible at this hostname: {e}"}), 500
 
            channel = connection.channel()
            logger.debug("Connected to RabbitMQ")
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Could not connect to RabbitMQ: {e}")
            return jsonify({"status": "error", "message": f"Could not connect to RabbitMQ: {e}"}), 500
 
        # Declare queue
        channel.queue_declare(queue='hello')
        logger.debug("Queue 'hello' declared")
 
        # Get message from request.  Handle the case where the request is not JSON or 'message' is missing.
        try:
            data = request.get_json()
            logger.debug(f"Received JSON data: {data}")
            if not isinstance(data, dict):
                logger.error("Request must be JSON")
                return jsonify({"status": "error", "message": "Request must be JSON"}), 400
            message = data.get('message', 'Hello World!')
            if message is None:
                logger.error("'message' key is missing or null in the JSON payload")
                return jsonify({"status": "error", "message": "'message' key is missing or null in the JSON payload"}), 400
        except Exception as e:
            logger.error(f"Error parsing JSON: {e}")
            return jsonify({"status": "error", "message": f"Error parsing JSON: {e}"}), 400
 
        # Publish message
        try:
            channel.basic_publish(exchange='', routing_key='hello', body=message.encode('utf-8'))
            connection.close()
            logger.debug(f"Published message: {message}")
        except Exception as e:
            # Handle errors during publishing
            connection.close()
            logger.error(f"Error publishing message: {e}")
            return jsonify({"status": "error", "message": f"Error publishing message: {e}"}), 500
 
        return jsonify({"status": "Message published", "message": message}), 200
 
    except Exception as e:
        # Catch any unexpected errors
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return jsonify({"status": "error", "message": f"An unexpected error occurred: {e}", "traceback": traceback.format_exc()}), 500
 
@app.route('/api/createAndGetData', methods=['GET'])
def create_data():
    try:
        rows = db.connectToDb.connect_to_db()
        return jsonify({
            "status": "success",
            "message": "Data created and retrieved successfully",
            "data": rows  # This should be a list, not a set
        }), 200
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
 
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
 
 