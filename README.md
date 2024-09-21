# Timing-Based-Covert-Channel
A proof of concept for covert communication using timing intervals in HTTP requests to encode and transmit data.

## Implementation
This project is a proof of concept using a simple client-server model in Python, showing how binary data can be hidden using time delays between sent requests. 

![image](https://github.com/user-attachments/assets/3cc1f850-dd78-47c1-a989-1fa1bce0590e)

### Client Script
In the `client.py` file, the `message` is encoded to binary data. Each bit in the binary data determines the delay before sending the next request:
- A '0' bit sends a request immediately.
- A '1' bit introduces a delay (5 seconds here) before sending the next request.

### Server Script
The `server.py` receives these requests and measures the time difference between consecutive requests:
- If the time difference is less than or equal to the delay threshold (5 seconds), it is a '0' bit.
- If the time difference exceeds the delay threshold, it is '1' bit.

The server collects these bits until it forms a complete byte (8 bits) and then decodes the byte into a character. Once all characters of the message are received, the server prints the complete message.

#### Message Termination 
If no requests are received for 20 seconds and there are decoded characters in the buffer, the server assumes the transmission is complete and prints the entire received message.

## Server Output
Secret Message : test

 ![Screenshot 2024-07-26 204149](https://github.com/user-attachments/assets/481b18f4-ef94-466c-a083-f9da27e55ae8)

## Additional Resources

To read about covert channels, you can read my blog [**Understanding Covert Channels**](https://medium.com/@vansh_/understanding-covert-channels-hands-on-19585315a19d).
