# Vars shared between files. Created this class because was having trouble with
# cyclical imports.

import praw

reddit_service = praw.Reddit('trapbot')
# ID of thread of where to post info about found matches
hevin_test_thread_id = '7zvr6h'
# id of comment to respond to when posting sample post
default_comment_id = 'duquvfg'
# name of file storing all found comments
found_comments_file_name = 'found_comments.txt'
not_found_text = ' could not be found.'

#  header/footer of response {{{ # 
header = '**SoundCloud Links:**\n\n'
footer = '___\n^^[Usage](https://github.com/Kevin-Mok/TrapBot#usage)&nbsp;|&nbsp;Bot&nbsp;created&nbsp;by&nbsp;u/ConfusedFence'
#  }}} header/footer of response # 

#  for matching song name {{{ # 
# section should be between 3 and 50 chars
section_regex = '(.{3,50})'
song_name_regex = '(^{0}\s-\s{0}$)'.format(section_regex)

# max length of word in song name
max_word_length = 30

#  }}} for matching song name # 
