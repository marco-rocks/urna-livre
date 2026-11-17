import json
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

ARQUIVO_BLOCKCHAIN = BASE_DIR / 'data' / 'blockchain.txt'

def obter_chave_fernet():
    chave = os.getenv('CHAVE_BLOCKCHAIN')
    
    if not chave:
        raise ValueError('A chave da blockchain não foi encontrada')
    
    return Fernet(chave.encode())

def salvar_blockchain_para_arquivo(corrente):
    
    cursor_fernet = obter_chave_fernet()
    
    dados_json = json.dumps(corrente, indent=4)
    dados_criptografados = cursor_fernet.encrypt(dados_json.encode())
    
    os.makedirs(os.path.dirname(ARQUIVO_BLOCKCHAIN), exist_ok=True)
    
    with open(ARQUIVO_BLOCKCHAIN, 'wb') as arquivo_blockchain:
        arquivo_blockchain.write(dados_criptografados)
        
def carregar_blockchain_do_arquivo():
    
    if not os.path.exists(ARQUIVO_BLOCKCHAIN) or os.path.getsize(ARQUIVO_BLOCKCHAIN) == 0:
        return []
    
    cursor_frenet = obter_chave_fernet()
    
    with open(ARQUIVO_BLOCKCHAIN, 'rb') as arquivo:
        dados_criptografados = arquivo.read()
        
    dados_descriptografados = cursor_frenet.decrypt(dados_criptografados).decode()
    return json.loads(dados_descriptografados)