# Exercício 3 — Chat em Rede TCP

## O que faz

- **`servidor.py`**: servidor de chat que aceita vários clientes ao mesmo tempo (sem limite de dois), com **uma thread por cliente**. Cada mensagem recebida é retransmitida (**broadcast**) para todos os outros clientes, precedida do nickname de quem enviou. Avisa a todos quando alguém **entra** ou **sai** do chat.
- **`cliente.py`**: pede um nickname, conecta ao servidor e permite enviar e receber mensagens ao mesmo tempo. Uma **thread separada** fica recebendo as mensagens enquanto a thread principal lê o teclado. Digitar `sair` encerra só esse cliente.

Detalhes de implementação:
- a lista de clientes conectados é protegida por um `threading.Lock`, porque várias threads a acessam ao mesmo tempo;
- o TCP é um fluxo de bytes e pode juntar ou partir mensagens, por isso cada mensagem termina com `\n` e quem recebe junta os bytes em um buffer até encontrar o `\n`;
- quando um cliente sai (com `sair`) ou cai de repente, ele é removido da lista e os outros são avisados; o servidor e os demais clientes continuam funcionando;
- se o servidor for desligado, os clientes avisam e encerram.

## Dependências

Apenas Python 3.10+ (biblioteca padrão). Nada para instalar.

## Como executar

Em um terminal, inicie o servidor:

```bash
python3 servidor.py
```

Em outros terminais (um para cada participante), inicie os clientes:

```bash
python3 cliente.py
```

Cada cliente pede um nickname. Depois é só digitar as mensagens e pressionar Enter. Digite `sair` para sair do chat. Encerre o servidor com `Ctrl+C`.

## Parâmetros

| Script | Parâmetro | Padrão | Descrição |
|---|---|---|---|
| `servidor.py` | `--host` | `0.0.0.0` | Endereço em que o servidor escuta (todas as interfaces) |
| `servidor.py` | `--porta` | `5001` | Porta TCP |
| `cliente.py` | `--host` | `127.0.0.1` | Endereço do servidor |
| `cliente.py` | `--porta` | `5001` | Porta TCP do servidor |

## Exemplo de saída

Servidor:
```
[11/11/2026 14:30:00] Servidor de chat escutando em 0.0.0.0:5001 (Ctrl+C para encerrar)
[11/11/2026 14:30:05] Ana (127.0.0.1:51234) entrou no chat
[11/11/2026 14:30:09] Bruno (127.0.0.1:51240) entrou no chat
[11/11/2026 14:30:15] Ana: Oi, Bruno!
[11/11/2026 14:30:20] Ana (127.0.0.1:51234) saiu do chat
```

Cliente do Bruno:
```
Seu nickname: Bruno
Digite suas mensagens e pressione Enter. Digite 'sair' para sair.
*** Bem-vindo ao chat, Bruno! ***
Ana: Oi, Bruno!
*** Ana saiu do chat ***
```
