# Xbot
bot de raid discord server feito em python.
## Oque o bot tem de especial:
> **Ele coleta logs de uso e envia para um webhook que você define**
> **Ele salva dados de uso, então você passa os dados e então fica salvo pelo seu ID**
> **Você pode personalisar os dados para raid**


# Informações de uso abaixo
# Comando `/dados`

Ao usar o comando `/dados`, informe as seguintes configurações:

> **nome_do_servidor**
> 
> **nome_dos_canais**
> 
> **quantos_canais**
> 
> **bots**

## O que cada opção faz

> **nome_do_servidor**
> 
> O nome informado será usado para renomear o servidor.

> **nome_dos_canais**
> 
> Define o nome-base dos canais que serão criados.
> 
> Exemplo: se você informar `chat`, os canais poderão ser criados como:
> 
> `chat-1`, `chat-2`, `chat-3`.

> **quantos_canais**
> 
> Define quantos canais serão criados.
> 
> Informe um número inteiro, como `5`, `10` ou `20`.

> **bots**
> 
> Define se o bot deverá executar a função relacionada ao gerenciamento de bots.
> 
> - `True` — ativa a função.
> - `False` — desativa a função.

## Exemplo

```text
/dados
nome_do_servidor: Meu Servidor
nome_dos_canais: chat
quantos_canais: 10
bots: False
```