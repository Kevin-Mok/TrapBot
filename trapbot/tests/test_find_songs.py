import unittest
from trapbot.reddit.write_post import filter_song_names
from trapbot.soundcloud_search.find_songs import get_song_url_pairs

class TestWritePost(unittest.TestCase):
    def test_get_song_url_pairs(self):
        song_names_matches = [('Blake Jarrell - Punta del Este (Beach Mix)', 
            'Blake Jarrell', 'Punta del Este (Beach Mix)')]
        expected = [["Blake Jarrell - Punta del Este (Beach Mix)",
            "https://soundcloud.com/blake-jarrell-official/blake-jarrell-punta-del-este"]]
        self.assertEqual(get_song_url_pairs(song_names_matches), expected)

if __name__ == '__main__':
    unittest.main()
