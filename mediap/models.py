from datetime import datetime

class Track:
    def __init__(self, id: int, title: str, artist: str, duration: int, rating: int, data_adicao: str | datetime):
        self.id = id
        self.title = title
        self.artist = artist
        self.duration = duration
        self.rating = rating
        self.data_adicao = data_adicao
        
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id
        
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        self._title = title
        
    @property
    def artist(self):
        return self._artist
    
    @artist.setter
    def artist(self, artist):
        self._artist = artist
        
    @property
    def duration(self):
        return self._duration
    
    @duration.setter
    def duration(self, duration):
        self._duration = duration
        
    @property
    def rating(self):
        return self._rating
        
    @rating.setter
    def rating(self, rating):
        if 1 <= rating <= 5:
            self._rating = rating
        else:
            raise ValueError("O valor de rating deve ser inteiro e estar entre 1 e 5.")
        
    @property
    def data_adicao(self):
        return self._data_adicao
    
    @data_adicao.setter
    def data_adicao(self, data_adicao):
        self._data_adicao = data_adicao
        
    def para_dicionario(self):
        return {"id": self.id, "title": self.title, "artist": self.artist, "duration": self.duration, "rating": self.rating, "data_adicao": self.data_adicao}
    
    @classmethod
    def de_dicionario(classe, dados):
        return classe(
            id = dados['id'],
            title = dados['title'],
            artist = dados['artist'],
            duration = dados['duration'],
            rating = dados['rating'],
            data_adicao = dados['data_adicao']
        )