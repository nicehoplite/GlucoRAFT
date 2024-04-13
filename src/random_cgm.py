import subprocess
import random
import time

def generate_random_value():
    # Generate a random integer between 1 and 100
    return random.randint(1, 100)

def update_value_command(addr, key):
    value = generate_random_value()
    command = f"python3 client.py {addr} {key} '{value}'"
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    # Define the server address and key
    server_address = "http://127.0.0.1:8002"
    key = "name"

    while True:
        update_value_command(server_address, key)
        # Wait for 5 seconds before updating again
        time.sleep(5)
