from .computar_voto import calcular_hash_bloco


def gerar_bloco_genese():
    
    bloco_genese = {
        "timestamp": 0,
        "id_eleitor": 0,
        "voto": 0,
        "hash_anterior": 0,
    }
    
    bloco_genese["hash"] = calcular_hash_bloco(bloco_genese)
    
    return bloco_genese

