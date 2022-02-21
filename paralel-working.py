#!/usr/bin/env python

import sys
import time
import urllib.request
import signal
import threading
from multiprocessing import Manager

queue = []
threads = []

RUNNING = True

quit = 0

def data():
    while RUNNING:
        global x
        x = "roee"
        time.sleep(1)
        x = "tal"
        time.sleep(1)

def sig_handler(signum, frame):
    sys.stderr.write("Signal is received:" + str(signum) + "\n")
    global quit
    quit = 1
    global RUNNING
    RUNNING=False

def handle_line(line):
     if not RUNNING:
         return
     if not line:
         return
     if quit > 0:
         return

     arr = line.split()
     response = x

     queue.append(arr[0] + " " + response)

def handle_stdout(n):
     while RUNNING:
         if quit > 0:
           return
         while len(queue) > 0:
             item = queue.pop(0)
             sys.stdout.write(item)
             sys.stdout.flush()
        #  time.sleep(0.5)

def handle_stdin(n):
    while RUNNING:
         line = sys.stdin.readline()
         if not line:
             break
         if quit > 0:
             break
         line = line.strip()
         thread = threading.Thread(target=handle_line, args=(line,))
         thread.start()
         threads.append(thread)

signal.signal(signal.SIGUSR1, sig_handler)
signal.signal(signal.SIGUSR2, sig_handler)
signal.signal(signal.SIGALRM, sig_handler)
signal.signal(signal.SIGINT, sig_handler)
signal.signal(signal.SIGQUIT, sig_handler)
signal.signal(signal.SIGTERM, sig_handler)


data_thread = threading.Thread(target=data)
data_thread.start()

threads.append(data_thread)

stdout_thread = threading.Thread(target=handle_stdout, args=(1,))
stdout_thread.start()

threads.append(stdout_thread)

stdin_thread = threading.Thread(target=handle_stdin, args=(2,))
stdin_thread.start()

threads.append(stdin_thread)

while(RUNNING):
    time.sleep(1)


print("Not RUNNING")
for thread in threads:
    thread.join()
print("All threads stopped.")