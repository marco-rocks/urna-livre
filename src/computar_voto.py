import hashlib
import json
import time


def get_cpfs_registrados(corrente):
    return {bloco["id_eleitor"] for bloco in corrente[1:]}

def get_informacoes_basicas():
    
    cpf_usuario = hashlib.sha256(input('Informe seu CPF sem pontuação: ').encode()).hexdigest()
    num_candidato = int(input("Informe o número que representa seu candidato: "))
    
    info_usuario = {
        "id": cpf_usuario,
        "candidato": num_candidato
    }
    
    return info_usuario

def calcular_hash_bloco(bloco):
    
    hash_bloco = json.dumps(bloco, sort_keys=True).encode()
    return hashlib.sha256(hash_bloco).hexdigest()

def registrar_voto(corrente, informacoes_voto, conjunto_cache_cpfs):

    hash_cpf = informacoes_voto["id"]
    
    if hash_cpf in conjunto_cache_cpfs:
        print(f"[BLOQUEADO O usuario de identificador {hash_cpf} já teve seu voto registrado")
        exit
        
    hash_ultimo_bloco = corrente[-1]["hash"]
    
    bloco_atual = {
        "timestamp": time.time(),
        "id_eleitor": informacoes_voto["id"],
        "voto": informacoes_voto["candidato"],
        "hash_anterior": hash_ultimo_bloco
    }
    
    return bloco_atual