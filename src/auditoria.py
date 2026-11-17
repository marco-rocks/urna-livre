from .computar_voto import calcular_hash_bloco

def validar_integridade_corrente(corrente):
    
    for i in range(1, len(corrente)):
        bloco_atual = corrente[i]
        bloco_anterior = corrente[i - 1]
        
        copia_bloco = bloco_atual.copy()
        hash_salvo = copia_bloco.pop("hash")
        
        if hash_salvo != calcular_hash_bloco(copia_bloco):
            print(f"[FRAUDE DETECTADA] O conteúdo do bloco #{i} foi alterado")
            exit
        
        if bloco_atual["hash_anterior"] != bloco_anterior["hash"]:
            print(f"[FRAUDE DETECTADA] A corrente foi quebrada entre os blocos ${i - 1} e {i}")
            exit
    return True

    
def apurar_votos(corrente):
    if not validar_integridade_corrente(corrente):
        print("[APURAÇÃO CANCELADA]: A blockchain foi corrompida ou fraudada")
        
    print("\n--- RESULTADO OFICIAL DA ELEIÇÃO (NOVA AURORA) ---")
    contagem = {}
    
    # Ignora o Bloco Gênesis (índice 0)
    for bloco in corrente[1:]:
        voto = bloco["voto"]
        contagem[voto] = contagem.get(voto, 0) + 1

    for candidato, total in sorted(contagem.items(), key=lambda x: x[1], reverse=True):
        print(f"{candidato}: {total} voto(s)")
    print("--------------------------------------------------\n")