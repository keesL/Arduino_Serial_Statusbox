#!/usr/bin/python
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 4321))
while True:
   try:
      sock.send("state 7 \r\n")
      time.sleep(1)
      sock.send("state 0 \r\n")
      time.sleep(1)
   except Error:
      sock.shutdown()
      sock.close()
