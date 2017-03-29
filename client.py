'''
Created on 29.3.2017

@author: T
'''

import socket
import time
import threading
from datetime import datetime
import sys

HOST = "127.0.0.1"
BUFFER_SIZE = 1024
DEBUG = True

def debug(string):
    if (DEBUG):
        print("{} DEBUG: {}".format(datetime.now(), string))

def connect(host, nick):
    msg = "CONNECT\n" + nick + "\n\0"
    s.connect((HOST, 2000))
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
    while 1:
        time.sleep(10)
        msg = "KEEPALIVE\n" + nick + "\n\0"
        s.send(msg.encode(encoding='utf_8'))
        debug("10 sekuntia meni -> KEEPALIVE")

def listen_messages():
    debug("kuuntelija started")
    while 1:
        rec = s.recv(BUFFER_SIZE).decode()
        osat = rec.split("\n")
        debug(osat)
        debug(rec)
        if osat[0] == "BROADCAST":
            print(osat[1] + ": " + osat[2])


host = input("Syota ip")
nick = input("Syota nick")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect(host, nick)

#luodaan laskuri
laskuri = threading.Thread(target=keep_alive, args=())
laskuri.start()
#luodaan viestien kuuntelija
kuuntelija = threading.Thread(target=listen_messages, args=())
kuuntelija.start()

#odotetaan kayttajan kirjoittavan viestin tai lopettavan ohjelman -quit-komennolla
while 1:
    syote = input()
    if syote == "-quit":
        disconnect()
        break
    else:
        send_message(syote)
        #Yrityksia poistaa kayttajan syote koska tulee muuten kahteen kertaan
        #print("", end="\r")
        #sys.stdout.write("\r")
    
debug("Stopped")