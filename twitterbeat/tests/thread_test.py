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

_Event = threading._Event


class Event(_Event):
    # Event from Celery
    if not hasattr(threading._Event, "is_set"):
        is_set = _Event.isSet


class ThereadTest(threading.Thread):
    def __init__(self, threadID=1, name='threding-1'):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.count_runner = 1
        self.is_shutdown = Event()
        

    def stop(self):
        print 'STOOPED \n'
        sys.exit()
            
    def start(self):
        self.is_shutdown.set()
        while True:
            print '%s - Break with the random power!!! \n' % self.count_runner
            if self.count_runner == 3:
                self.stop()
            
            self.count_runner += 1
            time.sleep(1)
        

def main():
    beat = ThereadTest()
    beat.daemon = True
    beat.start()

if __name__ == '__main__':
    main()

