''' This script represents the patient device that will be interacting with the servers by sending daily updates on cgm values and percentages'''

import subprocess
import random
import time
hypo_percent=0
hyper_percent=0
inrange_percent=0

def generate_random_value():
    
    level=""
    x=random.randint(50, 250)
    if x<=70:
        level="Hypoglycemia"
    elif x>=180:
        level="Hyperglycemia"
    else:
        level="In Range"
     

def update_value_command(addr, key):
    value = generate_random_value()
    command = f"python3 client.py {addr} {key} '{value}'"
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    # Define the server address and key
    server_address = "http://127.0.0.1:8002" 
    key = "Shreyas"

    while True:
        update_value_command(server_address, key)
        # Wait for 5 seconds before updating again
        time.sleep(5)
