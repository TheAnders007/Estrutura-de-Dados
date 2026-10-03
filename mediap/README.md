# Mini Projeto 01 - Media Player

Este projeto refere-se ao primeiro trabalho da componente curricular SMD0033 Estrutura de Dados, ministrada pelo docente Ernesto Trajano no semestre 2026.2.

A atividade consiste em um protótipo de reprodutor de faixas musicais pelo terminal, aplicando diferentes estruturas de dados (lista duplamente encadeada, filas e deque) nas funcionalidades do sistema como montagem de playlists, simulação da reprodução de faixas, armazenamento em histórico etc.

## Executar o Projeto

Dentro da pasta `MiniProjeto01/`, execute:

```bash
python -m mediap
```

Esse comando executará o terminal do MediaPlayer.

*Observação: Para comando acima funcione de forma estrita, o nome do arquivo `main.py` foi substituído por `__main__.py`, já que, ao executá-lo, é procurado por padrão o arquivo de nome `__main__.py`.*

Para executar as operações de testes, execute:

```bash
python -m unittest test_mediap.py
```

## Comandos do MediaPlayer Cli

Comando | Explicação
:---:     | :---: |
**library load \<arquivo>** | Carrega a biblioteca a partir de um JSON
**library list [ --by rating \| title \| artist ]** | lista as faixas, ordenando pelo critério informado (default: id)
**playlist new \<nome>** | cria uma nova playlist vazia e a torna a “atual”
**playlist add \<track_id>** | adiciona a faixa ao final da playlist atual
**playlist remove \<pos>** | remove a faixa na posição pos (o discente definiu que as posições começam a partir do número 1 em vez de 0 para esse comando)
**playlist show** | imprime a playlist com cursor marcado por ">" (ou seja, indica a música em execução ou que será executada)
**play** | inicia/retoma a reprodução a partir do cursor
**next** | avança (a fila Up Next tem precedência sobre a próxima faixa da playlist)
**prev** | retrocede o cursor da playlist
**enqueue \<track_id>** | acrescenta a faixa à fila Up Next
**queue show** | imprime o conteúdo da fila Up Next na ordem em que será tocada
**history** | imprime o histórico, do mais recente ao mais antigo
**smart-shuffle \<n>** | gera nova playlist de n faixas usando a fila com prioridade
**save \<arquivo>** | serializa o estado completo (playlist, fila up next, histórico, cursor) em JSON
**load \<arquivo>** | restaura o estado a partir de JSON
**help** | imprime os comandos disponíveis
**quit** | encerra o programa.

## Exemplo de Sessão 

```bash
MediaPlayer Cli
mediap> library load library.json
Biblioteca Carregada: 10 faixas.
mediap> library list --by title
1. [8] Beleza Eterna - Tim Bernardes (05:30)
2. [7] Doce Futuro - ANAVITÓRIA (04:47)
3. [2] Fases - Tim Bernardes (04:19)
4. [3] Honeybee - Olivia Rodrigo (03:45)
5. [4] Me Ajude a Salvar os Domingos - Liniker (07:24)
6. [1] Minto pra quem perguntar - ANAVITÓRIA (03:08)
7. [6] Smokin Out The Window - Bruno Mars (03:21)
8. [5] The Grudge - Olivia Rodrigo (03:10)
9. [10] Tudo - Liniker (03:39)
10. [9] Uptown Funk - Bruno Mars (04:05)
mediap> playlist new Minha Playlist
Playlist 'Minha Playlist' criada.
mediap> playlist add 1
mediap> playlist add 2
mediap> playlist add 3
mediap> playlist show
> 1. Minto pra quem perguntar - ANAVITÓRIA (03:08)
  2. Fases - Tim Bernardes (04:19)
  3. Honeybee - Olivia Rodrigo (03:45)
mediap> play
>>> Tocando: "Minto pra quem perguntar" - ANAVITÓRIA (03:08)
mediap> enqueue 3
mediap> queue show
1. Honeybee - Olivia Rodrigo (03:45)
mediap> next
>>> Tocando: "Honeybee" - Olivia Rodrigo (03:45)
mediap> next
>>> Tocando: "Fases" - Tim Bernardes (04:19)
mediap> smart-shuffle 3
Playlist 'Smart Shuffle' criada.
Smart Shuffle foi criado com 3 faixas na playlist.
mediap> enqueue 9
mediap> playlist show
> 1. Me Ajude a Salvar os Domingos - Liniker (07:24)
  2. Beleza Eterna - Tim Bernardes (05:30)
  3. Minto pra quem perguntar - ANAVITÓRIA (03:08)
mediap> queue show
1. Uptown Funk - Bruno Mars (04:05)
mediap> history
1. Fases - Tim Bernardes (14:35:19)
2. Honeybee - Olivia Rodrigo (14:35:13)
3. Minto pra quem perguntar - ANAVITÓRIA (14:34:19)
mediap> save estado.json
Estado salvo com sucesso em estado.json
mediap> quit
Sistema do MediaPlayer Encerrado!
...

mediap> library load library.json
Biblioteca Carregada: 10 faixas.
mediap> load estado.json
Estado obtido com sucesso em estado.json
mediap> playlist show   
> 1. Me Ajude a Salvar os Domingos - Liniker (07:24)
  2. Beleza Eterna - Tim Bernardes (05:30)
  3. Minto pra quem perguntar - ANAVITÓRIA (03:08)
mediap> queue show
1. Uptown Funk - Bruno Mars (04:05)
mediap> history
1. Fases - Tim Bernardes (14:35:19)
2. Honeybee - Olivia Rodrigo (14:35:13)
3. Minto pra quem perguntar - ANAVITÓRIA (14:34:19)

```

## Fórmula da Smart-Shuffle

Para definir as chaves de prioridade das faixas na playlist gerada pelo método de smart-shuffle, o discente optou por utilizar a mesma fórmula apresentada no documento, sendo essa:

$$
chave(f) = −10\ · rating(f) + penalty(f)
$$

Se a faixa (f) estiver entre as 5 últimas tocadas:

$$
penalty(f) = 5 - posHist(f)
$$

Sendo `posHist(f)` a posição que determinada faixa ocupa no histórico.

Se não:

$$
penalty(f) = 0
$$

Como sugerido, foi utilizada a classe PriorityQueue, evidenciada no seguinte bloco de código do arquivo `player.py`:

```python
# Método para Smart Shuffle - Fila com Prioridade

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
```


