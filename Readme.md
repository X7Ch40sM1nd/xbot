# 🎭 Xbot — Discord Raid Bot

O **Xbot** é um bot de automação e raid para servidores do Discord desenvolvido em Python. Ele possui um sistema inteligente de salvamento de dados por ID de usuário e envio de logs via Webhook.

---

## ✨ O que o bot tem de especial?

* **Logs via Webhook:** Coleta registros de uso do bot e envia em tempo real para um Webhook do Discord definido por você.
* **Persistência de Dados:** Salva as configurações de uso localmente. Uma vez configurado, os dados ficam atrelados ao seu **ID do Discord**, sem necessidade de reconfigurar a cada inicialização.
* **Altamente Personalizável:** Você define o comportamento, nomes e limites da automação diretamente pelos comandos.

---

## 🛠️ Pré-requisitos & Instalação

Escolha o método de instalação dependendo de onde você vai rodar o bot:

### 📱 Método 1: Pelo Android (Termux)
Abra o Termux e execute a sequência de comandos abaixo para instalar as dependências necessárias:
```bash
pkg update && pkg upgrade -y
pkg install python git -y
pip install -r requirements.txt
```

### 💻 Método 2: Pelo Computador (Windows/Linux)
Certifique-se de ter o Python 3.x instalado. Abra o terminal/CMD na pasta do projeto e instale as dependências:
```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuração Inicial

Antes de ligar o bot, você precisa configurar os arquivos de credenciais:

1. **Token do Bot:** Abra o arquivo `.env` e adicione o token do seu bot do Discord:
   ```env
   TOKEN=SEU_TOKEN_DO_BOT_AQUI
   ```

2. **Webhook de Logs:** Abra o arquivo `files/Dados.json` e adicione a URL do seu Webhook do Discord seguindo a estrutura abaixo:
   ```json
   {
     "webhook_discord": "SUA_URL_DO_WEBHOOK_AQUI"
   }
   ```

---

## 🚀 Como Usar

### Iniciando o Bot
Para ligar o bot, execute o comando principal no terminal:
```bash
python bot.py
```

### 🎮 Comandos do Bot
#### `/dados`
Use este comando slash (comando de barra) para definir e salvar as configurações do raid.

| Opção | Tipo | Descrição |
| :--- | :--- | :--- |
| `nome_do_servidor` | Texto | O nome que será usado para renomear o servidor alvo. |
| `nome_dos_canais` | Texto | Define o nome-base dos canais que serão criados (Ex: `chat` gerará `chat-1`, `chat-2`). |
| `quantos_canais` | Número | Quantidade total de canais que o bot deve criar (Ex: `10`, `20`, `50`). |
| `bots` | Boolean | `True` para ativar funções relacionadas ao gerenciamento de bots, `False` para desativar. |

### 📝 Exemplo de Preenchimento:
```text
/dados nome_do_servidor: Meu Servidor nome_dos_canais: chat quantos_canais: 10 bots: False
```

---

## ⚠️ AVISO DE ISENÇÃO DE RESPONSABILIDADE (Disclaimer)
Este bot foi desenvolvido exclusivamente para fins educacionais, testes de estresse autorizados e demonstração de conceitos de programação em Python. **Não** encorajamos, apoiamos ou nos responsabilizamos pelo uso desta ferramenta para atividades maliciosas, assédio ou violação dos Termos de Serviço do Discord. O uso indevido é de total responsabilidade do usuário.
