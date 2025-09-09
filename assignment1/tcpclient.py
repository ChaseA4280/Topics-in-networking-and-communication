"""
Simple TCP Client Implementation
Assignment 1 - TCP Socket Communication
"""

import socket
import sys
import time

class SimpleTCPClient:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
    
    def connect_and_execute(self, command):
        """Connect to server, execute command, and disconnect"""
        try:
            # Create socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            print(f"\n--- Connecting to {self.host}:{self.port} ---")
            
            # Connect to server
            client_socket.connect((self.host, self.port))
            print("Connected successfully!")
            
            # Receive welcome message
            welcome = client_socket.recv(1024).decode('utf-8').strip()
            print(f"Server welcome: {welcome}")
            
            # Send command
            print(f"Sending command: {command}")
            client_socket.send(f"{command}\n".encode('utf-8'))
            
            # Receive response
            response = client_socket.recv(1024).decode('utf-8').strip()
            print(f"Server response: {response}")
            
            # Send quit command
            print("Sending QUIT command")
            client_socket.send("QUIT\n".encode('utf-8'))
            
            # Receive goodbye message
            goodbye = client_socket.recv(1024).decode('utf-8').strip()
            print(f"Server goodbye: {goodbye}")
            
        except ConnectionRefusedError:
            print(f"Error: Could not connect to server at {self.host}:{self.port}")
            print("Make sure the server is running.")
        except Exception as e:
            print(f"Client error: {e}")
        finally:
            client_socket.close()
            print("Connection closed")

def main():
    """Main function to run the client"""
    host = 'localhost'
    port = 8888
    
    # Parse command line arguments
    if len(sys.argv) >= 3:
        host = sys.argv[1]
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("Invalid port number")
            return
    elif len(sys.argv) == 2:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number")
            return
    
    print(f"Simple TCP Client - Assignment 1")
    print(f"Target server: {host}:{port}")
    
    client = SimpleTCPClient(host, port)
    
    # First connection - Execute TIME command
    print("\n" + "="*50)
    print("FIRST CONNECTION - TIME COMMAND")
    print("="*50)
    client.connect_and_execute("TIME")
    
    # Wait a moment between connections
    time.sleep(1)
    
    # Second connection - Execute ECHO command
    print("\n" + "="*50)
    print("SECOND CONNECTION - ECHO COMMAND")
    print("="*50)
    client.connect_and_execute("ECHO Hello from TCP Client!")
    
    print("\n" + "="*50)
    print("CLIENT DEMONSTRATION COMPLETE")
    print("="*50)
    
    # Optional: Interactive mode
    while True:
        try:
            print("\nWould you like to test more commands? (y/n): ", end="")
            choice = input().lower()
            
            if choice != 'y':
                break
                
            print("Available commands: TIME, ECHO [message], STATUS")
            command = input("Enter command: ").strip()
            
            if command:
                print(f"\n--- Testing command: {command} ---")
                client.connect_and_execute(command)
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()