# Exercício 2 — Servidor Echo UDP

## O que faz

- **`servidor.py`**: servidor UDP que recebe mensagens e devolve cada uma de volta para quem enviou (eco). Imprime cada mensagem com data/hora e o endereço `IP:porta` do remetente.
- **`cliente.py`**: envia mensagens ao servidor e mostra o eco recebido, até o usuário digitar `sair`.

Tratamentos implementados:
- mensagens vazias não são enviadas;
- **tamanho máximo de 65.507 bytes**, medido em bytes depois do `encode()` (e não em caracteres, porque letras acentuadas ocupam 2 bytes em UTF-8). O valor vem de 65.535 (pacote IP máximo) − 20 (cabeçalho IP) − 8 (cabeçalho UDP);
- **tempo limite de 3 segundos** para o eco (`socket.settimeout()`): se o servidor estiver desligado ou o datagrama se perder, o cliente avisa e continua funcionando;
- erros de rede e porta inválida tratados sem encerrar o programa com erro.

## Dependências

Apenas Python 3.10+ (biblioteca padrão). Nada para instalar.

## Como executar

Em um terminal, inicie o servidor:

```bash
python3 servidor.py
```

Em outro terminal, inicie o cliente:

```bash
python3 cliente.py
```

Digite mensagens e pressione Enter. Digite `sair` para encerrar o cliente. Encerre o servidor com `Ctrl+C`.

## Parâmetros

| Script | Parâmetro | Padrão | Descrição |
|---|---|---|---|
| `servidor.py` | `--host` | `0.0.0.0` | Endereço em que o servidor escuta (todas as interfaces) |
| `servidor.py` | `--porta` | `6000` | Porta UDP |
| `cliente.py` | `--host` | `127.0.0.1` | Endereço do servidor |
| `cliente.py` | `--porta` | `6000` | Porta UDP do servidor |

## Testes dos limites

Mensagem com exatamente 65.507 bytes (aceita) e com 65.508 bytes (recusada):

```bash
python3 -c "print('x' * 65507)" | python3 cliente.py
python3 -c "print('x' * 65508)" | python3 cliente.py
```

Tempo limite: rode só o cliente, com o servidor desligado, e envie uma mensagem. Depois de 3 segundos aparece `Sem resposta em 3s. O servidor está ligado?`.

## Exemplo de saída

Servidor:
```
Servidor UDP escutando em 0.0.0.0:6000 (Ctrl+C para encerrar)
[11/11/2026 14:30:08] 127.0.0.1:43512 enviou 13 bytes: Olá servidor
```

Cliente:
```
Enviando para 127.0.0.1:6000. Digite 'sair' para encerrar.
Você: Olá servidor
Eco: Olá servidor
Você: sair
Cliente encerrado.
```
