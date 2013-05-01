#!/usr/bin/python
import socket
import time
import sys
import gzip
import csv
import math
from time import strftime

state=0

with gzip.open(sys.argv[8], "r") as f:
        f.readline()
        data = f.readline().strip()
        reader = csv.reader(data, delimiter=",", quotechar='"')
        percentage=float(reader.next()[0])
f.close()

if percentage < 40:
        state = 0
elif percentage <= 50:
        state = 4
elif percentage <= 65:
        state = 2
else:
        state = 1

with open("/tmp/tl.log", "a") as f:
        f.write("[%s] Percentage: %f - State: %d\n" %
                (strftime("%Y-%m-%d %X %z"), percentage, state))
f.close()

try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", 4321))
        sock.send("state %d\r\n" % state)
        time.sleep(1)
        sock.send("quit")
        sock.close()

except socket.error:
        print "Closed socket"
        sys.exit(1)
