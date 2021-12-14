#!/usr/bin/env python
# Ovan gör det möjligt att köra python på linux som om det vore en exe

# Importing libraries
import requests
from stem import Signal
from stem.control import Controller
import json
import threading
import random
import string

# Terminal colors
Reset = "\x1b[0m"
FgRed = "\x1b[31m"
FgGreen = "\x1b[32m"
FgYellow = "\x1b[33m"
FgBlue = "\x1b[34m"
FgCyan = "\x1b[36m"

# Generates random string
def get_random_string(length):
    letters = string.ascii_lowercase + string.digits
    # letters = string.ascii_lowercase
    # letters = string.digits
    return ''.join(random.choice(letters) for i in range(length))

# Creates new tor circuit / new ip
def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password=password)
        controller.signal(Signal.NEWNYM)

# Creates a session which is used to make https / http requests
def get_tor_session():
    session = requests.session()
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session

# Get ip-address in use
def get_ip():
    session = get_tor_session()
    r = session.get('https://httpbin.org/ip')
    j = r.json()
    return j['origin']

# Main request function
def req(name, ip):
    # Request to protonmail
    def protonmail(name, ip):
        session = get_tor_session()
        r = session.get(f'https://mail.protonmail.com/api/users/available?Name={name}', headers={"x-pm-appversion":"Web_3.16.61"})
        j = r.json()
        if j['Code'] == 1000:
            print(f'{FgBlue}{ip}{Reset} [{FgCyan}Protonmail{Reset}] {FgGreen}Avail{Reset} {name}')
            f = open('./output.txt', "a")
            f.write(f"{name}\n")
            f.close()
        elif j['Code'] == 12106:
            print(f'{FgBlue}{ip}{Reset} [{FgCyan}Protonmail{Reset}] {FgRed}Taken{Reset} {name}')
        else:
            print(f'{FgBlue}{ip}{Reset} [{FgCyan}Protonmail{Reset}] {FgYellow}Limit{Reset} {name}')

    protonmail(name, ip)

# Main loop
def loop(length):
    renew_connection()
    threads = []
    ip = get_ip()

    # Multithreading
    for i in range(thread_count):
        if length > 0:
            u = get_random_string(length)
        else:
            u = random.choice(wordlist)
        threads.append(threading.Thread(target=req, args=(u, ip,)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Repeat when done
    loop(length)

password = input('Enter password for Tor: ')

try:
    thread_count = int(input('Enter amount of threads to use: '))
except:
    print('Not an integer!')
    exit(0)
username_type = input('What dictionary do you want to use?\n1. Wordlist\n2. Random char\n>> ')
if username_type == '1':
    # Select path to wordlist
    path = input('Enter path to wordlist: ')
    # List of usernames to test
    wordlist = []
    f = open(path)
    wordlist = f.read().split('\n')
    f.close()
    loop(0)
elif username_type == '2':
    try:
        length = int(input('Enter Random Char length to use: '))
    except:
        print('Not an integer!')
        exit(0)
    loop(length)
else:
    print('You failed to choose between 1 and 2...')