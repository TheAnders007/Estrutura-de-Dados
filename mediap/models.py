from datetime import datetime

class Track:
    def __init__(self, id: int, titulo: str, artista: str, duracao: int, rating: int, data_adicao: str | datetime):
        self.id = id
        self.titulo = titulo
        self.artista = artista
        self.duracao = duracao
        self.rating = rating
        self.data_adicao = data_adicao
        
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id
        
    @property
    def titulo(self):
        return self._titulo
    
    @titulo.setter
    def titulo(self, titulo):
        self._titulo = titulo
        
    @property
    def artista(self):
        return self._artista
    
    @artista.setter
    def artista(self, artista):
        self._artista = artista
        
    @property
    def duracao(self):
        return self._duracao
    
    @duracao.setter
    def duracao(self, duracao):
        self._duracao = duracao
        
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
        return {"id": self.id, "titulo": self.titulo, "artista": self.artista, "duracao": self.duracao, "rating": self.rating, "data_adicao": self.data_adicao}
    
    @classmethod
    def de_dicionario(classe, dados):
        return classe(
            id = dados['id'],
            titulo = dados['titulo'],
            artista = dados['artista'],
            duracao = dados['duracao'],
            rating = dados['rating'],
            data_adicao = dados['data_adicao']
        )