#!/usr/bin/env python

from __future__ import print_function
import sys
import json
import datetime
import PyRSS2Gen as RSS
import requests
import urllib
import re

URL = "https://itunes.apple.com/us/rss/topvideorentals/limit=100/json"
iTunes_build = ''


def itunes(itunes_url):
    titles = []
    response = requests.get(url=itunes_url)
    if response.status_code is 200:
        iTunes_results = json.loads(response.text)
        global iTunes_build
        iTunes_build = iTunes_results['feed']['updated']['label']
        for title in iTunes_results['feed']['entry']:
            titles.append(re.sub('\s?\(.*\)', '', title['im:name']['label']))
        return titles
    else:
        print("Error: {0}".format(response.status_code))


def omdb(movie_list):
    omdb_id = []
    for title in movie_list:
        url_title = urllib.quote("t=" + title, safe='=')
        response = requests.get('http://www.omdbapi.com/?{}'.format(url_title))
        omdb_results = json.loads(response.text)
        if omdb_results['Response'] == "True":
            omdb_id.append({'title': title,
                            'imdbID': omdb_results['imdbID'],
                            'year': omdb_results['Year']})
        else:
            print("Error: {0} - {1}".format(title, omdb_results['Error']))
    return omdb_id


def rss(movieDict):
    item_list = []
    for item in movieDict:
        imdb_url = "http://www.imdb.com/title/{0}".format(item['imdbID'])
        title = item['title']
        year = item['year'].encode('utf-8')
        movie_name = "{0} ({1})".format(title, year)
        movie = RSS.RSSItem(title="{0}".format(movie_name),
                            link=imdb_url,
                            guid=imdb_url)
        item_list.append(movie)
    rss = RSS.RSS2(
        title="Top 100 iTunes Movies built for Radarr",
        link="http://www.cloudsrvr.io/topmovies.xml",
        description="",
        pubDate=iTunes_build,
        lastBuildDate=datetime.datetime.now(),
        items=item_list)
    with open("topmovies.xml", "w") as f:
        rss.write_xml(f)

rss(omdb(itunes(URL)))
