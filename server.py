import http.server
import socketserver
import time
import threading


last_request_time = None
bit_buffer = []
char_buffer = []
is_first_packet = True

class TimingHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global last_request_time, bit_buffer, is_first_packet
        
        current_time = time.time()
        
        if is_first_packet:
            print("Received first packet (temp packet)")
            is_first_packet = False
        else:
            if last_request_time is not None:
                time_diff = current_time - last_request_time
                if time_diff <= 5:         # Change the value getting compared to time_diff  if increasing the time delay in client.py               
                    bit_buffer.append('0')
                else:
                    bit_buffer.append('1')
                
                print(f"Received bit: {'0' if time_diff <= 5 else '1'} (time diff: {time_diff:.2f}s)")   # Change the value getting compared to time_diff  if increasing the time delay in client.py
                
                if len(bit_buffer) == 8:
                    self.decode_message()
        
        last_request_time = current_time
        
        self.send_response(200)
        self.end_headers()
    
    def decode_message(self):
        global bit_buffer, char_buffer
        byte_string = ''.join(bit_buffer)
        decoded_char = chr(int(byte_string, 2))
        char_buffer.append(decoded_char)
        print(f"Received character: {decoded_char}")
        bit_buffer = []
        
def check_timeout():
    global last_request_time, char_buffer
    while True:
        time.sleep(1)  # Check every second
        if last_request_time is not None and char_buffer:
            current_time = time.time()
            if current_time - last_request_time > 20:
                complete_message = ''.join(char_buffer)
                print(f"Complete message received : {complete_message}")
                char_buffer = []  # Reset for next message
                last_request_time = None

if __name__ == "__main__":
    PORT = 8000
    
    # Start the timeout checking thread
    timeout_thread = threading.Thread(target=check_timeout, daemon=True)
    timeout_thread.start()

    with socketserver.TCPServer(("", PORT), TimingHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()