from player import MediaPlayer
import shlex

class Cli:
    def __init__(self):
        self.player = MediaPlayer()
        
    def help(self):
        print("""
        Comandos Disponíveis
            library load <arquivo> —carrega a biblioteca a partir de CSV ou JSON;
            library list [--by rating|title|artist] — lista as faixas, ordenando pelo critério informado (default: id);
            playlist new <nome> —cria uma nova playlist vazia e a torna a "atual";
            playlist add <track_id> - adiciona a faixa ao final da playlist atual;
            playlist remove <pos> - remove a faixa na posição pos;
            playlist show - imprime a playlist com cursor marcado por ">"(ou seja, indica a música em execução ou que será executada);
            play - inicia/retoma a reprodução a partir do cursor;
            next - avança (a fila Up Next tem precedência sobre a próxima faixa da playlist);
            prev - retrocede ocursor da playlist;
            enqueue <track_id> - acrescenta a faixa à fila Up Next;
            queue show - imprime o conteúdo da fila Up Next na ordem em que será tocada;
            history - imprime o histórico, do mais recente ao mais antigo;
            smart-shuffle <n> - gera nova playlist de n faixas usando a fila com prioridade;
            save <arquivo> - serializa o estado completo (playlist, fila up next, histórico, cursor) em JSON;
            load <arquivo> - restaura o estado a partir de JSON;
            help - imprime os comandos disponíveis;
            quit - encerra o programa
            """)
        
    def process_cmd(self, line):
        line = line.strip()
        if not line:
            return True
        
        try:
            parts = shlex.split(line)
            
            command = parts[0]
                    
            if command == "quit":
                print("Sistema do MediaPlayer Encerrado!")
                return False
            
            elif command == "help":
                self.help()
            
            elif command == "library":
                if len(parts) < 2:
                    print("Comando incompleto. Use library load <arquivo> ou library list.")
                    return True
                
                subcommand = parts[1]
                if subcommand == "load":
                    if len(parts) == 2:
                        print("Infore o arquivo que deseje que seja carregado.")
                    else:
                        self.player.load_library(parts[2])
                elif subcommand == "list":
                    criterion = "id"
                    if (len(parts) == 4 and parts[2] == "--by"):
                        criterion = parts[3]
                    self.player.list_library(criterion)
                    
            elif command == "playlist":
                if len(parts) < 2:
                    print("Comando incompleto. Use playlist <new | add | remove | show>")
                    return True
                
                subcommand = parts[1]
                if subcommand == "new":
                    if len(parts) == 2:
                        print("O nome da playlist não foi informado.")
                    else:
                        nome = " ".join(parts[2:])
                        self.player.new_playlist(nome)
                        
                elif subcommand == "add":
                    if len(parts) == 2:   
                        print("O id da faixa a ser adicionada não foi informado.")
                    elif not parts[2].isdigit():
                        print("O id da faixa precisa ser um número inteiro.")
                    else:
                        self.player.playlist_add(int(parts[2]))
                        
                elif subcommand == "remove":
                    if len(parts) == 2:   
                        print("O id da faixa a ser removida não foi informado.")
                    elif not parts[2].isdigit():
                        print("O id da faixa precisa ser um número inteiro.")
                    else:
                        self.player.playlist_remove(int(parts[2]))
                
                elif subcommand == "show":
                    self.player.show_playlist()
                    
            return True
            
        except ValueError as e:
            print(f"Erro no comando: {e}")
            return True
        
            
    def run(self):
        print("MediaPlayer Cli")
        
        running = True
        while running:
            try:
                cliInput = input("mediap> ")
                running = self.process_cmd(cliInput)
            except KeyboardInterrupt:
                break
                
            

