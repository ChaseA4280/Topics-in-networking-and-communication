"""
Simple TCP Server Implementation
Assignment 1 - TCP Socket Communication
"""

import socket
import threading
import datetime
import sys

class SimpleTCPServer:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.connections_handled = 0
        self.running = False
        
    def start_server(self):
        """Start the TCP server and listen for connections"""
        try:
            # Create socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind to address and port
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"Server started on {self.host}:{self.port}")
            print("Waiting for connections...")
            
            while self.running:
                try:
                    # Accept client connection
                    client_socket, client_address = self.server_socket.accept()
                    print(f"\nNew connection from {client_address}")
                    
                    # Handle client in separate thread
                    client_thread = threading.Thread(
                        target=self.handle_client, 
                        args=(client_socket, client_address)
                    )
                    client_thread.start()
                    
                except socket.error as e:
                    if self.running:
                        print(f"Socket error: {e}")
                    break
                    
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.cleanup()
    
    def handle_client(self, client_socket, client_address):
        """Handle individual client connection"""
        try:
            self.connections_handled += 1
            
            # Send welcome message
            welcome_msg = "WELCOME: Simple TCP Server v1.0 - Ready for commands\n"
            client_socket.send(welcome_msg.encode('utf-8'))
            print(f"Sent welcome message to {client_address}")
            
            while True:
                # Receive command from client
                data = client_socket.recv(1024).decode('utf-8').strip()
                
                if not data:
                    break
                    
                print(f"Received from {client_address}: {data}")
                
                # Process command
                response = self.process_command(data)
                
                # Send response
                client_socket.send(f"{response}\n".encode('utf-8'))
                print(f"Sent to {client_address}: {response}")
                
                # Check if client wants to quit
                if data.upper() == "QUIT":
                    break
                    
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            client_socket.close()
            print(f"Connection with {client_address} closed")
    
    def process_command(self, command):
        """Process client commands and return appropriate response"""
        command = command.strip()
        command_upper = command.upper()
        
        if command_upper == "TIME":
            # Return current date and time
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return f"TIME_RESPONSE: {current_time}"
            
        elif command_upper.startswith("ECHO "):
            # Echo back the message
            message = command[5:]  # Remove "ECHO " prefix
            return f"ECHO_RESPONSE: {message}"
            
        elif command_upper == "STATUS":
            # Return server status
            return f"STATUS_RESPONSE: Server running, connections handled: {self.connections_handled}"
            
        elif command_upper == "QUIT":
            # Client wants to quit
            return "GOODBYE: Connection closing"
            
        else:
            # Unknown command
            return "ERROR: Unknown command"
    
    def cleanup(self):
        """Clean up server resources"""
        self.running = False
        if hasattr(self, 'server_socket'):
            self.server_socket.close()
        print("Server shutdown complete")

def main():
    """Main function to start the server"""
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
            if port < 1025 or port > 49151:
                print("Port must be between 1025 and 49151")
                return
        except ValueError:
            print("Invalid port number")
            return
    else:
        port = 8888  # Default port
    
    server = SimpleTCPServer(port=port)
    
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.cleanup()

if __name__ == "__main__":
    main()