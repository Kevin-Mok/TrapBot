import unittest
from trapbot.reddit.write_post import filter_song_names

class TestWritePost(unittest.TestCase):
    def test_filter_song_names_basic(self):
        comment_body = "Blake Jarrell - Punta del Este (Beach Mix)"
        expected = [('Blake Jarrell - Punta del Este (Beach Mix)', 
            'Blake Jarrell', 'Punta del Este (Beach Mix)')]
        self.assertEqual(filter_song_names(comment_body), expected)

    def test_filter_song_names_garbage_around(self):
        comment_body = "garbagegarbagegarbagegarbagegarbage\nBlake Jarrell - Punta del Este (Beach Mix)\ngarbagegarbagegarbagegarbagegarbage"
        expected = [('Blake Jarrell - Punta del Este (Beach Mix)', 
            'Blake Jarrell', 'Punta del Este (Beach Mix)')]
        self.assertEqual(filter_song_names(comment_body), expected)

if __name__ == '__main__':
    unittest.main()
