#!/usr/bin/env python3
import websockets
import asyncio
from time import sleep
from signalz.generators.ecgsyn import ecgsyn 

uri = "ws://localhost:9969"
interval = 0.05
epsilon = 0.1

def multiply_list(random_list, nbr):
    random_values_new = list()
    for i in range(len(random_list)):
        random_values_new.append(random_list[i] * nbr)
    return random_values_new


def flatten(random_list):
    random_values_new = list()
    for i in range(len(random_list)):
        random_values_new.append(random_list[i])
        if i != len(random_list) - 1:
            random_values_new.append((random_list[i] + random_list[i + 1]) / 2)
    return random_values_new

def flatten_near_zero(random_list):
    random_values_new = list()
    random_values_new.append(random_list[0])
    for i in range(1, len(random_list)):
        random_values_new.append(random_list[i])
        if (((-epsilon < random_list[i] and random_list[i] < -0.01) or (0.01 < random_list[i] and random_list[i] < epsilon)) and (random_list[i - 1] - random_list[i] > 0.15)):
            random_values_new.append(random_list[i])
    return random_values_new

def increment_high_value(random_list):
    for i in range(len(random_list)):
        if random_list[i] > 0.8:
            random_list[i] *= 2
    return random_list

random_values = ecgsyn(sfecg=16, n=4, hrmean=80.0)[0].tolist()
random_values = flatten_near_zero(random_values)
random_values = increment_high_value(random_values)
random_values = multiply_list(random_values, 1000)

print(f"Connecting to WebSocket : '{uri}'")

async def send_random_data():
    async with websockets.connect(uri) as websocket:
        for i in range(len(random_values)):
            await websocket.send(str(random_values[i]))
            sleep(interval)

asyncio.get_event_loop().run_until_complete(send_random_data())
