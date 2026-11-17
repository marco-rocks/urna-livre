import sys
from src.armazenar_e_carregar import carregar_blockchain_do_arquivo, salvar_blockchain_para_arquivo
from src.gerar_bloco_genese import gerar_bloco_genese
from src.computar_voto import (
    get_informacoes_basicas,
    get_cpfs_registrados,
    registrar_voto,
    calcular_hash_bloco
)
from src.auditoria import validar_integridade_corrente, apurar_votos

CANDIDATOS = {
    "10": "Floriano Peixoto",
    "20": "Getulio Vargas",
    "30": "Castelo Branco",
    "00": "Voto Nulo"
}

def exibir_cabecalho():
    print("\n" + "=" * 55)
    print("         🗳️  SISTEMA URNA LIVRE (BLOCKCHAIN)  🗳️         ")
    print("=" * 55)

def exibir_menu():
    print("""
[1] Votar
[2] Visualizar Livro-Razão (Blockchain)
[3] Auditar Integridade da Blockchain
[4] Apurar Resultado da Eleição
[0] Sair
""")

def menu_votar(livro_razao, cache_cpfs):
    print("\n--- CEDULA ELEITORAL ---")
    for num, nome in CANDIDATOS.items():
        print(f"  [{num}] {nome}")
    print("------------------------")

    info_usuario = get_informacoes_basicas()

    cand_str = str(info_usuario["candidato"])
    if cand_str not in CANDIDATOS:
        cand_str = "00"
    info_usuario["candidato"] = cand_str

    if info_usuario["id"] in cache_cpfs:
        print(f"\n❌ [BLOQUEADO] O eleitor já registrou seu voto nesta eleição!")
        return

    bloco = registrar_voto(livro_razao, info_usuario, cache_cpfs)
    bloco["hash"] = calcular_hash_bloco(bloco)
    livro_razao.append(bloco)
    cache_cpfs.add(bloco["id_eleitor"])

    salvar_blockchain_para_arquivo(livro_razao)

    nome_votado = CANDIDATOS.get(info_usuario["candidato"], "Nulo")
    print("\n" + "-" * 45)
    print("✅ VOTO CONFIRMADO E REGISTRADO NA BLOCKCHAIN!")
    print(f"   Candidato : {nome_votado} ({info_usuario['candidato']})")
    print(f"   Hash Bloco: {bloco['hash']}")
    print("-" * 45)

def menu_visualizar_blockchain(livro_razao):
    print("\n" + "=" * 65)
    print(f"       🔗 LIVRO-RAZÃO: {len(livro_razao)} BLOCO(S) ENCADERMADO(S)       ")
    print("=" * 65)
    for i, bloco in enumerate(livro_razao):
        tipo = "BLOCO GÊNESIS" if i == 0 else f"BLOCO #{i}"
        print(f"\n┌─ [ {tipo} ] " + "─" * 45)
        print(f"│ Timestamp     : {bloco['timestamp']}")
        print(f"│ ID Eleitor    : {bloco['id_eleitor']}")
        print(f"│ Voto          : {bloco['voto']}")
        print(f"│ Hash Anterior : {bloco['hash_anterior']}")
        print(f"│ Hash Atual    : {bloco['hash']}")
        print("└" + "─" * 58)
        if i < len(livro_razao) - 1:
            print("         ↓ (encadeamento criptográfico)")

def main():
    exibir_cabecalho()

    livro_razao = carregar_blockchain_do_arquivo()

    if not livro_razao:
        print("\n⚙️ Nenhuma blockchain encontrada. Inicializando Bloco Gênesis...")
        genesis_block = gerar_bloco_genese()
        livro_razao.append(genesis_block)
        salvar_blockchain_para_arquivo(livro_razao)
        print("✅ Bloco Gênesis criado e salvo com sucesso!")

    cache_cpfs = get_cpfs_registrados(livro_razao)

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_votar(livro_razao, cache_cpfs)
        elif opcao == "2":
            menu_visualizar_blockchain(livro_razao)
        elif opcao == "3":
            print("\n🔍 Auditando integridade de todos os blocos...")
            integro = validar_integridade_corrente(livro_razao)
            if integro:
                print("✅ [SUCESSO] Todos os blocos e elos criptográficos estão 100% íntegros!")
        elif opcao == "4":
            apurar_votos(livro_razao)
        elif opcao == "0":
            print("\nEncerrando o sistema. Até logo!\n")
            break
        else:
            print("⚠️ Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
