#  imports {{{ # 
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
#  from urllib.parse import urlparse
from urlparse import urlparse

import praw
import time
import re
import requests
import bs4
import soundcloud
#  }}} imports #

#  global vars {{{ # 
#  client = soundcloud.Client(client_id="BLIKpIMvNL9As25CHX4l9xXLu7KuU5uF")
# Location of file where id's of already visited comments are maintained
path = '~/Documents/coding/trapbot/commented.txt'
subreddits = 'test'

# Text to be posted along with comic description
header = '**SoundCloud Links:**\n'
footer = '\n Bot created by u/ConfusedFence | [Source
code](https://github.com/Kevin-Mok/TrapBot)*'

comment_query_limit = 5
#  track_query_limit = 10

# test comment
comment = ' I’m sure you’ve heard it but\n\nKendrick Lamar - Humble (Skrillex Remix)\n\nAnd these are bangers\n\nMontell2099 - Hunnid on the Drop (Mr. Carmack Remix)\n\nASAP Rocky - Lord Pretty Flacko Joyde 2 (Y2K Remix)\n\nEkali - Babylon (feat. Denzel Curry) (Woodpile flip)\n\nBrockhampton - Stains (Whethan Bootleg)\n\nKrane and B. Lewis - PCP (feat. Nick Row)\n\nSorry bout no links I’m on mobile\n'
#  }}} global vars #

#  authenticate() {{{ # 
def authenticate():
    print('Authenticating...\n')
    reddit = praw.Reddit('trapbot')
    print(reddit.user.me())
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit
#  }}} authenticate() #

#  run_trapbot() {{{ # 
def run_trapbot(reddit):
    # Regex used to determine if line is a song name. Matches are assumed to be
    # the artist and song name, order being irrelevant.
    song_name_regex = '(.+)\s-\s(.+)'
    #  print("Getting {0} comments...\n".format(comment_query_limit))

    # retrieve comments from reddit
    #  for comment in reddit.subreddit(subreddits).comments(limit=comment_query_limit):
    #  song_names = re.findall("(.+)\s-\s(.+)", comment.body)
    song_names = re.findall(song_name_regex, comment)
    #  if len(song_names) > 0:
    for i in range(0, len(song_names)):
        # combine song name and artist to form search query
        search_query = "{0} {1}".format(song_names[i][0], song_names[i][1])
        search_words = search_query.split(" ")

        # using url file to test code so don't have to call SoundCloud API
        url_file = open('urls.txt')
        title_words_lst = []
        for line in url_file:
            last_slash_index = line.rfind('/')
            if last_slash_index != -1:
                title_words = line[last_slash_index + 1:].replace("\n", "").split('-')
                title_words_lst.append(title_words)
        # call SoundCloud API to retrieve tracks based on search_query
        #  tracks = client.get('/tracks', q=search_query, limit=track_query_limit)
        #  for track in tracks:
            #  print("Track {0} Possible URL: {1}\n".format(i, track.permalink_url))
            #  url = track.permalink_url
            #  last_slash_index = url.rfind('/')
            #  title_words = url[last_slash_index + 1:].replace("\n", "").split('-')
        
        # *** UNFINISHED ***
        # check how many search words are actually in track title to see if it
        # at least somewhat matches
        search_words_matched = 0
        for title_words in title_words_lst:
            print(search_words)
            for search_word in search_words:
                if search_word in title_words:
                    search_words_matched += 1
                    print("'{0}' was found in '{1}'".format(search_word, title_words))
            percentage_found = search_words_matched / len(title_words)
            print("Found {0} search words in \
                    {1} ({2})".format(search_words_matched, title_words, \
                        percentage_found))

        #  post comment if haven't found this comment already {{{ # 
        #  file_obj_r = open(path,'r')

        #  if comment.id not in file_obj_r.read().splitlines():
            #  print('Link is unique...posting explanation\n')
            #  comment.reply(header + explanation + footer)

            #  file_obj_r.close()

            #  file_obj_w = open(path,'a+')
            #  file_obj_w.write(comment.id + '\n')
            #  file_obj_w.close()
        #  else:
            #  print('Already visited link...no reply needed\n')

        #  time.sleep(10)

    #  print('Waiting 60 seconds...\n')
    #  time.sleep(60)
        #  }}} post comment if haven't found this comment already # 
#  }}} run_trapbot() #

#  main() {{{ # 
def main():
    #  reddit = authenticate()
    #  while True:
        #  run_trapbot(reddit)
    run_trapbot(0)

if __name__ == '__main__':
    main()
#  }}} main() #