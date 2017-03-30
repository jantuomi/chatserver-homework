#!/usr/bin/env python3

import socket
import threading
import signal
import sys
from functools import partial
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000
DEBUG = True
running = True

def debug(string):
    if (DEBUG):
        print("{} DEBUG: {}".format(datetime.now(), string))

def signal_handler(signal, frame):
    print("Closing sockets and shutting down...")
    global running
    running = False
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def parse_message(text):
    rows = text.split('\n')
    if (len(rows) < 3):
        return None

    try:
        command = rows[0].strip()
        username = rows[1].strip()
        body = rows[2].strip()
    except:
        return None

    debug("Command '{}' from '{}' with body '{}'".format(command, username, body))
    return (command, username, body)

online_nicks = []
def send_online_nicks(recipient):
    msg = "Online users: " + ", ".join(online_nicks)
    response = "BROADCAST\nSERVER\n{}\n".format(msg)
    try:
        recipient.send(response.encode())
    except OSError:
        debug("ERROR: Couldn't broadcast message to {}".format(str(rec)))

def broadcast(message, username, recipients):
    debug("Broadcasting message '{}'".format(message))
    for rec in recipients:
        response = "BROADCAST\n{}\n{}\n".format(username, message)
        try:
            rec.send(response.encode())
        except OSError:
            debug("ERROR: Couldn't broadcast message to {}".format(str(rec)))

def do_command(command, username, body, bc, sender):
    if command == "CONNECT":
        online_nicks.append(username)
        send_online_nicks(sender)
        bc("User {} has connected".format(username), username)
    elif command == "DISCONNECT":
        bc("User {} has disconnected".format(username), username)
        online_nicks.remove(username)
    elif command == "MESSAGE":
        bc("{}".format(body), username)
    elif command == "KEEPALIVE":
        pass
    else:
        debug("Unknown command '{}' from user '{}'".format(command, username))

def keep_connection(conn, addr, connections):
    debug("Connection from: {}".format(addr))

    broadcast_fun = partial(broadcast, recipients=connections)
    while running:
        data = conn.recv(1024).decode()

        if not data:
            break

        data_tuple = parse_message(str(data))
        if not data_tuple:
            debug("Failed to parse data from client")
            continue

        command, username, body = data_tuple
        do_command(command, username, body, broadcast_fun, conn)

    conn.close()
    connections.remove(conn)
    debug("Closed connection to: {}".format(addr))

def main():
    sock = socket.socket()
    sock.bind((HOST, PORT))

    connections = []
    threads = []
    sock.listen(1)

    print("Chat server running on {}:{}".format(HOST, PORT))
    print("Press CTRL-C to quit")

    while running:
        conn, addr = sock.accept()
        t = threading.Thread(target=keep_connection, args=(conn, addr, connections))
        threads.append(t)
        connections.append(conn)
        t.daemon = True
        t.start()

if __name__ == '__main__':
    main()
