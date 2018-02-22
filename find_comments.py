#  imports {{{ # 
# -*- coding: utf-8 -*-

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
import sys
#  }}} imports #

#  global vars {{{ # 
# Location of file where id's of already visited comments are maintained
found_comments_path = '/home/kevin/Documents/coding/trapbot/found_comments.txt'
found_matches_file = 'found_matches.txt'
# Add more subreddits with '+'.
subreddits = 'EDM+trap+hevin'

# Text to be posted along with comic description
header = '**SoundCloud Links:**\n\n'
footer = '___\n^^[Source&nbsp;code](https://github.com/Kevin-Mok/TrapBot)&nbsp;|&nbsp;Bot&nbsp;created&nbsp;by&nbsp;u/ConfusedFence'

comment_query_limit = 10
check_freq = 120
#  check_freq = 10
time_btwn_wait_msgs = check_freq / 4

prepend_url_str = 'https://www.reddit.com'

read_comments_file = open(found_comments_path, 'r')
read_comment_ids = [id for id in read_comments_file.read().splitlines()]
read_comments_file.close()
#  }}} global vars #

#  return_reddit_service() {{{ #
def return_reddit_service():
    reddit_service = praw.Reddit('trapbot')
    print('Logged in as {}\n'.format(reddit_service.user.me()))
    return reddit_service

#  }}} return_reddit_service() #

#  split_string_into_words() {{{ # 
# Split given string by spaces and punctuation.
def split_string_into_words(str_in):
    stripped_punctuation = '[]()\'\''
    return [word.strip(stripped_punctuation) for word in str_in.lower().split(' ') if len(word) > 1]

#  }}} split_string_into_words() #

#  def filter_song_names(comment): {{{ # 
# Get song names matches from comment and filter out songs in which the words or
# actual song name are too long (likely not a song).
def filter_song_names(comment):
    # Regex used to determine if line is a song name. Matches are assumed to be
    # the artist and song name, order being irrelevant.

    # section should be between 3 and 50 chars
    section_regex = '(.{3,50})'
    song_name_regex = '(^{0}\s?-\s?{0}$)'.format(section_regex)
    compiled_song_name_regex = re.compile(song_name_regex, re.MULTILINE)
    #  min_section_length = 3
    #  max_song_length = 100
    max_word_length = 30
    proper_song_name = True

    song_names_matches = compiled_song_name_regex.findall(comment)
    filtered_song_names_matches = []
    for match in song_names_matches:
        # max word length
        for word in split_string_into_words(match[0]):
            if len(word) > max_word_length:
                proper_song_name = False

        # min section length/max song length
        #  if len(match[1]) <= min_section_length or \
                #  len(match[2]) <= min_section_length or \
                #  len(match[0]) < max_song_length:
            #  proper_song_name = False

        # if passed all conditions, then add
        if proper_song_name:
            filtered_song_names_matches.append(match)

    return filtered_song_names_matches

#  }}}  def filter_song_names(comment): #

#  def reset_found_streak(streak): {{{ # 
#  def reset_found_streak(streak):
    #  print("Already searched last {0} comments.".format(streak))
    #  return 0
#  }}}  def reset_found_streak(streak): # 

#  def scan_comments(): {{{ # 
def scan_comments(reddit_service):
    #  print("Getting {0} comments...".format(comment_query_limit))

    fetched_comments = reddit_service.subreddit(subreddits).comments(limit=comment_query_limit)
    new_comments = [comment for comment in fetched_comments if comment.id not in read_comment_ids]

    #  print("Found {} new comment(s).".format(len(new_comments)))
    #  comments_read = 0
    #  prev_found_streak = 0
    #  retrieve comments from reddit_service
    for comment in new_comments:
        #  comments_read += 1
        #  if comment.id not in :
            #  if prev_found_streak > 0:
                #  prev_found_streak = reset_found_streak(prev_found_streak)
        url = prepend_url_str + comment.permalink
        #  print(comments_read, comment.id)
        #  print(comment.id, url)
        #  print(comment.body + '\n')
        #  write_comments_file = open(found_comments_path, 'a+')
        read_comment_ids.append(comment.id)
        write_comments_file = open(found_comments_path, 'a+')
        write_comments_file.write(comment.id + '\n')
        write_comments_file.close()

        song_names_matches = filter_song_names(comment.body)
        if len(song_names_matches) > 0:
            print('\n*** THIS COMMENT CONTAINS SONG NAMES. FINDING... ***')
            #  print('Comment is new and contains song names. Finding...')
            formatted_matches = pprint.pformat(song_names_matches)
            #  pprint.pprint(song_names_matches)
            print(formatted_matches)
            print('*** END OF MATCHES ***\n')
            match_str = "{0}\n{1}\n\n".format(url, formatted_matches)
            #  write_matches_file = open(found_matches_file, 'a+')
            write_matches_file = open(found_matches_file, 'a+')
            write_matches_file.write(match_str)
            write_matches_file.close()
            #  post = return_comment(get_song_url_pairs(song_names_matches))
            #  comment.reply(post)

        #  else:
            #  prev_found_streak += 1

    #  if prev_found_streak > 0:
        #  prev_found_streak = reset_found_streak(prev_found_streak)
    #  print('Waiting {} seconds before next scan...'.format(check_freq))
    #  for i in range(check_freq, 0, time_btwn_wait_msgs * -1):
        #  print("{}...".format(i))
        #  time.sleep(time_btwn_wait_msgs)
    #  print('')
    print('Waiting {} seconds before next scan...'.format(check_freq))
    time.sleep(check_freq)

#  }}} def scan_comments(): #

#  main() {{{ # 
def main():
    #  open(found_comments_path, 'w+').close()
    #  open(found_matches_file, 'w+').close()
    reddit_service = return_reddit_service()
    
    while True:
        scan_comments(reddit_service)
    #  scan_comments(reddit_service)

if __name__ == '__main__':
    main()
#  }}} main() #
