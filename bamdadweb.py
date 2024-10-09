import http.server
import os
from urllib.parse import urlparse, parse_qs
import time

class WebServerHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, data_dir=None, **kwargs):
        # Ensure DATA_DIR is set
        self.data_dir = data_dir

        # If the directory does not exist, create it
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        # Call the parent class (SimpleHTTPRequestHandler) constructor
        super().__init__(*args, **kwargs)

    def do_POST(self):
        try:
            # Parse headers
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)  # Read raw data

            # Attempt to decode the post data
            text_data = post_data.decode('utf-8', errors='ignore').strip()

            if text_data:
                # Create a unique filename for the text data
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                text_file_name = os.path.join(self.data_dir, f"sensor_data_{timestamp}.txt")

                # Save the text data in a separate file
                with open(text_file_name, 'w') as f:
                    f.write(text_data)  # Write text data to a new file

                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Data received")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Bad Request: No data received")

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())

