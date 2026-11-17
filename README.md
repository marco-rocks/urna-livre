# 🗳️ Urna Livre - Blockchain Eleitoral

Sistema de votação eletrônica transparente, auditável e imutável baseado no conceito de **Blockchain** e criptografia de ponta com **SHA-256** e **Fernet**.

O projeto visa garantir o anonimato do eleitor, evitar fraudes (como voto duplicado ou alteração de votos em blocos passados) e permitir a auditoria pública e independente de todo o processo de votação.

---

## 🚀 Funcionalidades

- **Bloco Gênesis Automático:** Criação e encadeamento inicial da blockchain na primeira inicialização.
- **Anonimato do Eleitor:** O CPF do eleitor é transformado em um hash criptográfico irreversível (SHA-256) antes do registro.
- **Proteção contra Voto Duplo:** Cache e validação de eleitores para impedir múltiplos votos de um mesmo CPF.
- **Integridade Criptográfica (Blockchain):** Cada bloco é selado com um hash próprio e aponta para o hash do bloco anterior (`hash_anterior`), garantindo imutabilidade.
- **Auditoria contra Fraudes:** Ferramenta integrada capaz de detectar qualquer alteração retroativa de conteúdo ou quebra de elo na corrente.
- **Armazenamento Seguro:** Persistência dos dados em disco criptografada com a biblioteca **Fernet** (chave simétrica).
- **Apuração Oficial dos Votos:** Consolidação e ranqueamento automático dos votos por candidato e apuração de votos nulos.
- **Interface Visual no Terminal:** Menu interativo para votação, inspeção de blocos, auditoria e apuração.

---

## 📁 Estrutura do Projeto

```text
urna-livre/
├── data/
│   └── blockchain.txt           # Dados da blockchain criptografados em disco
├── src/
│   ├── armazenar_e_carregar.py  # Criptografia Fernet e persistência dos blocos
│   ├── auditoria.py             # Verificação de integridade e apuração dos votos
│   ├── computar_voto.py         # Registro e cálculo de hash de cada voto
│   ├── gerar_bloco_genese.py    # Geração do bloco inicial (Gênesis)
│   └── gerar_chave.py           # Geração da chave Fernet no arquivo .env
├── teste/
│   └── simular_testes.py        # Suíte de simulação de todos os cenários de teste
├── .env                         # Chave simétrica da blockchain
├── main.py                      # Ponto de entrada com menu visual e interativo
└── README.md
```

---

## 🛠️ Pré-requisitos

- **Python 3.10+** instalado
- Dependências:
  - `cryptography`
  - `python-dotenv`

---

## ⚙️ Instalação e Configuração

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/marco-rocks/urna-livre.git
   cd urna-livre
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   # Windows
   python -m venv .venv
   .\.venv\Scripts\activate

   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install cryptography python-dotenv
   ```

4. **Gere a chave de criptografia (.env):**
   ```bash
   python src/gerar_chave.py
   ```

---

## ▶️ Como Executar

Execute o menu interativo:

```bash
python main.py
```

### Opções do Menu:
```text
[1] Votar                              -> Registro de voto anônimo e encadeamento do bloco
[2] Visualizar Livro-Razão (Blockchain)-> Desenho visual de todos os blocos e elos
[3] Auditar Integridade da Blockchain  -> Verificação completa contra adulterações
[4] Apurar Resultado da Eleição        -> Contagem e resultado oficial
[0] Sair                               -> Encerra o sistema
```

---

## 🧪 Executando os Testes / Simulações

Para simular todos os cenários (votação normal, detecção de fraude, quebra de hash, voto duplo e persistência):

```bash
python teste/simular_testes.py
```

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais e de estudo sobre Blockchain e Criptografia. Sinta-se livre para utilizar e expandir!
