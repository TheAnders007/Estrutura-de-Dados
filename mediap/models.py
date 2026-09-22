from datetime import datetime

class Track:
    def __init__(self, id: int, titulo: str, artista: str, duracao: int, rating: int, data_adicao: str | datetime):
        self.id = id
        self.titulo = titulo
        self.artista = artista
        self.dutacao = duracao
        self.rating = rating
        self.data_adicao = data_adicao
        
    @property
    def id(self):
        return self.id
    
    @id.setter
    def id(self, id):
        self.id = id
        
    @property
    def titulo(self):
        return self.titulo
    
    @titulo.setter
    def titulo(self, titulo):
        self.titulo = titulo
        
    @property
    def artista(self):
        return self.artista
    
    @artista.setter
    def artista(self, artista):
        self.arista = artista
        
    @property
    def duracao(self):
        return self.duracao
    
    @duracao.setter
    def duracao(self, duracao):
        self.duracao = duracao
        
    @property
    def rating(self):
        return self.rating
        
    @rating.setter
    def rating(self, rating):
        self.rating = rating
        
    @property
    def data_adicao(self):
        return self.data_adicao
    
    @data_adicao.setter
    def data_adicao(self, data_adicao):
        self.data_adicao = data_adicao