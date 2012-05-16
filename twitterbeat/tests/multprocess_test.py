#!/usr/bin/env python
# encoding: utf-8
"""
multprocess_test.py

Created by Valder Gallo on 2012-05-14.
Copyright (c) 2012 valdergallo. All rights reserved.
"""
import time
from multiprocessing import Process
from functools import partial


class MultiprocessTest(Process):
    def __init__(self, work_queue, mean=0, sd=1):
        Process.__init__(self)
        self.count_runner = 0
        self.KeepAlive = False
        self.work_queue = work_queue
        self.mean = mean
        self.sd = sd
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
                

if __name__ == '__main__':
    mult = MultiprocessTest()
    mult.daemon = True
    mult.start()
    mult.join()
