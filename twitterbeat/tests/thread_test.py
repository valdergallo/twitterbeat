#!/usr/bin/env python
# encoding: utf-8
"""
test.py

Created by Valder Gallo on 2012-05-12.
Copyright (c) 2012 valdergallo. All rights reserved.
"""
import sys
import threading
import time


class ThereadTest(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.count_runner = 0
        self.KeepAlive = False
        self.open_file = open('./output.log', 'w')

    def stop(self):
        print 'STOOPED \n'
        self.open_file.close()
        self.KeepAlive = False
        raise SystemExit()

    def handle(self):
        self.open_file.write('Break with the random power!! \n')
        time.sleep(1)

    def run(self):
        self.KeepAlive = True
        while True:
            if self.count_runner == 3:
                self.KeepAlive = False

            if self.KeepAlive:
                self.handle()
                self.count_runner += 1
            else:
                self.stop()
        

def main():
    beat = ThereadTest()
    beat.start()

if __name__ == '__main__':
    main()

