from http.server import HTTPServer
import json
from http.server import BaseHTTPRequestHandler
import mysql.connector
from datetime import date, datetime
from decimal import Decimal

# MySQL database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "tourism"  # Update with your actual database name
}

def get_db_connection():
    """Get a MySQL database connection."""
    return mysql.connector.connect(**DB_CONFIG)

class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle date, datetime, and Decimal types."""
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

class RequestHandler(BaseHTTPRequestHandler):
    """RequestHandler to process GET, POST, PUT, and DELETE requests."""

    def do_GET(self):
        """Handle GET requests."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            result = None

            if self.path.startswith("/agents/"):
                agent_id = self.path.split("/")[-1]
                cursor.execute("SELECT * FROM agents WHERE AgentID = %s", (agent_id,))
                result = cursor.fetchone()
            elif self.path.startswith("/bookings/"):
                booking_id = self.path.split("/")[-1]
                cursor.execute("SELECT * FROM bookings WHERE BookingID = %s", (booking_id,))
                result = cursor.fetchone()
            elif self.path.startswith("/customers/"):
                customer_id = self.path.split("/")[-1]
                cursor.execute("SELECT * FROM customers WHERE CustomerID = %s", (customer_id,))
                result = cursor.fetchone()
            elif self.path.startswith("/destinations/"):
                destination_id = self.path.split("/")[-1]
                cursor.execute("SELECT * FROM destinations WHERE DestinationID = %s", (destination_id,))
                result = cursor.fetchone()
            elif self.path.startswith("/tourpackages/"):
                package_id = self.path.split("/")[-1]
                cursor.execute("SELECT * FROM tourpackages WHERE PackageID = %s", (package_id,))
                result = cursor.fetchone()
            else:
                cursor.execute("SELECT * FROM agents")  # Default to listing all agents
                result = cursor.fetchall()

            response_body = json.dumps(result, cls=CustomJSONEncoder)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(response_body.encode())
        except Exception as e:
            self.send_error(500, str(e))
        finally:
            cursor.close()
            conn.close()

    def do_POST(self):
        """Handle POST requests."""
        cursor = None
        conn = None
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            if self.path.startswith("/agents/"):
                name = data.get("Name")
                email = data.get("Email")
                phone = data.get("Phone")
                commission_rate = data.get("CommissionRate", 10.00)  # Default to 10.00

                if not all([name, email, phone]):
                    self.send_error(400, "Missing required fields")
                    return

                insert_query = """
                    INSERT INTO agents (Name, Email, Phone, CommissionRate)
                    VALUES (%s, %s, %s, %s)
                """
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(insert_query, (name, email, phone, commission_rate))
                conn.commit()

            elif self.path.startswith("/bookings/"):
                customer_id = data.get("CustomerID")
                package_id = data.get("PackageID")
                total_amount = data.get("TotalAmount")
                agent_id = data.get("AgentID")
                transport_id = data.get("TransportID", None)  # Optional field
                status = data.get("Status", "Pending")  # Default to Pending

                if not all([customer_id, package_id, total_amount, agent_id]):
                    self.send_error(400, "Missing required fields")
                    return

                insert_query = """
                    INSERT INTO bookings (CustomerID, PackageID, TotalAmount, AgentID, Status, TransportID)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(insert_query, (customer_id, package_id, total_amount, agent_id, status, transport_id))
                conn.commit()

            self.send_response(201)  # Created
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"message": "Data added successfully"}
            self.wfile.write(json.dumps(response).encode())

        except mysql.connector.Error as db_err:
            self.send_error(500, f"Database error: {str(db_err)}")
        except Exception as e:
            self.send_error(500, f"Error: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def do_PUT(self):
        """Handle PUT requests to update records."""
        cursor = None
        conn = None
        try:
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            data = json.loads(put_data)

            if self.path.startswith("/agents/"):
                agent_id = self.path.split("/")[-1]
                name = data.get("Name")
                email = data.get("Email")
                phone = data.get("Phone")
                commission_rate = data.get("CommissionRate")

                if not all([name, email, phone, commission_rate]):
                    self.send_error(400, "Missing required fields")
                    return

                update_query = """
                    UPDATE agents
                    SET Name = %s, Email = %s, Phone = %s, CommissionRate = %s
                    WHERE AgentID = %s
                """
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(update_query, (name, email, phone, commission_rate, agent_id))
                conn.commit()

            elif self.path.startswith("/bookings/"):
                booking_id = self.path.split("/")[-1]
                status = data.get("Status")

                if not status:
                    self.send_error(400, "Missing required fields")
                    return

                update_query = """
                    UPDATE bookings
                    SET Status = %s
                    WHERE BookingID = %s
                """
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(update_query, (status, booking_id))
                conn.commit()

            self.send_response(200)  # OK
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"message": "Data updated successfully"}
            self.wfile.write(json.dumps(response).encode())

        except mysql.connector.Error as db_err:
            self.send_error(500, f"Database error: {str(db_err)}")
        except Exception as e:
            self.send_error(500, f"Error: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def do_DELETE(self):
        """Handle DELETE requests to remove records."""
        cursor = None
        conn = None
        try:
            # Extract the ID from the URL path
            if self.path.startswith("/agents/"):
                agent_id = self.path.split("/")[-1]
                delete_query = "DELETE FROM agents WHERE AgentID = %s"
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(delete_query, (agent_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    self.send_error(404, "Agent not found")
                    return

            elif self.path.startswith("/bookings/"):
                booking_id = self.path.split("/")[-1]
                delete_query = "DELETE FROM bookings WHERE BookingID = %s"
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(delete_query, (booking_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    self.send_error(404, "Booking not found")
                    return

            elif self.path.startswith("/customers/"):
                customer_id = self.path.split("/")[-1]
                delete_query = "DELETE FROM customers WHERE CustomerID = %s"
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(delete_query, (customer_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    self.send_error(404, "Customer not found")
                    return

            elif self.path.startswith("/destinations/"):
                destination_id = self.path.split("/")[-1]
                delete_query = "DELETE FROM destinations WHERE DestinationID = %s"
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(delete_query, (destination_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    self.send_error(404, "Destination not found")
                    return

            elif self.path.startswith("/payments/"):
                payment_id = self.path.split("/")[-1]
                delete_query = "DELETE FROM payments WHERE PaymentID = %s"
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(delete_query, (payment_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    self.send_error(404, "Payment not found")
                    return

            elif self.path.startswith("/reviews/"):
                review_id = self.path.split("/")[-1]
                delete_query = "DELETE FROM reviews WHERE ReviewID = %s"
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(delete_query, (review_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    self.send_error(404, "Review not found")
                    return

            elif self.path.startswith("/tourpackages/"):
                package_id = self.path.split("/")[-1]
                delete_query = "DELETE FROM tourpackages WHERE PackageID = %s"
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(delete_query, (package_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    self.send_error(404, "Tour package not found")
                    return

            elif self.path.startswith("/transport/"):
                transport_id = self.path.split("/")[-1]
                delete_query = "DELETE FROM transport WHERE TransportID = %s"
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(delete_query, (transport_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    self.send_error(404, "Transport not found")
                    return

            else:
                self.send_error(400, "Invalid endpoint for DELETE")
                return

            # Send successful response
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"message": "Data deleted successfully"}
            self.wfile.write(json.dumps(response).encode())

        except mysql.connector.Error as db_err:
            self.send_error(500, f"Database error: {str(db_err)}")
        except Exception as e:
            self.send_error(500, f"Error: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def run():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Server is running on http://localhost:8080")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
