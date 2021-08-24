import redis
import random 


r = redis.Redis("bigdata-1")

def geraSenha(tipo_senha):
    
    if tipo_senha == "n":
        fila_normal= r.lrange('fila_normal', -1, -1) # Busca o utimo elemento
        if len(fila_normal) == 0:
            seq = 1
            seq_string = "N-"+str(seq)
            r.rpush('fila_normal', seq_string) # Adiciona a primeira senha na fila
            return seq_string

        else:
            senha_normal = int(r.lrange('fila_normal', -1, -1)[0].decode("utf-8").split("-")[1])
            seq = senha_normal + 1
            seq_string = "N-"+str(seq)
            r.rpush('fila_normal', seq_string) # Adiciona uma nova senha na fila
            emite_senha_normal = seq_string

            return emite_senha_normal


    if tipo_senha == "p":
        
        fila_prioritaria = r.lrange('fila_prioritaria', -1, -1) # Busca o utimo elemento
        
        if len(fila_prioritaria) == 0:
            seq = 1
            seq_string = "p-"+str(seq)
            r.rpush('fila_prioritaria', seq_string) # Adiciona uma nova senha na fila
            return seq_string
        else:
            
            senha_prioritaria = int(r.lrange('fila_prioritaria', -1, -1)[0].decode("utf-8").split("-")[1])
            seq = senha_prioritaria + 1
            seq_string = "P-"+str(seq)
            r.rpush('fila_prioritaria', seq_string)  # Adiciona uma nova senha na fila
            emite_senha_prioritaria = seq_string

            return emite_senha_prioritaria

        
        

def menu():
    print('''
            MENU:

            [N] - Emitir senha normal
            [P] - Emitir senha prioritaria
            [X] - Proxima senha
            [S] - Sair
        ''')
    return str(input('Escolha uma opcao: '))


while (True):
    escolha = menu()
    if(escolha == 'n'):
        print('Emitir senha normal')
        senha = geraSenha('n')
        print("SENHA" , senha)
        r.rpush('fila_geral', senha)

    
    if(escolha == 'p'):
        print('Emitir senha prioritaria')
        senha = geraSenha('p')
        print("SENHA" , senha)
        r.rpush('fila_geral', senha)

    if(escolha == 'x'):
        
        print('Proxima senha')

        # verifica se tem dados 
        if r.llen('fila_geral') == 0:
            print("FILA VAZIA")

        else:

            fila_geral = r.lrange('fila_geral', -1, -1)[0].decode("utf-8").split("-")
            if fila_geral[1] != 0:
                
                
                if fila_geral[0].split("-")[0] == "N":
                    if fila_geral[1] != 0:
                        print("Senha : ", '-'.join(fila_geral))
                        r.rpop('fila_geral')
                    
                else:
                    
                    if fila_geral[1] != 0:
                        print("Senha : ", '-'.join(fila_geral))
                        r.rpop('fila_geral')
                        
        
    if (escolha == 's'):
        # limpa as filas 
        r.delete('fila_geral')
        r.delete('fila_normal')
        r.delete('fila_prioritaria')
        quit()