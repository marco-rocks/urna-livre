import sys
import copy
from pathlib import Path

# Adiciona a raiz do projeto para importar diretamente seus módulos
DIRETORIO_RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIRETORIO_RAIZ))

from src.gerar_bloco_genese import gerar_bloco_genese
from src.computar_voto import (
    registrar_voto,
    calcular_hash_bloco,
    get_cpfs_registrados
)
from src.auditoria import validar_integridade_corrente, apurar_votos
from src.armazenar_e_carregar import (
    salvar_blockchain_para_arquivo,
    carregar_blockchain_do_arquivo
)


def simular():
    print("=" * 60)
    print("          SIMULAÇÃO DE TESTES - URNA LIVRE")
    print("=" * 60)

    # ---------------------------------------------------------
    # CENÁRIO 1: Geração e validação do Bloco Gênesis
    # ---------------------------------------------------------
    print("\n[CENÁRIO 1] Bloco Gênesis:")
    blockchain = []
    bloco_genese = gerar_bloco_genese()
    blockchain.append(bloco_genese)
    print("Bloco Gênesis:", blockchain[0])

    # ---------------------------------------------------------
    # CENÁRIO 2: Votação normal (votos legítimos)
    # ---------------------------------------------------------
    print("\n[CENÁRIO 2] Registrando votos legítimos:")
    cache_cpfs = get_cpfs_registrados(blockchain)

    votos_simulados = [
        {"id": "hash_eleitor_1", "candidato": "10"},
        {"id": "hash_eleitor_2", "candidato": "20"},
        {"id": "hash_eleitor_3", "candidato": "10"},
        {"id": "hash_eleitor_4", "candidato": "30"},
        {"id": "hash_eleitor_5", "candidato": "00"},
    ]

    for info_usuario in votos_simulados:
        bloco = registrar_voto(blockchain, info_usuario, cache_cpfs)
        bloco["hash"] = calcular_hash_bloco(bloco)
        blockchain.append(bloco)
        cache_cpfs.add(bloco["id_eleitor"])

    print(f"Total de blocos na cadeia: {len(blockchain)}")

    # ---------------------------------------------------------
    # CENÁRIO 3: Validação da integridade da blockchain legítima
    # ---------------------------------------------------------
    print("\n[CENÁRIO 3] Validação de integridade (corrente íntegra):")
    valida = validar_integridade_corrente(blockchain)
    print(f"Resultado da validação: {valida}")

    # ---------------------------------------------------------
    # CENÁRIO 4: Tentativa de voto duplo (mesmo CPF/id)
    # ---------------------------------------------------------
    print("\n[CENÁRIO 4] Testando tentativa de voto duplo:")
    voto_duplicado = {"id": "hash_eleitor_1", "candidato": "20"}
    registrar_voto(blockchain, voto_duplicado, cache_cpfs)

    # ---------------------------------------------------------
    # CENÁRIO 5: Detecção de fraude (adulteração de voto em um bloco)
    # ---------------------------------------------------------
    print("\n[CENÁRIO 5] Detecção de fraude por adulteração de conteúdo:")
    blockchain_fraudada = copy.deepcopy(blockchain)
    blockchain_fraudada[1]["voto"] = "30"  # alterando voto do bloco #1
    validar_integridade_corrente(blockchain_fraudada)

    # ---------------------------------------------------------
    # CENÁRIO 6: Detecção de fraude (quebra de elo entre blocos)
    # ---------------------------------------------------------
    print("\n[CENÁRIO 6] Detecção de fraude por quebra de elo (hash_anterior):")
    blockchain_elo_quebrado = copy.deepcopy(blockchain)
    blockchain_elo_quebrado[2]["hash_anterior"] = "hash_falso_injetado"
    validar_integridade_corrente(blockchain_elo_quebrado)

    # ---------------------------------------------------------
    # CENÁRIO 7: Apuração oficial dos votos
    # ---------------------------------------------------------
    print("\n[CENÁRIO 7] Apuração dos votos:")
    apurar_votos(blockchain)

    # ---------------------------------------------------------
    # CENÁRIO 8: Salvamento e carregamento com criptografia
    # ---------------------------------------------------------
    print("[CENÁRIO 8] Persistência em arquivo (salvar e carregar):")
    salvar_blockchain_para_arquivo(blockchain)
    blockchain_recuperada = carregar_blockchain_do_arquivo()
    print(f"Blocos salvos: {len(blockchain)} | Blocos carregados do arquivo: {len(blockchain_recuperada)}")
    print(f"Integridade da cadeia carregada: {validar_integridade_corrente(blockchain_recuperada)}")

    print("\n" + "=" * 60)
    print("          SIMULAÇÃO FINALIZADA")
    print("=" * 60)


if __name__ == "__main__":
    simular()
