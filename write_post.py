import re
import unicodedata
from pprint import pformat, pprint

import find_songs
from constants import reddit_service, song_name_regex, max_word_length, \
found_comments_file_name, not_found_text, hevin_test_thread_id, header, footer

num_finds = 0
# thread of where to post info about found matches
hevin_test_thread = reddit_service.submission(id=hevin_test_thread_id)
queued_posts_file_name = 'queued_posts.txt'
prepend_url_str = 'https://www.reddit.com'
surround_comment_id = '!@#'

#  def convert_str_to_ascii(str_in): {{{ #
def convert_str_to_ascii(str_in):
    return unicodedata.normalize('NFKD', str_in).encode('ascii', 'ignore')


#  }}}  def convert_str_to_ascii(str_in): #

#  def filter_song_names(comment): {{{ # 
# Get song names matches from comment and filter out songs in which the words or
# actual song name are too long (likely not a song).
def filter_song_names(comment):
    compiled_song_name_regex = re.compile(song_name_regex, re.MULTILINE)
    proper_song_name = True

    song_names_matches = compiled_song_name_regex.findall(comment)
    filtered_song_names_matches = []
    for match in song_names_matches:
        # max word length
        for word in find_songs.split_string_into_words(match[0]):
            if len(word) > max_word_length:
                proper_song_name = False

        if proper_song_name:
            filtered_song_names_matches.append(match)

    return filtered_song_names_matches


#  }}}  def filter_song_names(comment): #

#  def add_comment_id_to_read(id): {{{ # 
def add_comment_id_to_read(comment_id):
    #  read_comment_ids.add(comment_id)
    write_comments_file = open(found_comments_file_name, 'a+')
    write_comments_file.write(comment_id + '\n')
    write_comments_file.close()


#  }}}  def add_comment_id_to_read(id): #

# Also prints out to console about match.
def set_last_found_comment(found_comment):
    global last_found_comment
    last_found_comment = found_comment
    add_comment_id_to_read(found_comment.id)
    console_msg = '*** MATCH #{0} *** | URL: {1}'.format(num_finds,\
            prepend_url_str + found_comment.permalink)
    divider = '-' * len(console_msg)
    print(divider)
    print(console_msg)
    print(divider)

def add_matches_to_output(output, song_url_pairs):
    output += '**Matches:**\n\n'
    for pair in song_url_pairs:
        if type(pair[1]) == 'str':
            match_output = not_found_text
        else:
            match_output = [pair[1].user['username'], pair[1].title]
        output += "{0}: {1}\n\n".format(pair[0], match_output)
    return output

#  def print_matched_comment(comment): {{{ # 
def print_matched_comment(comment_body, url, song_url_pairs, comment_id):
    global num_finds
    #  global last_found_comment
    # format output str
    output = '**Find #{}**\n\n'.format(num_finds)
    output += '**URL:** {}\n\n'.format(url)
    output += '**Comment Body:**\n\n{}\n\n'.format(comment_body)
    output = add_matches_to_output(output, song_url_pairs)
    output += '___\n' + return_comment(comment_id, song_url_pairs)
    print(output)
    #  post_extractor_regex = '{0}(\w{{3,10}}){0}(.+)'.format(surround_comment_id)
    # todo: fix this post/regex problem
    post_extractor_regex = '!@#(.+)!@#'.format(surround_comment_id)
    print(post_extractor_regex)
    compiled_post_extractor_regex = re.compile(post_extractor_regex, re.M)
    print(re.match(post_extractor_regex, output))

    #  set_last_found_comment(hevin_test_thread.reply(output))


#  }}}  def print_matched_comment(comment): #

#  def return_comment(song_url_pairs): {{{ #
# Expects lst of lsts containing song then URL in that specific order.
def return_comment(comment_id, song_url_pairs):
    comment = "{0}{1}{0}".format(surround_comment_id, comment_id)
    comment += header
    for item in song_url_pairs:
        if len(item) == 3:
            comment += '* ~~[{0}]({1})~~{2}'.format(item[0], item[1], item[2])
        else:
            comment += '* [{0}]({1})'.format(item[0], item[1].permalink_url)
        comment += '\n\n'
    return comment + footer


#  }}}  def return_comment(song_url_pairs): #

#  def write_post_if_appropriate(comment): {{{ # 
def write_post_if_appropriate(comment):
    global num_finds
    global last_found_comment

    comment_body = convert_str_to_ascii(comment.body)
    song_names_matches = filter_song_names(comment_body)
    if len(song_names_matches) > 0:
        num_finds += 1
        url = prepend_url_str + comment.permalink
        #  formatted_matches = pformat(song_names_matches)
        song_url_pairs = find_songs.get_song_url_pairs(song_names_matches)
        print_matched_comment(comment_body, url, song_url_pairs, comment.id)

        #  post = return_comment(comment.id, song_url_pairs)
        #  last_found_comment.reply(post)


#  }}}  def write_post_if_appropriate(comment): #

#  def write_post_from_submission_text(submission): {{{ # 
def write_post_from_submission_text(submission):
    song_names_matches = filter_song_names(convert_str_to_ascii(submission.selftext))
    post = return_comment(find_songs.get_song_url_pairs(song_names_matches))
    hevin_test_thread.reply(post)
    #  write_post_to_file(submission.url, post)
#  }}} def write_post_from_submission_text(submission): #
