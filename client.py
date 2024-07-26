import requests
import time

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def send_message(message, base_url):
    binary_message = text_to_binary(message)
    
    # Send first packet as a temp packet
    requests.get(base_url)
    
    for bit in binary_message:
        if bit == '1':
            time.sleep(5)  # Wait 5 seconds for '1' bit
            # the time delay needs to be greater than the network latency(time taken by packet from client to reach server) for accurate results.
            # if this is not working fine, try increasing the time delay. Also modify the value in do_GET function in server.py
        requests.get(base_url)  # Send packet immediately for '0' bit

if __name__ == "__main__":
    base_url = "http://localhost:8000"
    message = "test"
    send_message(message, base_url)
    print("Message sent!")