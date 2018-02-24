import scan_reddit
from constants import default_comment_id, reddit_service

if __name__ == '__main__':
    global last_found_comment
    last_found_comment = reddit_service.comment(id=default_comment_id)

    #  for reply in reddit_service.inbox.comment_replies():
    #  print(type(reply))

    # normal 
    scan_reddit.loop_scanning()
    # comment
    # New EDM this week source
    #  write_post_if_appropriate(reddit_service.comment(id='dupa1ue'), last_found_comment)
    #  write_post_if_appropriate(reddit_service.comment(id='dupfald'), last_found_comment)

    #  submissions {{{ # 
    #  submission = reddit_service.submission(id='7z51na')
    #  #  write_post_from_submission_text(submission)
    #  scan_submission_comments(reddit_service, submission)
    #  }}} submissions #
