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
import pprint
import cPickle as pickle

from googleapiclient.discovery import build
#  }}} imports #

#  global vars {{{ # 
#  client = soundcloud.Client(client_id="BLIKpIMvNL9As25CHX4l9xXLu7KuU5uF")
# Location of file where id's of already visited comments are maintained
comments_path = '~/Documents/coding/trapbot/commented.txt'
api_file = 'google-api.ini'
cse_id = '016449672529328854635:e0dwkvd2jqa'
subreddits = 'test'

# Text to be posted along with comic description
header = '**SoundCloud Links:**\n\n'
footer = '___\n^^[Source&nbsp;code](https://github.com/Kevin-Mok/TrapBot)&nbsp;|&nbsp;Bot&nbsp;created&nbsp;by&nbsp;u/ConfusedFence'

comment_query_limit = 5
search_query_limit = 10
#  track_query_limit = 10

# test comment
comment = ' I’m sure you’ve heard it but\n\nKendrick Lamar - Humble (Skrillex Remix)\n\nAnd these are bangers\n\nMontell2099 - Hunnid on the Drop (Mr. Carmack Remix)\n\nASAP Rocky - Lord Pretty Flacko Joyde 2 (Y2K Remix)\n\nEkali - Babylon (feat. Denzel Curry) (Woodpile flip)\n\nBrockhampton - Stains (Whethan Bootleg)\n\nKrane and B. Lewis - PCP (feat. Nick Row)\n\nSorry bout no links I’m on mobile\n'

with open('search_results-all.p', 'rb') as fp:
    all_search_results = pickle.load(fp)

# Regex used to determine if line is a song name. Matches are assumed to be
# the artist and song name, order being irrelevant.
song_name_regex = '((.+)\s-\s(.+))'
#  all_search_results = []
#  }}} global vars #

#  authenticate() {{{ # 
def authenticate():
    print('Authenticating...\n')
    reddit = praw.Reddit('trapbot')
    print(reddit.user.me())
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit
#  }}} authenticate() #

#  def return_cse_service(): {{{ # 
def return_cse_service():
    file = open(api_file)
    api_key = file.read().strip('\n')
    file.close()
    return build("customsearch", "v1", developerKey=api_key)

#  def get_google_api_key():
    #  file = open(api_file)
    #  api_key = file.read().strip('\n')
    #  file.close()
    #  return api_key
#  }}}  def return_cse_service(): # 

#  split_string_into_words() {{{ # 
# Split given string by spaces and punctuation.
def split_string_into_words(str_in):
    stripped_punctuation = '[]()\'\''
    return [word.strip(stripped_punctuation) for word in str_in.lower().split(' ') if len(word) > 1]
#  }}} split_string_into_words() # 

#  compare_search_with_title(search_words, title_words): {{{ # 
def compare_search_with_title(search_words, title_words):
    search_words_found = []
    for search_word in search_words:
        if search_word in title_words:
            search_words_found.append(search_word)
    words_found = len(search_words_found)
    #  percentage_found = float(words_found) / len(title_words)
    return float(words_found) / len(title_words)
    #  print("Found {0} ({1}) search words in {2} ({3:.2f}%)\n".format(words_found,
        #  search_words_found, title_words, percentage_found * 100))
#  }}} compare_search_with_title() # 

#  get_best_song_url(google_cse_service, query): {{{ #
# todo: remove last arg when actually using
def get_best_song_url(google_cse_service, query, search_results_index):
    #  LIVE/store search code {{{ # 
    # LIVE search
    #  search_results = google_cse_service.cse().list(q=query, cx=cse_id, num=search_query_limit).execute()
    #  all_search_results.append(search_results)
    #  }}} LIVE/store search code # 
    search_results = all_search_results[search_results_index]

    most_similar_percent = 0
    best_url = ''
    for result in search_results['items']:
        url = result['link']
        if 'search' not in url:
            page_title = result['title'].encode("utf-8")
            song_name = result['pagemap']['metatags'][0]['twitter:title']

            search_words = split_string_into_words(query)
            title_words = split_string_into_words(song_name)
            if len(title_words) > 1:
                similar_percent = compare_search_with_title(search_words, title_words)
                if similar_percent > (most_similar_percent + 0.1):
                    most_similar_percent = similar_percent
                    best_url = url

    return best_url
#  }}} get_best_song_url(api_key, query): # 

#  def get_song_url_pairs(song_names_matches): {{{ #
def get_song_url_pairs(song_names_matches):
    song_url_pairs = []
    google_cse_service = return_cse_service()

    # todo: remove when actually using
    results_index = 0
    for match in song_names_matches:
        # combine song name and artist to form search query
        search_query = "{0} {1}".format(match[1], match[2])
        song_url_pairs.append([match[0], get_best_song_url(google_cse_service, search_query, results_index)])
        results_index += 1

    return song_url_pairs

        #  SoundCloud API code {{{ # 
        # using url file to test code so don't have to call SoundCloud API
        #  url_file = open('urls.txt')
        #  title_words_lst = []
        #  for line in url_file:
            #  last_slash_index = line.rfind('/')
            #  if last_slash_index != -1:
                #  title_words = line[last_slash_index + 1:].replace("\n", "").split('-')
                #  title_words_lst.append(title_words)
        # call SoundCloud API to retrieve tracks based on search_query
        #  tracks = client.get('/tracks', q=search_query, limit=track_query_limit)
        #  for track in tracks:
            #  print("Track {0} Possible URL: {1}\n".format(i, track.permalink_url))
            #  url = track.permalink_url
            #  last_slash_index = url.rfind('/')
            #  title_words = url[last_slash_index + 1:].replace("\n", "").split('-')
        #  }}} SoundCloud API code # 
#  }}} get_song_url_pairs() #

def test_comment():
    song_names_matches = re.findall(song_name_regex, comment)
    print(return_comment(get_song_url_pairs(song_names_matches)))

#  def scan_comments(): {{{ # 
def scan_comments():
    reddit = authenticate()
    print("Getting {0} comments...\n".format(comment_query_limit))

    # retrieve comments from reddit
    for comment in reddit.subreddit(subreddits).comments(limit=comment_query_limit):
        song_names_matches = re.findall(song_name_regex, comment.body)

        file_obj_r = open(path,'r')
        if comment.id not in file_obj_r.read().splitlines():
            file_obj_r.close()
            print('Link is new. Posting links.\n')
            post = return_comment(get_song_url_pairs(song_names_matches))
            comment.reply(post)

            file_obj_w = open(path,'a+')
            file_obj_w.write(comment.id + '\n')
            file_obj_w.close()
        else:
            print('Already visited link.\n')

        #  time.sleep(10)

    #  print('Waiting 60 seconds...\n')
    #  time.sleep(60)
#  }}} def scan_comments(): # 

#  def return_comment(song_url_pairs): {{{ # 
# Expects list of lists containing song then URL in that specific order.
def return_comment(song_url_pairs):
    comment = header
    for pair in song_url_pairs:
        #  print("[{0}]({1})".format(pair[0], pair[1]))
        comment += "[{0}]({1})\n\n".format(pair[0], pair[1])
    return comment + footer
#  }}}  def return_comment(song_url_pairs): # 

#  main() {{{ # 
def main():
    #  while True:
        #  scan_comments()
    test_comment()

    #  query = 'Montell2099 Hunnid on the Drop (Mr. Carmack Remix)'

    # store results using cPickle
    #  with open('search_results-all.p', 'wb') as fp:
        #  pickle.dump(all_search_results, fp, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    main()
#  }}} main() #
