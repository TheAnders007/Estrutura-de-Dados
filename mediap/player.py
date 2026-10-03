import os
import json
from datetime import datetime
from .models import Track
from .doubly_linked_list import DoublyLinkedList
from collections import deque
from queue import PriorityQueue

def convert_track_duration(duration: int):
    minutes = duration // 60
    seconds = duration % 60
    
    return f"{minutes:02d}:{seconds:02d}"
    
class MediaPlayer:
    class Playlist(DoublyLinkedList):
        def __init__(self, name):
            super().__init__()
            self.name = name
    
    def __init__(self):
        self.current_track = None
        self.library = {}
        self.playlist = None
        self.up_next = deque()
        self.history = deque(maxlen=20)
        
    def load_library(self, filepath):
        
        final_filepath = filepath if (os.path.exists(filepath)) else f"mediap/{filepath}"
            
        try:
            with open(f"{final_filepath}", 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.library.clear()
                
                for item in data:
                    track = Track.de_dicionario(item)
                    self.library[track.id] = track
        
            print(f"Biblioteca Carregada: {len(self.library)} faixas.")
        except FileNotFoundError:
            print(f"Erro: O arquivo {filepath} não foi encontrado.")
        except Exception as e:
            print(f"Erro ao carregar a biblioteca: {e}")
            
    def list_library(self, criterion = "id"):
        if not (self.library):
            print("Biblioteca de faixas vazia.")
            return 
        
        tracks = list(self.library.values())
        
        if criterion == "rating":
            tracks.sort(key=lambda track:track.rating, reverse=True)
        elif criterion == "title":
            tracks.sort(key=lambda track:track.title.lower())
        elif criterion == "artist":
            tracks.sort(key=lambda track:track.artist.lower())
        else:
            tracks.sort(key=lambda track:track.id)
            
        for count, track in enumerate(tracks, start=1):
            print(f"{count}. [{track.id}] {track.title} - {track.artist} ({convert_track_duration(track.duration)})") 
            
    def new_playlist(self, playlist_name):
        if not playlist_name.strip():
            return
        
        self.playlist = self.Playlist(playlist_name)
        print(f"Playlist '{self.playlist.name}' criada.")
               
    def playlist_add(self, track_id):
        if not track_id in self.library:
            print(f"Erro: Não foi encontrada faixa com id {track_id}")
            return
        
        if self.playlist is None:
            print("Antes de adicionar uma faixa, crie a playlist.")
            return
        
        track = self.library[track_id]
        self.playlist.add(track)
        
    def playlist_remove(self, pos):
        if self.playlist is None:
            print("Antes de remover uma faixa, crie a playlist.")
            return
        
        if pos > len(self.playlist):
            print("A posição indicada extrapola o tamanho da playlist.")
            return
        
        if pos <= 0:
            print("A posição mínima começa a partir de '1'.")
            return
        
        self.playlist.remove_at(pos - 1)
        self.current_track = self.playlist.current()
        
    def show_playlist(self):
        if not self.playlist or len(self.playlist) == 0:
            print("A playlist está vazia.")
            return
        
        current_track = self.playlist.current()
        for index, track in enumerate(self.playlist, start=1):
            cursor_symbol = "> " if current_track == track else "  "
            print(f"{cursor_symbol}{index}. {track.title} - {track.artist} ({convert_track_duration(track.duration)})")
        
    def history_add(self, current_track):
        self.history.appendleft({
            'track': current_track,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })
        
    def play(self):
        if not self.playlist or (len(self.playlist)) == 0:
            print("A playlist está vazia.")
            return
        
        current_track = self.playlist.current()
        if current_track:
            self.current_track = current_track
            
            print(f">>> Tocando: \"{current_track.title}\" - {current_track.artist} ({convert_track_duration(current_track.duration)})")
            
            self.history_add(current_track)
            
    def next(self):
        if len(self.up_next) > 0:
            current_track = self.up_next.popleft()
            self.current_track = current_track
            
            print(f">>> Tocando: \"{current_track.title}\" - {current_track.artist} ({convert_track_duration(current_track.duration)})")
            
            self.history_add(current_track)
            return
        
        if not self.playlist or len(self.playlist) == 0:
            print("A playlist está vazia.")
            return
        
        current_track = self.playlist.play_next()
        if current_track:
            self.current_track = current_track
            print(f">>> Tocando: \"{current_track.title}\" - {current_track.artist} ({convert_track_duration(current_track.duration)})")
            self.history_add(current_track)
        else:
            print("A playlist já chegou ao seu fim.")
    
    
    def prev(self):
        if not self.playlist or len(self.playlist) == 0:
            print("A playlist está vazia.")
            return
        
        current_track = self.playlist.play_prev()
        if current_track:
            self.current_track = current_track
            print(f">>> Tocando: \"{current_track.title}\" - {current_track.artist} ({convert_track_duration(current_track.duration)})")
            self.history_add(current_track)
        else:
            print("A playlist está no seu início. Não há faixas antigas.")
        
    
    def enqueue(self, track_id):
        if track_id not in self.library:
            print(f"Erro: Não foi encontrada faixa com id {track_id}")
            return 
        
        track = self.library[track_id]
        self.up_next.append(track)
        
        
    def show_queue(self):
        if len(self.up_next) == 0:
            print("A fila Up Next está vazia")
            return
        
        for index, track in enumerate(self.up_next, start=1):
            print(f"{index}. {track.title} - {track.artist} ({convert_track_duration(track.duration)})")
    
            
    def show_history(self):
        if len(self.history) == 0:
            print("Não há registro de faixas no histórico.")
            return
        
        for index, item in enumerate(self.history, start=1):
            print(f"{index}. {item['track'].title} - {item['track'].artist} ({item['timestamp']})")
            
    def smart_shuffle(self, n: int):
        if not self.library:
            print("Biblioteca vazia. Experimente carregar tracks primeiro.")
            return
        
        if n <= 0:
            print("O número de tracks deve ser maior que 0.")
            return
        
        recents_tracks = []
        for item in self.history:
            recents_tracks.append(item["track"].id)

            if (len(recents_tracks) == 5):
                break
            
        smart_queue = PriorityQueue()
        for track_id, track in self.library.items():
            penalty = 0
            if track_id in recents_tracks:
                penalty = 5 - recents_tracks.index(track_id)
                
            priority_key = -10 * track.rating + penalty
            smart_queue.put((priority_key, track_id, track))
            
        self.new_playlist("Smart Shuffle")
        
        count = 0
        while not smart_queue.empty() and count < n:
            track_id = smart_queue.get()[1]
            self.playlist_add(track_id)
            count += 1
            
        print(f"Smart Shuffle foi criado com {count} faixas na playlist.")
        
    def save(self, filepath):
        playlist_ids = []
        cursor_track_id = None
        
        if self.playlist and len(self.playlist) > 0:
            current_track = self.playlist.current()
            if current_track:
                cursor_track_id = current_track.id
                
            for track in self.playlist:
                playlist_ids.append(track.id)
                
        up_next_ids = [track.id for track in self.up_next]
        
        history_data = [{'track_id': item['track'].id, 'timestamp': item['timestamp']} for item in self.history]
        
        data = {
            'playlist_name': self.playlist.name if self.playlist else None,
            'playlist_tracks': playlist_ids,
            'cursor_track_id': cursor_track_id,
            'up_next_tracks': up_next_ids,
            'history': history_data
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            print(f"Estado salvo com sucesso em {filepath}")
        except Exception as e:
            print(f"Erro ao gravar dados: {e}")
            
                
    def load(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
            playlist_name = data["playlist_name"]
            playlist_tracks = data["playlist_tracks"]
            cursor_track_id = data["cursor_track_id"]
            
            if playlist_name:
                self.playlist = self.Playlist(playlist_name)
                for track_id in playlist_tracks:
                    if track_id in self.library:
                        self.playlist.add(self.library[track_id])

                if cursor_track_id and len(self.playlist) > 0:
                    self.playlist.reset_cursor()
                    while self.playlist.current() and self.playlist.current().id != cursor_track_id:
                        self.playlist.play_next()
            
            self.up_next.clear()
            for track_id in data["up_next_tracks"]:
                if track_id in self.library:
                    self.up_next.append(self.library[track_id])
                    
            self.history.clear()
            for item in data["history"]:
                if item["track_id"] in self.library:
                    self.history.append({"track": self.library[item["track_id"]], "timestamp": item["timestamp"] })
                    
            print(f"Estado obtido com sucesso em {filepath}")
        except FileNotFoundError:
            print(f"Erro: o arquivo {filepath} não foi encontrado.")
        except Exception as e:
            print(f"Erro ao carregar o estado: {e}")
        
            