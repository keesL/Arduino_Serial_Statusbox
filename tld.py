#!/usr/bin/python

from socket import *
from thread import *

import serial
import signal
import sys

host=""
port=4321

sock=socket()
conn=socket()

def clientThread(conn):
        state=0

        conn.send("100 OK Connection Accepted.\r\n")
        while True:
                data = conn.recv(1024).strip().upper().split()
                if data[0] == "QUIT":
                        conn.send("999 Goodbye!")
                        print "Peer ",conn.getpeername()," disconnected."
                        conn.close()
                        return

                elif data[0] == "RED":
                        if data[1] == "ON":
                                if (state & 1) != 1:
                                        state = state + 1
                        elif data[1] == "OFF":
                                if (state & 1) == 1:
                                        state = state - 1
                        conn.send("101 state %d\r\n" % state)
                        ser.write("%s" % state)

                elif data[0] == "AMBER":
                        if data[1] == "ON":
                                if (state & 2) != 2:
                                        state = state + 2
                        elif data[1] == "OFF":
                                if (state & 2) == 2:
                                        state = state - 2
                        conn.send("101 state %d\r\n" % state)
                        ser.write("%s" % state)

                elif data[0] == "GREEN":
                        if data[1] == "ON":
                                if (state & 4) != 4:
                                        state = state + 4
                        elif data[1] == "OFF":
                                if (state & 4) == 4:
                                        state = state - 4
                        conn.send("101 state %d\r\n" % state)
                        ser.write("%s" % state)

                elif data[0] == "STATE":
                        state = int(data[1])

                        conn.send("101 state %d\r\n" % state)
                        ser.write("%s" % state)

                elif data[0] == "STATUS":
                        red = amber = green = "off"
                        if (state & 1 == 1):
                                red = "on"
                        if (state & 2 == 2):
                                amber = "on"
                        if (state & 4 == 4):
                                green = "on"

                        conn.send("102 STATUS: (red,amber,green)=(%s, %s, %s)\r\n" % (red, amber, green))


def serverThread():
        sock.bind((host,port))
        sock.listen(5)
        print "Listening on ",host,":",port
        while True:
                (conn, addr) = sock.accept()
                print "Incoming connection from ",addr
                start_new_thread(clientThread, (conn,))


def setupSerial():
        global ser
        ser = serial.Serial(
                port="/dev/ttyS0",
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
        )
        ser.open()
        if (ser.isOpen()):
           print "Serial port opened successfully."
        else:
           print "Serial port FAILED to open."

def signalHandler(signum, frame):
   if signum == signal.SIGINT:
      print "Caught interrupt signal. Closing down gracefully."
      sock.close()
      sys.exit(0)

signal.signal(signal.SIGINT, signalHandler)
setupSerial()
serverThread()

