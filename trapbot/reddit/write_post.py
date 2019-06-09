import re
import unicodedata
from pprint import pformat

from trapbot.soundcloud_search.find_songs import split_string_into_words, \
        get_song_url_pairs
from trapbot.data.constants import reddit_service, song_name_regex, \
        max_word_length, found_comments_file_name

num_finds = 0
# where to post info about found matches
hevin_test_thread = reddit_service.submission(id='by2tsi')
prepend_url_str = 'https://www.reddit.com'

header = '**SoundCloud Links:**\n\n'
footer = '___\n^^[Usage](https://github.com/Kevin-Mok/TrapBot#usage)&nbsp;|&nbsp;Bot&nbsp;created&nbsp;by&nbsp;u/ConfusedFence'

def convert_str_to_ascii(str_in):
    return unicodedata.normalize('NFKD', str_in).encode('ascii', 'ignore')

# Get song names matches from comment and filter out songs in which the words or
# actual song name are too long (likely not a song).
def filter_song_names(comment):
    compiled_song_name_regex = re.compile(song_name_regex, re.MULTILINE)
    proper_song_name = True

    try:
        song_names_matches = compiled_song_name_regex.findall(comment)
    # need to decode HTML bytes
    except TypeError as e:
        song_names_matches = \
                compiled_song_name_regex.findall(comment.decode("utf-8"))
    filtered_song_names_matches = []
    for match in song_names_matches:
        # max word length
        for word in split_string_into_words(match[0]):
            if len(word) > max_word_length:
                proper_song_name = False

        if proper_song_name:
            filtered_song_names_matches.append(match)

    return filtered_song_names_matches

def add_comment_id_to_read(comment_id):
    #  read_comment_ids.add(comment_id)
    write_comments_file = open(found_comments_file_name, 'a+')
    write_comments_file.write(comment_id + '\n')
    write_comments_file.close()

def print_matched_comment(comment_body, url, song_names_matches):
    global num_finds
    global last_found_comment
    # format output str
    output = '**Find #{}**\n\n'.format(num_finds)
    output += '**URL:** {}\n\n'.format(url)
    output += '**Comment Body:**\n\n{}\n\n'.format(comment_body)
    output += '**Matches:** {}'.format(pformat(song_names_matches))

    # set last found comment and output to console
    last_found_comment = hevin_test_thread.reply(output)
    add_comment_id_to_read(last_found_comment.id)
    console_msg = '*** MATCH #{0} *** | URL: {1}'.format(num_finds, prepend_url_str + last_found_comment.permalink)
    divider = '-' * len(console_msg)
    print(divider)
    print(console_msg)
    print(divider)

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

def write_post_if_appropriate(comment):
    global num_finds
    comment_body = convert_str_to_ascii(comment.body)
    #  print(comment.subreddit, comment_body)
    song_names_matches = filter_song_names(comment_body)
    if len(song_names_matches) > 0:
        num_finds += 1
        url = prepend_url_str + comment.permalink
        formatted_matches = pformat(song_names_matches)
        # DEBUG
        print(formatted_matches)
        #  print_matched_comment(comment_body, url, formatted_matches)
        # print post
        post = return_comment(get_song_url_pairs(song_names_matches))
        #  last_found_comment.reply(post)
        #  write_post_to_file(url, post)
        #  comment.reply(post)

def write_post_from_submission_text(submission):
    song_names_matches = filter_song_names(convert_str_to_ascii(submission.selftext))
    post = return_comment(get_song_url_pairs(song_names_matches))
    hevin_test_thread.reply(post)
    #  write_post_to_file(submission.url, post)
