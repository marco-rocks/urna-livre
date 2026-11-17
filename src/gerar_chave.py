import os
from cryptography.fernet import Fernet

ENV_FILE = ".env"
NOME_CHAVE = "CHAVE_BLOCKCHAIN"

def gerar_chave():
    
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r') as f:
            conteudo = f.read()
            
            if NOME_CHAVE in conteudo:
                print("A chave do blockchain já foi gerada no arquivo .env")
                return
            
    nova_chave = Fernet.generate_key().decode()
    
    mode = "a" if os.path.exists(ENV_FILE) else "w"
    
    with open(ENV_FILE, mode) as f:
        f.write(f"{NOME_CHAVE}={nova_chave}\n")
        
    print("Nova chave do blockchain gerada com sucesso!")
    
if __name__ == "__main__":
    gerar_chave()