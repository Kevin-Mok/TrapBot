#  imports {{{ # 
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib import quote
from urlparse import urlparse

import praw
import time
import re
import requests
import bs4
import soundcloud
import pprint
import cPickle as pickle
import ast

from googleapiclient.discovery import build
#  }}} imports #

#  global vars {{{ # 
# Location of file where id's of already visited comments are maintained
comments_path = '/home/kevin/Documents/coding/trapbot/commented.txt'
api_file = 'google-api.ini'
cse_id = '016449672529328854635:e0dwkvd2jqa'
# Add more subreddits with '+'.
subreddits = 'test'

# Text to be posted along with comic description
header = '**SoundCloud Links:**\n\n'
footer = '___\n^^[Source&nbsp;Code](https://github.com/Kevin-Mok/TrapBot)&nbsp;|&nbsp;Bot&nbsp;created&nbsp;by&nbsp;u/ConfusedFence'

comment_query_limit = 5
search_query_limit = 10

# Open stored search results. (LOCAL)
#  with open('search_results-all.p', 'rb') as fp:
    #  all_search_results = pickle.load(fp)
all_search_results = []
search_results_file_name = 'search-results.txt'

# Link to search of song when it can't be found.
quality_threshold = 0.5
# Higher search results are usually better so later ones should be substantially
# more matched.
better_by_than = 0.25
soundcloud_search_url = 'https://soundcloud.com/search?q='
not_found_text = ' could not be found.'
# For %-encoding search URL.
url_safe_chars = ':/=?'
#  }}} global vars #

#  return_reddit_service() {{{ #
def return_reddit_service():
    print('Authenticating...\n')
    reddit_service = praw.Reddit('trapbot')
    print(reddit_service.user.me())
    print('Authenticated as {}\n'.format(reddit_service.user.me()))
    return reddit_service
#  }}} return_reddit_service() #

#  def return_cse_service(): {{{ # 
def return_cse_service():
    file = open(api_file)
    api_key = file.read().strip('\n')
    file.close()
    return build("customsearch", "v1", developerKey=api_key)
#  }}}  def return_cse_service(): # 

#  split_string_into_words() {{{ # 
# Split given string by spaces and punctuation.
def split_string_into_words(str_in):
    stripped_punctuation = '[]()\'\''
    return [word.strip(stripped_punctuation) for word in str_in.lower().split(' ') if len(word) > 1]
#  }}} split_string_into_words() # 

#  compare_search_with_title(search_words, title_words): {{{ # 
# Return percentage of words found vs all words in title.
def compare_search_with_title(search_words, title_words):
    search_words_found = []
    for search_word in search_words:
        if search_word in title_words:
            search_words_found.append(search_word)
    words_found = len(search_words_found)
    return float(words_found) / len(title_words)
    #  print("Found {0} ({1}) search words in {2} ({3:.2f}%)\n".format(words_found,
        #  search_words_found, title_words, percentage_found * 100))
#  }}} compare_search_with_title() # 

#  get_best_song_url(cse_service, query): {{{ #
# todo: remove last arg when actually using (LOCAL)
#  def get_best_song_url(cse_service, query, search_results_index):
def get_best_song_url(cse_service, query):
    # LIVE/LOCAL
    search_results = cse_service.cse().list(q=query, cx=cse_id, num=search_query_limit).execute()
    print(search_results)
    search_results_file = open(search_results_file_name, 'a+')
    search_results_file.write(str(search_results) + '\n')
    search_results_file.close()
    all_search_results.append(search_results)
    #  search_results = all_search_results[search_results_index]

    most_similar_percent = 0
    best_url = ''
    for result in search_results['items']:
        url = result['link']
        #  print(url, query)
        if 'search' not in url:
            page_title = result['title'].encode("utf-8")
            song_name = result['pagemap']['metatags'][0]['twitter:title']

            search_words = split_string_into_words(query)
            title_words = split_string_into_words(song_name)
            # remix is pretty big keyword to see if title is good match
            remix_in_both = ('remix' in search_words) == ('remix' in title_words)
            if len(title_words) > 1 and remix_in_both:
                similar_percent = compare_search_with_title(search_words, title_words)
                if similar_percent > (most_similar_percent + better_by_than):
                    most_similar_percent = similar_percent
                    best_url = url
                    #  print(most_similar_percent, best_url)

    return best_url if most_similar_percent > quality_threshold else None
#  }}} get_best_song_url(api_key, query): # 

#  def get_not_found_pair(song_name): {{{ # 
def get_not_found_pair(song_name):
    search_url = quote(soundcloud_search_url + song_name, url_safe_chars)
    return [song_name, search_url, not_found_text]
#  }}} def get_not_found_pair(song_name): # 

#  def get_song_url_pairs(song_names_matches): {{{ #
def get_song_url_pairs(song_names_matches):
    song_url_pairs = []
    cse_service = return_cse_service()

    # todo: remove when actually using (LOCAL)
    #  results_index = 0
    for match in song_names_matches:
        # combine song name and artist to form search query
        search_query = "{0} {1}".format(match[1], match[2])
        best_song_url = get_best_song_url(cse_service, search_query)
        #  best_song_url = get_best_song_url(cse_service, search_query, results_index)
        if best_song_url is not None:
            song_url_pairs.append([match[0], best_song_url])
        else:
            song_url_pairs.append(get_not_found_pair(match[0]))
        #  results_index += 1

    return song_url_pairs
#  }}} get_song_url_pairs() #

#  def filter_song_names(comment): {{{ # 
# Get song names matches from comment.
def filter_song_names(comment):
    # Regex used to determine if line is a song name. Matches are assumed to be
    # the artist and song name, order being irrelevant.
    song_name_regex = '((.+)\s?-\s?(.+))'
    max_word_length = 30
    max_song_length = 100

    song_names_matches = re.findall(song_name_regex, comment)
    filtered_song_names_matches = []
    for match in song_names_matches:
        proper_word_lengths = True
        for word in split_string_into_words(match[0]):
            if len(word) > max_word_length:
                proper_word_lengths = False
        if proper_word_lengths and len(match[0]) < max_song_length:
            filtered_song_names_matches.append(match)
    return filtered_song_names_matches
#  }}}  def filter_song_names(comment): # 

#  def scan_comments(): {{{ # 
def scan_comments():
    reddit_service = return_reddit_service()
    print("Getting {0} comments...\n".format(comment_query_limit))

    # retrieve comments from reddit_service
    for comment in reddit_service.subreddit(subreddits).comments(limit=comment_query_limit):
        #  song_names_matches = re.findall(song_name_regex, comment.body)
        #  song_names_matches = [match for match in song_names_matches if len(match[0]) <= max_artist_length and len(match[1]) <= max_artist_length]
        song_names_matches = filter_song_names(comment.body)
        read_comments_file = open(comments_path, 'r')

        if len(song_names_matches) > 0 and comment.id not in read_comments_file.read().splitlines():
            read_comments_file.close()
            print('Link is new. Posting links.\n')
            post = return_comment(get_song_url_pairs(song_names_matches))
            comment.reply(post)

            write_comments_file = open(comments_path, 'a+')
            write_comments_file.write(comment.id + '\n')
            write_comments_file.close()
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
    for item in song_url_pairs:
        #  print("[{0}]({1})".format(item[0], item[1]))
        if len(item) == 3:
            comment += "* ~~[{0}]({1})~~{2}".format(item[0], item[1], item[2])
        else:
            comment += "* [{0}]({1})".format(item[0], item[1])
        comment += "\n\n"
    return comment + footer
#  }}}  def return_comment(song_url_pairs): # 

#  main() {{{ # 
def main():
    #  scan reddit {{{ # 
    #  while True:
        #  scan_comments()
    #  print(re.findall(song_name_regex, comment))
    #  scan_comments()
    #  }}} scan reddit # 

    #  test comment {{{ # 
    comment = ' Definitely check\n\nSOPHIE - faceshopping\n\nGTA death to genres 3 comp\n\nJust a Gent - 404\n\nSumthin sumthin - spiral\n\nMinnesota - HiLow (charlesthefirst remix)\n\nZeke Beats Devestate EP\n\nJadu Dala (label) had some solid recent releases as well\n'

    song_names_matches = filter_song_names(comment)
    #  pprint.pprint(song_names_matches)
    #  pprint.pprint(len(song_names_matches))
    print(return_comment(get_song_url_pairs(song_names_matches)))

    #  song_names_matches = re.findall(song_name_regex, comment)
    #  song_names_matches = [match for match in song_names_matches if len(match[0]) <= max_artist_length and len(match[1]) <= max_artist_length]
    #  }}} for test comment # 

    # store results using cPickle (LOCAL)
    with open('search_results-all.p', 'wb') as fp:
        pickle.dump(all_search_results, fp, protocol=pickle.HIGHEST_PROTOCOL)

    #  read dict from file {{{ # 
    #  f = open('search-results.txt')
    #  results = []
    #  for line in f:
        #  results.append(ast.literal_eval(line))
    #  with open('search_results-all.p', 'wb') as fp:
        #  pickle.dump(results, fp, protocol=pickle.HIGHEST_PROTOCOL)
    #  }}} read dict from file # 

if __name__ == '__main__':
    main()
#  }}} main() #
