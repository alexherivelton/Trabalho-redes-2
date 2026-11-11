# Exercício 1 — Cliente-Servidor TCP

## O que faz

- **`servidor.py`**: servidor TCP que aceita vários clientes ao mesmo tempo, com **uma thread por conexão**. Para cada mensagem recebida, imprime data/hora e o `IP:porta` do cliente e responde `Mensagem recebida`.
- **`cliente.py`**: conecta ao servidor e envia várias mensagens até o usuário digitar `sair`. Mostra a resposta do servidor a cada envio.

Tratamentos implementados:
- mensagens vazias são rejeitadas (no cliente e também no servidor);
- mensagens acima de 1024 bytes são recusadas no cliente (é o tamanho que o servidor lê por vez);
- conexões sempre fechadas com segurança usando `try/finally`;
- conexão recusada (servidor desligado) e outros erros de rede tratados no cliente;
- queda inesperada de um cliente não afeta o servidor nem os outros clientes.

## Dependências

Apenas Python 3.10+ (biblioteca padrão). Nada para instalar.

## Como executar

Em um terminal, inicie o servidor:

```bash
python3 servidor.py
```

Em outro terminal (ou vários, para testar clientes simultâneos), inicie o cliente:

```bash
python3 cliente.py
```

Digite mensagens e pressione Enter. Digite `sair` para encerrar o cliente. Encerre o servidor com `Ctrl+C`.

## Parâmetros

| Script | Parâmetro | Padrão | Descrição |
|---|---|---|---|
| `servidor.py` | `--host` | `0.0.0.0` | Endereço em que o servidor escuta (todas as interfaces) |
| `servidor.py` | `--porta` | `5000` | Porta TCP |
| `cliente.py` | `--host` | `127.0.0.1` | Endereço do servidor |
| `cliente.py` | `--porta` | `5000` | Porta TCP do servidor |

Exemplo com outra porta:

```bash
python3 servidor.py --porta 5050
python3 cliente.py --host 127.0.0.1 --porta 5050
```

## Exemplo de saída

Servidor:
```
Servidor escutando em 0.0.0.0:5000 (Ctrl+C para encerrar)
Cliente conectado: 127.0.0.1:51234
[11/11/2026 14:30:08] 127.0.0.1:51234: Olá servidor
Cliente desconectado: 127.0.0.1:51234
```

Cliente:
```
Conectado a 127.0.0.1:5000. Digite 'sair' para encerrar.
Você: Olá servidor
Servidor: Mensagem recebida
Você: sair
Conexão encerrada.
```
