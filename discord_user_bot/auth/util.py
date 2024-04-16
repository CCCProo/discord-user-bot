import string
import time
import json
import os

from random import choice

from faker import Faker
file_name = 'fake.json'
file_path = None

current_dir = os.getcwd()

for root, dirs, files in os.walk(current_dir):
    if file_name in files:
        file_path = os.path.join(root, file_name)
        break

with open(file_path, 'r') as file:
    fake_data = json.load(file)

def random(min_val, max_val):
    return random.uniform(min_val, max_val)

def rrandom(min_val, max_val):
    return round(random(min_val, max_val))

def random_in_array(arr):
    rand = choice(arr)
    return rand

def random_name(length_min, length_max=None):
    length_max = length_max or length_min
    length = rrandom(length_min, length_max)
    return ''.join(random.choice(string.printable) for _ in range(length))

def gen_component(name):
    return random_in_array(fake_data[name])

def gen_ua():
    fake = Faker()
    return fake.user_agent()

async def sleep(ms):
    time.sleep(ms / 1000)

def main():
    return {
        'random': random,
        'rrandom': rrandom,
        'random_in_array': random_in_array,
        'random_name': random_name,
        'gen_component': gen_component,
        'gen_ua': gen_ua,
        'sleep': sleep
    }
