#  imports {{{ # 
# -*- coding: utf-8 -*-
import pprint
import re
import time
from urllib import quote

import praw
import unicodedata

from create_post import *
#  }}} imports #

#  global vars {{{ # 
#  file names {{{ # 
found_comments_file_name = 'found_comments.txt'
subreddits_file_name = 'subreddits.txt'

read_comments_file = open(found_comments_file_name, 'r')
read_comment_ids = {comment_id for comment_id in read_comments_file.read().splitlines()}
read_comments_file.close()
#  read_comment_ids = make_lst_from_file(found_comments_file_name)
#  }}} file names # 

#  output text {{{ # 
# Text around comment body
header = '**SoundCloud Links:**\n\n'
footer = '___\n^^[Source&nbsp;code](https://github.com/Kevin-Mok/TrapBot)&nbsp;|&nbsp;Bot&nbsp;created&nbsp;by&nbsp;u/ConfusedFence'
footer = '___\n^^[Usage](https://github.com/Kevin-Mok/TrapBot#usage)&nbsp;|&nbsp;Bot&nbsp;created&nbsp;by&nbsp;u/ConfusedFence'
#  }}} output text # 

#  timing/limit vars {{{ # 
#  comment_query_limit = 2000
comment_query_limit = 20
#  check_freq = 30
check_freq = 120
num_finds = 0
#  }}} timing/limit vars # 

prepend_url_str = 'https://www.reddit.com'

hevin_test_thread_id = '7ysnhg'
default_comment_id = 'dupa1ue'
#  }}} global vars #

#  def make_lst_from_file(file_name): {{{ # 
def make_lst_from_file(file_name):
    arb_file = open(file_name, 'r')
    lst = [line for line in arb_file.read().splitlines()]
    arb_file.close()
    return lst
#  }}} def make_lst_from_file(file_name): # 

#  return_reddit_service() {{{ #
def return_reddit_service():
    #  print('Authenticated as {}\n'.format(reddit_service.user.me()))
    return praw.Reddit('trapbot')


#  }}} return_reddit_service() #

#  def filter_song_names(comment): {{{ # 
# Get song names matches from comment and filter out songs in which the words or
# actual song name are too long (likely not a song).
def filter_song_names(comment):
    # section should be between 3 and 50 chars
    section_regex = '(.{3,50})'
    song_name_regex = '(^{0}\s-\s{0}$)'.format(section_regex)
    compiled_song_name_regex = re.compile(song_name_regex, re.MULTILINE)
    max_word_length = 30
    proper_song_name = True

    song_names_matches = compiled_song_name_regex.findall(comment)
    filtered_song_names_matches = []
    for match in song_names_matches:
        # max word length
        for word in split_string_into_words(match[0]):
            if len(word) > max_word_length:
                proper_song_name = False

        if proper_song_name:
            filtered_song_names_matches.append(match)

    return filtered_song_names_matches


#  }}}  def filter_song_names(comment): #

#  def add_comment_id_to_read(id): {{{ # 
def add_comment_id_to_read(comment_id):
    read_comment_ids.add(comment_id)
    write_comments_file = open(found_comments_file_name, 'a+')
    write_comments_file.write(comment_id + '\n')
    write_comments_file.close()


#  }}}  def add_comment_id_to_read(id): #

#  def print_matched_comment(comment): {{{ # 
def print_matched_comment(comment_body, url, song_names_matches):
    global num_finds
    global last_found_comment
    # format output str
    output = '**Find #{}**\n\n'.format(num_finds)
    output += '**URL:** {}\n\n'.format(url)
    output += '**Comment Body:**\n\n{}\n\n'.format(comment_body)
    output += '**Matches:** {}'.format(pprint.pformat(song_names_matches))

    # set last found comment and output to console
    last_found_comment = hevin_test_thread.reply(output)
    add_comment_id_to_read(last_found_comment.id)
    console_msg = '*** MATCH #{0} *** | URL: {1}'.format(num_finds, prepend_url_str + last_found_comment.permalink)
    divider = '-' * len(console_msg)
    print(divider)
    print(console_msg)
    print(divider)


#  }}}  def print_matched_comment(comment): #

#  def convert_str_to_ascii(str_in): {{{ # 
def convert_str_to_ascii(str_in):
    return unicodedata.normalize('NFKD', str_in).encode('ascii','ignore')
#  }}}  def convert_str_to_ascii(str_in): # 

#  def write_post_if_appropriate(comment): {{{ # 
def write_post_if_appropriate(comment):
    global num_finds
    comment_body = convert_str_to_ascii(comment.body)
    song_names_matches = filter_song_names(comment_body)
    if len(song_names_matches) > 0:
        num_finds += 1
        url = prepend_url_str + comment.permalink
        formatted_matches = pprint.pformat(song_names_matches)
        print_matched_comment(comment_body, url, formatted_matches)
        # print post
        post = return_comment(get_song_url_pairs(song_names_matches))
        last_found_comment.reply(post)
        #  write_post_to_file(url, post)
        #  comment.reply(post)


#  }}}  def write_post_if_appropriate(comment): #

#  def write_post_from_submission_text(submission): {{{ # 
def write_post_from_submission_text(submission):
    song_names_matches = filter_song_names(convert_str_to_ascii(submission.selftext))
    post = return_comment(get_song_url_pairs(song_names_matches))
    hevin_test_thread.reply(post)
    #  write_post_to_file(submission.url, post)
#  }}} def write_post_from_submission_text(submission): # 

#  def scan_submission_comments(reddit_service, submission): {{{ # 
def scan_submission_comments(reddit_service, submission):
    new_comments = [comment for comment in submission.comments \
            if comment.id not in read_comment_ids]
    #  pprint.pprint(new_comments)
    for comment in new_comments:
        add_comment_id_to_read(comment.id)
        write_post_if_appropriate(comment)
#  }}}  def scan_submission_comments(reddit_service, submission): # 

#  def scan_comments(reddit_service): {{{ # 
def scan_comments(reddit_service, subreddits_str):
    fetched_comments = reddit_service.subreddit(subreddits_str).comments(limit=comment_query_limit)
    new_comments = [comment for comment in fetched_comments if comment.id not in read_comment_ids]

    #  retrieve comments from reddit_service
    for comment in new_comments:
        add_comment_id_to_read(comment.id)
        write_post_if_appropriate(comment)


#  }}} def scan_comments(reddit_service): #

#  def return_comment(song_url_pairs): {{{ #
# Expects lst of lsts containing song then URL in that specific order.
def return_comment(song_url_pairs):
    comment = header
    for item in song_url_pairs:
        if len(item) == 3:
            comment += '* ~~[{0}]({1})~~{2}'.format(item[0], item[1], item[2])
        else:
            comment += '* [{0}]({1})'.format(item[0], item[1])
        comment += '\n\n'
    return comment + footer


#  }}}  def return_comment(song_url_pairs): #

#  def loop_scanning(): {{{ # 
def loop_scanning():
    reddit_service = return_reddit_service()
    subreddits_str = '+'.join(make_lst_from_file(subreddits_file_name))

    num_scans = 0
    while True:
        total_uptime = float(num_scans * check_freq) / 60
        wait_msg = 'Scan #{0} ({1}s) | Total Uptime: {2:.0f}m'.format(num_scans, \
                                                                      check_freq, total_uptime)
        print(wait_msg)

        scan_comments(reddit_service, subreddits_str)
        num_scans += 1
        time.sleep(check_freq)
    #  scan_comments(reddit_service, subreddits_str)

#  }}} def loop_scanning(): #

if __name__ == '__main__':
    global hevin_test_thread
    global last_found_comment
    reddit_service = return_reddit_service()
    hevin_test_thread = reddit_service.submission(id=hevin_test_thread_id)
    last_found_comment = reddit_service.comment(id=default_comment_id)

    # normal 
    loop_scanning()
    # comment
    # New EDM this week source
    #  write_post_if_appropriate(reddit_service.comment(id='dupa1ue'))
    #  write_post_if_appropriate(reddit_service.comment(id='dupfald'))

    #  submissions {{{ # 
    #  submission = reddit_service.submission(id='7z51na')
    #  #  write_post_from_submission_text(submission)
    #  scan_submission_comments(reddit_service, submission)
    #  }}} submissions # 
