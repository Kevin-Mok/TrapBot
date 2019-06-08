# -*- coding: utf-8 -*-
import time

import write_post
from constants import reddit_service, found_comments_file_name

subreddits_file_name = 'subreddits.txt'

#  comment_query_limit = 2000
comment_query_limit = 20
#  comment_query_limit = 100
#  check_freq = 30
check_freq = 120

def make_set_from_file(file_name):
    arb_file = open(file_name, 'r')
    lst = {line for line in arb_file.read().splitlines()}
    arb_file.close()
    return lst

def scan_submission_comments(reddit_service, submission):
    new_comments = [comment for comment in submission.comments \
                    if comment.id not in make_set_from_file(found_comments_file_name)]
    #  pprint.pprint(new_comments)
    for comment in new_comments:
        write_post.add_comment_id_to_read(comment.id)
        write_post.write_post_if_appropriate(comment)

def filter_new_comment(comment):
    """Return whether comment hasn't been scanned yet and it's not from
    AutoModerator.

    :comment: PRAW comment object
    :returns: bool

    """
    return (comment.id not in make_set_from_file(found_comments_file_name)) and \
            (comment.author.name != "AutoModerator")

def scan_comments(reddit_service, subreddits_str):
    fetched_comments = reddit_service.subreddit(subreddits_str).comments(limit=comment_query_limit)
    new_comments = [comment for comment in fetched_comments if
            filter_new_comment(comment)]

    #  retrieve comments from reddit_service
    for comment in new_comments:
        write_post.add_comment_id_to_read(comment.id)
        write_post.write_post_if_appropriate(comment)

def loop_scanning():
    subreddits_str = '+'.join(make_set_from_file(subreddits_file_name))

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
