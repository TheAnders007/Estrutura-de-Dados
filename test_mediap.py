import unittest
from datetime import datetime
from mediap.models import Track
from mediap.player import MediaPlayer
from mediap.cli import Cli

class TestePlaylist(unittest.TestCase):
    
    def setUp(self):
        self.player = MediaPlayer()
        
        self.track1 = Track(1, "My Way", "Olivia Rodrigo", 221, 5, datetime.now().isoformat())
        self.track2 = Track(2, "Praga", "Tim Bernardes", 201, 2, datetime.now().isoformat())
        self.track3 = Track(3, "Blue", "Billie Eilish", 343, 4, datetime.now().isoformat())
        
        self.player.library = {1: self.track1, 2: self.track2, 3: self.track3}
        
    def test_track(self):
        print("\nTestes para Track")
        track1_copia = Track.de_dicionario({"id": 1, "title": "My Way", "artist": "Olivia Rodrigo", "duration": 221, "rating": 5, "data_adicao": self.track1.data_adicao})
        
        self.assertEqual(self.track1.id, track1_copia.id)
        self.assertEqual(track1_copia.para_dicionario(), {"id": 1, "title": "My Way", "artist": "Olivia Rodrigo", "duration": 221, "rating": 5, "data_adicao": self.track1.data_adicao} )
        
        with self.assertRaises(ValueError):
            Track(id = 4, title = "Runnin Wild", artist = "Airboune", duration = 239, rating = 6, data_adicao = datetime.now().isoformat()
            )
        
    def test_doubly_linked_list_methods(self):
        print("\nTestes para os métodos da lista duplamente encadeada")   
        self.player.new_playlist("Playlist Teste")
         
        self.player.playlist.add(self.track1)
        self.player.playlist.add(self.track2)
        self.player.playlist.add(self.track3)
        
        self.assertEqual(len(self.player.playlist), 3)
        self.assertEqual(self.player.playlist.current(), self.track1)
        
        self.player.playlist.play_next()
        
        self.assertEqual(self.player.playlist.current(), self.track2)
        
        self.player.playlist.play_prev()
        self.assertEqual(self.player.playlist.current(), self.track1)
        
        self.player.playlist.play_next()
        self.player.playlist.remove_at(1)
        
        self.assertEqual(len(self.player.playlist), 2)
        self.assertEqual(self.player.playlist.current(), self.track3)
        
        self.player.playlist.reset_cursor()
        
        self.assertEqual(self.player.playlist.current(), self.track1)
        
        self.player.playlist.play_prev()   
        self.player.playlist.remove_at(0)
        self.player.playlist.remove_at(0)
        
        self.assertEqual(self.player.playlist.current(), None)
        
        self.player.playlist.play_next()
        self.assertEqual(self.player.playlist.current(), None)
    
    def test_load_library(self):
        print("\nTeste para load library")
        
        # Teste para arquivo que não existe
        self.player.load_library('biblioteca.json')
        
        self.player.load_library('mediap/library_exemplo.json')
        
    def test_list_library(self):
        print("\nTeste para list library")
        self.player.library = {}
        self.player.list_library()
        
        self.player.library = {1: self.track1, 2: self.track2, 3: self.track3}
        
        self.player.list_library()
        self.player.list_library("rating")
        self.player.list_library("title")
        self.player.list_library("artist")
        
    def test_playlist(self):
        print("\nTeste para operações da playlist")
        
        # Testes com playlist vazia
        self.player.new_playlist("  ")
        self.player.play()
        self.player.prev()
        self.player.next()
        self.player.playlist_remove(0)
        self.player.playlist_add(1)
        self.player.show_playlist()
        
        self.assertEqual(self.player.current_track, None)
        
        self.player.new_playlist("Playlist Teste")
        
        self.player.playlist_add(1)
        self.player.playlist_add(2)
        self.player.playlist_add(3)
        self.player.playlist_add(4)
        
        self.player.show_playlist()
        self.player.play()
        self.assertEqual(self.player.current_track.id, 1)
        
        self.player.next()
        self.assertEqual(self.player.current_track.id, 2)
        
        for n in range(2): self.player.next()
        for n in range(2): self.player.prev()
        
        self.assertEqual(self.player.current_track.id, 1)
        
        self.player.playlist_remove(4)
        self.player.playlist_remove(1)
        self.assertEqual(self.player.current_track.id, 2)
        
        self.player.prev()
        self.assertEqual(self.player.current_track.id, 2) 
    
    def test_up_next(self):
       print("\nTeste para fila up next")
       
       self.player.new_playlist("Playlist Teste")
       self.player.playlist_add(1)
       self.player.playlist_add(2)
       
       self.player.show_queue()
       
       self.player.enqueue(3)
       self.player.enqueue(4)
       
       self.player.show_queue()
        
       self.player.play()
       self.player.next()
        
       self.assertEqual(self.player.current_track, self.track3)
       
    def test_history(self):
        print("\nTeste para histórico")
        
        self.player.new_playlist("Playlist Teste")
        
        self.player.show_history()
        
        for i in range(0, 25):
            track = Track(i + 1, f"Faixa {i + 1}", f"Artista {i + 1}", 120, 4, datetime.now().isoformat())
            self.player.library[track.id] = track
            self.player.playlist_add(track.id)
            
            if (i == 0): self.player.play()
            else: self.player.next()
            
        self.player.show_history()
            
        self.assertEqual(self.player.history[-1]['track'].id, 6)
        
    def test_smart_shuffle(self):
        print("\nTeste para smart shuffle")
        
        self.player.library.clear()
        
        self.player.smart_shuffle(2)
        
        self.player.library = {1: self.track1, 2: self.track2, 3: self.track3}
        self.player.new_playlist("Playlist Teste")
        
        for n in range(1, 4): self.player.playlist_add(n)
        
        self.player.show_playlist()
        self.player.play()
        self.player.next()
            
        self.player.smart_shuffle(0)
        self.player.smart_shuffle(2)
        
        self.assertEqual(self.player.playlist.play_next(), self.track3)
        
    def test_save_and_load(self):
        print("\nTestes para save e load")
        
        self.player.new_playlist("Playlist Teste")
        self.player.playlist_add(1)
        
        self.player.save("pastainexistente/teste_save.json")
        self.player.save("teste_save_and_load.json")
        
        self.player.playlist = None
        
        self.player.load("arquivoinexistente.json")
        self.player.load("teste_save_and_load.json")
        
        self.assertIsNotNone(self.player.playlist)
        self.assertEqual(self.player.playlist.name, "Playlist Teste")
        self.assertEqual(self.player.playlist.current().id, self.track1.id)
        
    def test_cli(self):
        print("\nTestes para cli")
        
        cli = Cli()
        
        cli.process_cmd(" ")
        
        cli.process_cmd("help")
        
        cli.process_cmd("library")
        cli.process_cmd("library load")
        cli.process_cmd("library load library.json")
        cli.process_cmd("library list")
        cli.process_cmd("library list --by rating")
        
        cli.process_cmd("playlist")
        cli.process_cmd("playlist new")
        cli.process_cmd("playlist new 'Playlist Teste'")
        cli.process_cmd("playlist add")
        cli.process_cmd("playlist add 'a'")
        cli.process_cmd("playlist add 1")
        cli.process_cmd("playlist add 2")
        cli.process_cmd("playlist remove")
        cli.process_cmd("playlist remove 'a'")
        cli.process_cmd("playlist remove 2")
        cli.process_cmd("playlist show")
        
        cli.process_cmd("play")
        cli.process_cmd("next")
        cli.process_cmd("prev")
        
        cli.process_cmd("playlist add 3")
        cli.process_cmd("enqueue")
        cli.process_cmd("enqueue 3")
        cli.process_cmd("queue")
        cli.process_cmd("queue show")
        
        cli.process_cmd("history")
        
        cli.process_cmd("smart-shuffle")
        cli.process_cmd("smart-shuffle 2")
        
        cli.process_cmd("save")
        cli.process_cmd("save teste_save_and_load.json")
        cli.process_cmd("load")
        cli.process_cmd("load teste_save_and_load.json")
        
        
if __name__ == '__main__':
    unittest.main()