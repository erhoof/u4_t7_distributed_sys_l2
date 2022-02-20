import base64
import ipaddress
import requests
import random
import json
import os

import numpy as np
from concurrent.futures import ThreadPoolExecutor
from requests_futures.sessions import FuturesSession
from base64 import urlsafe_b64encode, urlsafe_b64decode

session = FuturesSession(executor=ThreadPoolExecutor(max_workers=10))

# Hardcode some values
os.environ["LAB_SUBNET"] = "127.0.0.1/32"
filename = "../steve.jpg"

# Hosts
hosts = []

# Discovery hosts 
network = ipaddress.ip_network(os.getenv("LAB_SUBNET"))
for host in network:
    print(f"Trying to connect to {host}")
    try:
        resp = requests.get(f"http://{host}:5000/status")
    except Exception as e:
        print(f" - connect error")
        continue

    if resp.status_code == 200:
        print(f" - added!")
        hosts.append(host)
    else:
        print(f" - ignore: {resp.status_code}")

def encrypt():
    print("encrypt called!")

    # Open and split file
    data_to_encrypt = []
    with open(filename, "rb") as f:
        data_to_encrypt = urlsafe_b64encode(f.read())

    print(f"len of file: {len(data_to_encrypt)}")

    # Split data
    hosts_count = len(hosts)
    print(f"Count of hosts: {hosts_count}")
    data_chunks = np.array_split(list(data_to_encrypt), hosts_count)

    # Send data chunks
    futures = []
    for i in range(hosts_count):
        host = random.choice(hosts)
        futures.append(session.put(f"http://{host}:5000/encrypt", json.dumps({'id': i, 'data': data_chunks[i].tolist()})))

    # Receive data
    incoming_data_chunks = dict()
    for future in futures:
        response = future.result()
        data = json.loads(response.content)
        id = data['id']
        print(f"response: {id} - {response.status_code}")
        incoming_data_chunks[id] = data['data']

    # Complete file data
    with open('encrypted.json', 'w', encoding='utf-8') as f:
        json.dump(incoming_data_chunks, f, ensure_ascii=False, indent=4)

    # End
    print("Succesfully encrypted!")

def decrypt():
    print("decrypt called!")

    data = dict()
    with open('encrypted.json', 'r') as f:
        data = json.load(f)

    futures = []
    for id in data.keys():
        # Convert int bytearray -> base64
        data_bin = bytearray(data[id])
        print(f"data_bin len: {len(data_bin)}")

        data_base64 = urlsafe_b64encode(data_bin)
        print(f"data_base64 len: {len(data_base64)}")

        data_str = str(data_base64)
        print(f"data_str len: {len(data_str)}")

        host = random.choice(hosts)
        futures.append(session.put(f"http://{host}:5000/decrypt", json.dumps({'id': id, 'data': data_str})))

    # Receive data
    incoming_data_chunks = dict()
    for future in futures:
        response = future.result()
        data = json.loads(response.content)
        id = data['id']
        print(f"response: {id} - {response.status_code}")
        incoming_data_chunks[id] = data['data']

    # Restore file
    file_array = []
    for id in range(len(incoming_data_chunks.keys())):
        print(f"len idc: {len(incoming_data_chunks[str(id)])}")
        print(type(incoming_data_chunks[str(id)]))
        file_array += incoming_data_chunks[str(id)]

    # Convert file_array -> base 64 -> bytearray
    file_base64 = urlsafe_b64decode(bytes(file_array))
    file_array_bin = bytearray(file_base64)

    # Write file
    with open("out.jpg", "wb") as f:
        print(f"len file_array: {len(file_array_bin)}")
        f.write(file_array_bin)

    # End
    print("Finished!")

    pass

#encrypt()
decrypt()


