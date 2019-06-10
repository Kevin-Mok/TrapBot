from urllib.parse import quote

import soundcloud
from importlib.resources import open_text
#  from . import soundcloud_search

soundcloud_api_file_name = 'soundcloud-api.ini'
search_query_limit = 10

# Link to search of song when it can't be found.
soundcloud_search_url = 'https://soundcloud.com/search?q='
not_found_text = ' could not be found.'

#  weights used to find right song
quality_threshold = 0.5
real_artist_threshold = 0.50
real_artist_weight = 1
remix_same_weight = 1
# Higher search results are usually better so later ones should be substantially
# more matched.
better_by_than = 0.5

def __return_soundcloud_service():
    #  soundcloud_api_file = open(soundcloud_api_file_name)
    soundcloud_api_file = open_text('trapbot.soundcloud_search', soundcloud_api_file_name)
    soundcloud_client_id = soundcloud_api_file.readline().strip('\n')
    soundcloud_api_file.close()
    return soundcloud.Client(client_id=soundcloud_client_id)

def split_string_into_words(str_in):
    """Split given string by spaces and punctuation.

    :returns: TODO

    """
    stripped_punctuation = '[]()\''
    return [word.strip(stripped_punctuation) for word in str_in.lower().split(' ') if len(word) > 1]

def __compare_search_with_title(search_words, title_words):
    """Return percentage of words found vs. all words in title.

    :search_words: TODO
    :title_words: TODO
    :returns: TODO

    """
    if len(search_words) < 1:
        return 0
    search_words_found = []
    for search_word in search_words:
        if search_word in title_words:
            search_words_found.append(search_word)
    words_found = len(search_words_found)
    return float(words_found) / len(search_words)

def __check_if_real_artist(artist_words, search_words):
    real_artist = __compare_search_with_title(artist_words, search_words) > real_artist_threshold
    return real_artist_weight if real_artist else 0

def __check_if_remix_same(title_words, search_words):
    def check_if_remix_synonym_in_lst(lst):
        remix_synonyms = ['remix', 'flip', 'edit', 'cover', 'remixes',
                'acoustic', 'mix']
        return True if len(set(lst) & set(remix_synonyms)) else False

    remix_same = check_if_remix_synonym_in_lst(title_words) == \
                 check_if_remix_synonym_in_lst(search_words)
    return remix_same_weight if remix_same else 0

def __get_best_song_url_from_sc(soundcloud_service, query):
    found_tracks = soundcloud_service.get('/tracks', q=query, limit=search_query_limit)

    most_similar_percent = 0
    best_url = ''
    if len(found_tracks) < 1:
        return None
    for track in found_tracks:
        search_words = split_string_into_words(query)
        title_words = split_string_into_words(track.title)
        artist_words = split_string_into_words(track.user['username'])

        word_similarity_weight = __compare_search_with_title(search_words, title_words)
        artist_weight = __check_if_real_artist(artist_words, search_words)
        remix_weight = __check_if_remix_same(title_words, search_words)

        similar_percent = word_similarity_weight + artist_weight + remix_weight
        # DEBUG
        print([word_similarity_weight, artist_weight, remix_weight],
                similar_percent, track.title, track.user['username'])
        if similar_percent > (most_similar_percent + better_by_than):
            most_similar_percent = similar_percent
            best_url = track.permalink_url
    print()

    return best_url if most_similar_percent > quality_threshold else None

def get_song_url_pairs(song_names_matches):
    """Return list of lists consisting of the song name and matching
    SoundCloud URL.

    :song_names_matches: list of regex matches from filter_song_names
    """
    song_url_pairs = []
    soundcloud_service = __return_soundcloud_service()

    for match in song_names_matches:
        # combine song name and artist to form search query
        search_query = '{0} {1}'.format(match[1], match[2])
        best_song_url = __get_best_song_url_from_sc(soundcloud_service, search_query)
        if best_song_url is not None:
            song_url_pairs.append([match[0], best_song_url])
        # comment out to not show not found
        else:
            song_url_pairs.append([match[0],
                soundcloud_search_url + quote(match[0]), not_found_text])

    return song_url_pairs
