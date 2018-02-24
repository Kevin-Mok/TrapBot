# -*- coding: utf-8 -*-
import time

import write_post
from constants import reddit_service, found_comments_file_name, \
        hevin_test_thread_id, header

# for debugging purposes
from pprint import pprint

subreddits_file_name = 'subreddits.txt'
#  inbox_reply_limit = 20
inbox_reply_limit = 5
confirmation_str = 'Y'

#  freq/limits {{{ # 
#  comment_query_limit = 200
comment_query_limit = 20
#  check_freq = 30
check_freq = 120


#  }}} freq/limits #

#  def make_set_from_file(file_name): {{{ #

def make_set_from_file(file_name):
    arb_file = open(file_name, 'r')
    lst = {line for line in arb_file.read().splitlines()}
    arb_file.close()
    return lst


#  }}} def make_set_from_file(file_name): #

#  def scan_submission_comments(reddit_service, submission): {{{ # 
def scan_submission_comments(reddit_service, submission):
    new_comments = [comment for comment in submission.comments \
                    if comment.id not in make_set_from_file(found_comments_file_name)]
    #  pprint.pprint(new_comments)
    for comment in new_comments:
        write_post.add_comment_id_to_read(comment.id)
        write_post.write_post_if_appropriate(comment)


#  }}}  def scan_submission_comments(reddit_service, submission): #

#  def scan_comments(reddit_service): {{{ # 
def scan_comments(reddit_service, subreddits_str):
    fetched_comments = reddit_service.subreddit(subreddits_str).comments(limit=comment_query_limit)
    new_comments = [comment for comment in fetched_comments \
                    if comment.id not in make_set_from_file(found_comments_file_name)]

    #  retrieve comments from reddit_service
    for comment in new_comments:
        write_post.add_comment_id_to_read(comment.id)
        write_post.write_post_if_appropriate(comment)


#  }}} def scan_comments(reddit_service): #

def respond_to_orig_post(parent_comment_id):
    for comment in reddit_service.submission(id=hevin_test_thread_id).comments.list():
        if comment.id == parent_comment_id:
                if header in child_comment:
                    child_comment_lines = child_comment.body.split('\n')
                    


def check_for_replies():
    fetched_replies = reddit_service.inbox.comment_replies(limit=inbox_reply_limit).__iter__()
    new_replies = [reply for reply in fetched_replies \
                    if reply.id not in make_set_from_file(found_comments_file_name)]
    for reply in new_replies:
        #  print(reply.submission.id, reply.body)
        if reply.submission.id == hevin_test_thread_id and \
                reply.body == confirmation_str:
                    respond_to_orig_post(reply.parent().id)



#  def loop_scanning(): {{{ # 
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

#  }}} def loop_scanning(): #

if __name__ == '__main__':
    # normal 
    #  loop_scanning()

    #  check_for_replies()

    # comment
    write_post.write_post_if_appropriate(reddit_service.comment(id='dur3z7x'))

    #  submissions {{{ # 
    #  submission = reddit_service.submission(id='7z51na')
    #  #  write_post.write_post_from_submission_text(submission)
    #  scan_submission_comments(reddit_service, submission)
    #  }}} submissions #

    # New EDM this week source
    #  write_post.write_post_if_appropriate(reddit_service.comment(id='dupa1ue'))
