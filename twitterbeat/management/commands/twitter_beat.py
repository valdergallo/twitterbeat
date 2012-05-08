#!/usr/bin/env python
# encoding: utf-8
"""
twiiter_beat.py

Created by Valder Gallo on 2012-05-05.
Copyright (c) 2012 valdergallo. All rights reserved.
"""

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from twitterbeat import TwitterBeat


options = (
        make_option('--start', action='store_true',dest='start', default=False, 
            help='Start service to twiiter check'),
        make_option('--stop', action='store_true',dest='stop', default=False, 
            help='Close service'),
        make_option('--status', action='store_true',dest='status', default=False, 
            help='Status service'),
        )

class Command(BaseCommand):
    help = 'Twitter Beat is one service active on background to check updates on status from one user'
    option_list = BaseCommand.option_list + options
    
    def start_thread(self, *args, **options):
        print 'start'
        self.settigns.TWITTER_BEAT = TwitterBeat()
        self.settigns.TWITTER_BEAT.start()

    def stop_thread(self, *args, **options):
        print 'stop'
        self.settigns.TWITTER_BEAT.stop()

    def status_thread(self, *args, **options):
        print 'status'
        self.settigns.TWITTER_BEAT.KeepAlive
    
    def handle(self, *args, **options):
        print options
        print '---------------------------------------'
        print args
        print self.help
