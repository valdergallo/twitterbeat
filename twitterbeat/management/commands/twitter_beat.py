#!/usr/bin/env python
# encoding: utf-8
"""
twitter_beat.py

Created by Valder Gallo on 2012-05-05.
Copyright (c) 2012 valdergallo. All rights reserved.
"""

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from twitterbeat import TwitterBeat
from django.conf import settings

options = (
        make_option('--start', action="store_true", dest='start', default=False, 
                    help='Start service to twitter check'),
        make_option('--restart', action="store_true", dest='restart', default=False, 
                    help='Restart service to twitter check'),
        make_option('--stop', action='store_true',dest='stop', default=False, 
            help='Close service'),
        make_option('--status', action='store_true',dest='status', default=False, 
            help='Status service'),
        )
        
TWITTER_BEAT = TwitterBeat('./twitterbeat.pid')

class Command(BaseCommand):
    help = 'Twitter Beat is one service active on background to check updates on status from one user'
    option_list = BaseCommand.option_list + options
    
    def handle(self, *args, **options):
        if options['start']:
            TWITTER_BEAT.start()
        elif options['restart']:
            TWITTER_BEAT.restart()
        elif options['stop']:
            TWITTER_BEAT.stop()
        elif options['status']:
            print 'Status:' , TWITTER_BEAT.KeepAlive
        else:
            print self.help


