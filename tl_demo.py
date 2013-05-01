#!/usr/bin/python
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 4321))
sock.send("STATE 1\r\n")
time.sleep(1)
sock.send("STATE 2\r\n")
time.sleep(1)
sock.send("STATE 4\r\n")
time.sleep(1)
for i in range(1, 8):
   sock.send("STATE "+str(i))
   time.sleep(1)

sock.send("STATE 0\r\n")
time.sleep(1)
sock.send("QUIT\r\n")
