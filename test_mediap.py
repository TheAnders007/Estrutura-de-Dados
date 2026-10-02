import unittest
from datetime import datetime
from mediap.doubly_linked_list import DoublyLinkedList
from mediap.models import Track

class TestePlaylist(unittest.TestCase):
    def test_doubly_linked_list(self):
        playlist = DoublyLinkedList()
        
        track1 = Track(1, "My Way", "Olivia Rodrigo", 221, 5, datetime.now().isoformat())
        track2 = Track(2, "Praga", "Tim Bernardes", 201, 4, datetime.now().isoformat())
        
        playlist.add(track1)
        playlist.add(track2)
        
        self.assertEqual(len(playlist), 2)
        self.assertEqual(playlist.current(), track1)
        
        track3 = Track(3, "Blue", "Billie Eilish", 343, 5, datetime.now().isoformat())
        
        playlist.add(track3)
        playlist.play_next()
        
        self.assertEqual(len(playlist), 3)
        self.assertEqual(playlist.current(), track2)
        
        playlist.play_prev()
        self.assertEqual(playlist.current(), track1)
        
        playlist.play_next()
        playlist.remove_at(1)
        
        self.assertEqual(len(playlist), 2)
        self.assertEqual(playlist.current(), track3)
        
        playlist.reset_cursor()
        
        self.assertEqual(playlist.current(), track1)
        
        playlist.play_prev()
        
        self.assertEqual(playlist.current(), track1)
        
        playlist.remove_at(0)
        playlist.remove_at(0)
        
        self.assertEqual(len(playlist), 0)
        self.assertEqual(playlist.current(), None)
        
        playlist.play_next()
        self.assertEqual(playlist.current(), None)
    ...
        
if __name__ == '__main__':
    unittest.main()