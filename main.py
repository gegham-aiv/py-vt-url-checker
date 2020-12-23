from inc.vtclient import VTClient
import os
import sys
from datetime import datetime

def info(message):
    date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f'[INFO]: [{date_time}] {message}')

if len(sys.argv) < 2:
    print('Please provide the path to directory where the files are located:')
    path = input()
else:
    path = sys.argv[1]

if not os.path.isdir(path):
    print('Invalid path provided. Exiting')
    exit()

files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

vt_client = VTClient()

info(f"Total {len(files)} files detected")
for file in files:
    info(f"Reading file {file}")
    file_path = f"{path}/{file}"
    file_handler = open(file_path, 'r')
    lines = file_handler.readlines()

    for hostname in lines:
        info(f"Checking hostname: {hostname}")
        score = vt_client.is_host_secure(hostname)
        # message = 'secure' if score > 0 else 'insecure'
        info(f"Score: {score}")