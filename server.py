#!/usr/bin/env python3

import socket
import threading
from functools import partial
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000
DEBUG = True
def debug(string):
    if (DEBUG):
        print("{} DEBUG: {}".format(datetime.now(), string))

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

def broadcast(message, username, recipients):
    debug("Broadcasting message '{}'".format(message))
    for rec in recipients:
        response = "BROADCAST\n{}\n{}\n".format(username, message)
        try:
            rec.send(response.encode())
        except OSError:
            debug("ERROR: Couldn't broadcast message to {}".format(str(rec)))

def do_command(command, username, body, bc):
    if command == "CONNECT":
        bc("User {} has connected".format(username), username)
    elif command == "DISCONNECT":
        bc("User {} has disconnected".format(username), username)
    elif command == "MESSAGE":
        bc("{}: {}".format(username, body), username)
    elif command == "KEEPALIVE":
        pass
    else:
        debug("Unknown command '{}' from user '{}'".format(command, username))

def keep_connection(conn, addr, connections):
    debug("Connection from: {}".format(addr))

    broadcast_fun = partial(broadcast, recipients=connections)
    while True:
        data = conn.recv(1024).decode()

        if not data:
            break

        data_tuple = parse_message(str(data))
        if not data_tuple:
            debug("Failed to parse data from client")
            continue

        command, username, body = data_tuple
        do_command(command, username, body, broadcast_fun)

    conn.close()
    connections.remove(conn)
    debug("Closed connection to: {}".format(addr))

def main():
    mySocket = socket.socket()
    mySocket.bind((HOST, PORT))

    connections = []
    threads = []
    mySocket.listen(1)
    running = True

    while running:
        conn, addr = mySocket.accept()
        t = threading.Thread(target=keep_connection, args=(conn, addr, connections))
        threads.append(t)
        connections.append(conn)
        t.daemon = True
        t.start()

if __name__ == '__main__':
    main()
