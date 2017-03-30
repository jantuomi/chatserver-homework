#!/usr/bin/env python3
'''
Created on 29.3.2017

@author: T
'''

import socket
import time
from time import gmtime, strftime

import threading
import signal
from datetime import datetime
import sys

DEFAULT_HOST = "127.0.0.1"
PORT = 5000
DEFAULT_NICK = "Anonymous"
BUFFER_SIZE = 1024
DEBUG = False
running = True

def debug(string):
    if (DEBUG):
        print("{} DEBUG: {}".format(datetime.now(), string))

def signal_handler(signal, frame):
    print("Closing sockets and shutting down...")
    global running
    running = False
    disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def connect(host, nick):
    msg = "CONNECT\n" + nick + "\n\0"
    s.connect((host, 5000))
    debug("connected")
    s.send(msg.encode(encoding='utf_8'))
    
def disconnect():
    msg = "DISCONNECT\n" + nick + "\n\0"
    s.send(msg.encode(encoding='utf_8'))
    
def send_message(viesti):
    msg = "MESSAGE\n" + nick + "\n" + viesti + "\0"
    s.send(msg.encode(encoding='utf_8'))
    
def keep_alive():
    debug("laskuri started")
    while running:
        # kikka kakkonen sille, että ohjelman sulkeutuminen tarkistetaan sekuntin välein
        # 10 sekuntin sijaan
        for i in range(10):
            if not running:
                break

            time.sleep(1)

        msg = "KEEPALIVE\n" + nick + "\n\0"
        s.send(msg.encode(encoding='utf_8'))
        debug("10 sekuntia meni -> KEEPALIVE")

def listen_messages():
    debug("kuuntelija started")
    while running:
        rec = s.recv(BUFFER_SIZE).decode()
        osat = rec.split("\n")
        if osat[0] == "BROADCAST":
            username = osat[1]
            body = osat[2]
            debug(username)
            debug(body)
            if username != nick:
                timestamp = strftime("%H:%M:%S", gmtime())
                print("{} {}: {}".format(timestamp, username, body))

host = input("Host [{}]: ".format(DEFAULT_HOST))
nick = input("Nickname [{}]: ".format(DEFAULT_NICK))
if len(host) == 0:
    host = DEFAULT_HOST

if len(nick) == 0:
    nick = DEFAULT_NICK

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect(host, nick)

#luodaan laskuri
laskuri = threading.Thread(target=keep_alive, args=())
laskuri.start()
#luodaan viestien kuuntelija
kuuntelija = threading.Thread(target=listen_messages, args=())
kuuntelija.start()

#odotetaan kayttajan kirjoittavan viestin tai lopettavan ohjelman -quit-komennolla
print("Type '-quit' to exit.")
while running:
    syote = input()
    if syote == "-quit":
        disconnect()
        running = False
        break
    else:
        send_message(syote)
        #Yrityksia poistaa kayttajan syote koska tulee muuten kahteen kertaan
        #print("", end="\r")
        #sys.stdout.write("\r")
    
debug("Stopped")
