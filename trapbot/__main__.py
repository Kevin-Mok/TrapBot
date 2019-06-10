import trapbot.reddit.scan_reddit
from trapbot.reddit.write_post import write_post_if_appropriate
from trapbot.data.constants import default_comment_id, reddit_service

# DEBUG # 
#  from trapbot.reddit.write_post import *
from trapbot.soundcloud_search.find_songs import __return_soundcloud_service

if __name__ == '__main__':
    #  global last_found_comment
    #  last_found_comment = reddit_service.comment(id=default_comment_id)

    #  for reply in reddit_service.inbox.comment_replies():
    #  print(type(reply))

    # loop or single comment 
    #  scan_reddit.loop_scanning()
    #  write_post_if_appropriate(reddit_service.comment(id='eqc1yl6'))

    #  submission = reddit_service.submission(id='7z51na')
    #  #  write_post_from_submission_text(submission)
    #  scan_submission_comments(reddit_service, submission)

    #  TODO: write up issue regarding not finding top tracks # 
    found_tracks = __return_soundcloud_service().get('/tracks', 
            q='Blake Jarrell - Punta del Este (Beach Mix)')
    for track in found_tracks:
        print(track.title)
