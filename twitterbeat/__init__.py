#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by Valder Gallo on 2012-05-10.
Copyright (c) 2012 valdergallo. All rights reserved.
"""
import time
import re
import sys
from datetime import datetime

import twitter
import feedparser

from django.conf import settings
from twitterbeat.models import Account, Tweet, ConnectionError
from twitterbeat.daemon import Daemon

from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
 

class TwitterBeat(Daemon):
    
    def __init__(self, pidfile, *args, **kwargs):
        super(TwitterBeat, self).__init__(self, *args, **kwargs)
        self.count_runner = 0
        self.KeepAlive = False
        self.pidfile = pidfile
        
        user_id  = getattr(settings, 'TWITTER_USER_ID', 
                            Account.objects.filter(active=True).latest('id').id)
                            
        self.twitter_user = Account.objects.get(id=user_id, active=True)
        self.twitter_rss = 'http://api.twitter.com/1/statuses/user_timeline.rss?screen_name=%s' \
                       % self.twitter_user.username

    @staticmethod
    def _get_status_id_from_link(link):
        item = re.findall(r'/(\d+)', link)
        if len(item):
            return item.pop()
        else:
            return None
            
    @staticmethod
    def _convert_datetime(created_at_string):
        """Convert string to datetime"""
        fmt = '%a %b %d %H:%M:%S +0000 %Y' #Tue Apr 26 08:57:55 +0000 2011
        return datetime.strptime(created_at_string, fmt)
        
    def parse_rss(self):
        """
        #fields
            t.entries[0].published_parsed #created_at
            t.entries[0].link #urls
            t.entries[0].id #id - need parse
            t.entries[0].summary #text
            t.entries[0].title #title
        """
        tweets = feedparser.parse(self.twitter_rss)
        parsed = []
        for tweet in tweets.entries:
            parsed.append({
            'created_at': tweet.published_parsed,
            'link': tweet.link,
            'text': tweet.summary.replace('%s:' % self.twitter_user.username, ''),
            'status_id': self._get_status_id_from_link(tweet.link),
            })
        return parsed
    
    def parse_tweet(self):
        """
         #fields 
            tweet.text
            tweet.created_at
            tweet.urls
            tweet.user.name
            tweet.id
        """
        api = twitter.Api()
        try:
            tweets = api.GetUserTimeline(self.twitter_user, count=10)
        except Exception, e:
            ConnectionError.objects.create(text=e)
            return self.parse_rss()
        parsed = []
        for tweet in tweets:
            parsed.append({
            'created_at': self._convert_datetime(tweet.created_at),
            'link': "https://twitter.com/#!/%s/status/%s" % (tweet.user.name, tweet.id),
            'text': tweet.text,
            'status_id': tweet.id,
            })
        return parsed
    
    def handle(self):
        tweets = self.parse_tweet()
        
        for tweet in tweets:
            tw , created = Tweet.objects.get_or_create(**tweet)
            if created:
                LogEntry.objects.log_action(
                    user_id         = self.twitter_user.pk, 
                    content_type_id = ContentType.objects.get_for_model(Tweet).pk,
                    object_repr     = 'twitterbeat', 
                    object_id       = tw.pk,
                    action_flag     = ADDITION
                )
                
        time.sleep(60)
    
    def stop(self):
        self.KeepAlive = False
        super(TwitterBeat, self).stop()
    
    def run(self):
        self.KeepAlive = True
        while True:
            self.handle()
            if self.twitter_user.active:
                self.count_runner += 1
            else:
                self.stop()


if __name__ == "__main__":
    beat = TwitterBeat('./twitterbeat.pid')
    beat.start()
