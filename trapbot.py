#  imports {{{ # 
# -*- coding: utf-8 -*-
import pprint
import re
import time
from urllib import quote

import praw
import soundcloud

#  }}} imports #

#  global vars {{{ # 
#  file names {{{ # 
soundcloud_api_file_name = 'soundcloud-api.ini'
found_comments_file_name = 'found_comments.txt'
read_comments_file = open(found_comments_file_name, 'r')
read_comment_ids = [comment_id for comment_id in read_comments_file.read().splitlines()]
read_comments_file.close()
#  found_matches_file = 'found_matches.txt'
posts_file_name = 'posts.txt'
#  }}} file names # 

# Add more subreddits with '+'.
subreddits = 'EDM+trap+hevin'

#  output text {{{ # 
# Text around comment body
header = '**SoundCloud Links:**\n\n'
footer = '___\n^^[Source&nbsp;code](https://github.com/Kevin-Mok/TrapBot)&nbsp;|&nbsp;Bot&nbsp;created&nbsp;by&nbsp;u/ConfusedFence'
#  }}} output text # 

#  timing/limit vars {{{ # 
comment_query_limit = 10
search_query_limit = 10
#  check_freq = 60
check_freq = 120
num_finds = 0
#  }}} timing/limit vars # 

#  vars used to find best song {{{ # 
quality_threshold = 0.5
real_artist_threshold = 0.50
real_artist_weight = 1
remix_same_weight = 1
remix_synonyms = ['remix', 'flip', 'edit']
# Higher search results are usually better so later ones should be substantially
# more matched.
better_by_than = 0.5

prepend_url_str = 'https://www.reddit.com'

# Link to search of song when it can't be found.
soundcloud_search_url = 'https://soundcloud.com/search?q='
not_found_text = ' could not be found.'


#  }}} vars used to find best song #
#  }}} global vars #

#  return_reddit_service() {{{ #
def return_reddit_service():
    #  print('Authenticated as {}\n'.format(reddit_service.user.me()))
    return praw.Reddit('trapbot')


#  }}} return_reddit_service() #

#  def return_soundcloud_service(): {{{ # 
def return_soundcloud_service():
    soundcloud_api_file = open(soundcloud_api_file_name)
    soundcloud_client_id = soundcloud_api_file.readline().strip('\n')
    return soundcloud.Client(client_id=soundcloud_client_id)


#  }}} def return_soundcloud_service(): #

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
    return float(words_found) / len(search_words)


#  }}} compare_search_with_title() #

#  def check_if_real_artist(artist_words, search_words): {{{ # 
def check_if_real_artist(artist_words, search_words):
    real_artist = compare_search_with_title(artist_words, search_words) > real_artist_threshold
    return real_artist_weight if real_artist else 0


#  }}}  def check_if_real_artist(artist_words, search_words): #

#  def check_if_remix_same(title_words, search_words): {{{ # 
def check_if_remix_synonym_in_list(lst):
    return True if len(set(lst) & set(remix_synonyms)) else False


def check_if_remix_same(title_words, search_words):
    remix_same = check_if_remix_synonym_in_list(title_words) == \
                 check_if_remix_synonym_in_list(search_words)
    return remix_same_weight if remix_same else 0


#  }}}  def check_if_remix_same(title_words, search_words): #

#  def get_best_song_url_from_sc(soundcloud_service, query): {{{ # 
def get_best_song_url_from_sc(soundcloud_service, query):
    found_tracks = soundcloud_service.get('/tracks', q=query, limit=search_query_limit)

    most_similar_percent = 0
    best_url = ''
    if len(found_tracks) < 1:
        return None
    for track in found_tracks:
        search_words = split_string_into_words(query)
        title_words = split_string_into_words(track.title)
        artist_words = split_string_into_words(track.user['username'])

        word_similarity_weight = compare_search_with_title(search_words, title_words)
        artist_weight = check_if_real_artist(artist_words, search_words)
        remix_weight = check_if_remix_same(title_words, search_words)

        similar_percent = word_similarity_weight + artist_weight + remix_weight
        # DEBUG
        #  print([word_similarity_weight, artist_weight, remix_weight], similar_percent, track.title, track.user['username'])
        if similar_percent > (most_similar_percent + better_by_than):
            most_similar_percent = similar_percent
            best_url = track.permalink_url

    return best_url if most_similar_percent > quality_threshold else None


#  }}}  def get_best_song_url_from_sc(soundcloud_service, query): #

#  def get_song_url_pairs(song_names_matches): {{{ #
def get_song_url_pairs(song_names_matches):
    song_url_pairs = []
    soundcloud_service = return_soundcloud_service()

    for match in song_names_matches:
        # combine song name and artist to form search query
        search_query = '{0} {1}'.format(match[1], match[2])
        best_song_url = get_best_song_url_from_sc(soundcloud_service, search_query)
        if best_song_url is not None:
            song_url_pairs.append([match[0], best_song_url])
        else:
            song_url_pairs.append([match[0], soundcloud_search_url + quote(match[0]), not_found_text])

    return song_url_pairs


#  }}} get_song_url_pairs() #

#  def filter_song_names(comment): {{{ # 
# Get song names matches from comment and filter out songs in which the words or
# actual song name are too long (likely not a song).
def filter_song_names(comment):
    # section should be between 3 and 50 chars
    section_regex = '(.{3,50})'
    song_name_regex = '(^{0}\s?-\s?{0}$)'.format(section_regex)
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
    read_comment_ids.append(comment_id)
    write_comments_file = open(found_comments_file_name, 'a+')
    write_comments_file.write(comment_id + '\n')
    write_comments_file.close()


#  }}}  def add_comment_id_to_read(id): #

#  def print_matched_comment(comment): {{{ # 
def print_matched_comment(comment, url, song_names_matches):
    global num_finds
    #  print(found_comment_output[0])
    print('-' * 80)
    print('Find #{}\n'.format(num_finds))
    print('URL: {}'.format(url))
    print('Comment Body:\n{}'.format(comment.body))
    print('Matches: {}'.format(song_names_matches))
    print('-' * 80)
    #  print(found_comment_output[1])


#  }}}  def print_matched_comment(comment): #

#  def write_post_to_file(url, post): {{{ # 
def write_post_to_file(url, post):
    global num_finds
    formatted_post = 'Find #{}\n\n'.format(num_finds)
    formatted_post += 'URL: {}\n\n'.format(url)
    formatted_post += 'Post:\n\n {}\n\n'.format(post)
    formatted_post += ('=' * 80) + '\n\n'
    #  print(formatted_post)

    # write post to file
    write_posts_file = open(posts_file_name, 'a+')
    write_posts_file.write(formatted_post)
    write_posts_file.close()


#  }}} def write_post_to_file(url, post): #

#  def write_post_if_appropriate(comment): {{{ # 
def write_post_if_appropriate(comment):
    global num_finds
    song_names_matches = filter_song_names(comment.body)
    if len(song_names_matches) > 0:
        num_finds += 1
        url = prepend_url_str + comment.permalink
        formatted_matches = pprint.pformat(song_names_matches)
        print_matched_comment(comment, url, formatted_matches)
        # print post
        post = return_comment(get_song_url_pairs(song_names_matches))
        write_post_to_file(url, post)
        #  comment.reply(post)


#  }}}  def write_post_if_appropriate(comment): #

#  def scan_comments(reddit_service): {{{ # 
def scan_comments(reddit_service):
    fetched_comments = reddit_service.subreddit(subreddits).comments(limit=comment_query_limit)
    new_comments = [comment for comment in fetched_comments if comment.id not in read_comment_ids]

    #  retrieve comments from reddit_service
    for comment in new_comments:
        add_comment_id_to_read(comment.id)
        write_post_if_appropriate(comment)


#  }}} def scan_comments(reddit_service): #

#  def return_comment(song_url_pairs): {{{ #
# Expects list of lists containing song then URL in that specific order.
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
    num_scans = 0
    while True:
        total_uptime = float(num_scans * check_freq) / 60
        wait_msg = 'Scan #{0} ({1}s) | Total Uptime: {2:.0f}m'.format(num_scans, \
                                                                      check_freq, total_uptime)
        print(wait_msg)

        scan_comments(reddit_service)
        num_scans += 1
        time.sleep(check_freq)


#  }}} def loop_scanning(): #

if __name__ == '__main__':
    loop_scanning()

    # work with single comment
    #  write_post_if_appropriate(reddit_service.comment(id='dum44tn'))
