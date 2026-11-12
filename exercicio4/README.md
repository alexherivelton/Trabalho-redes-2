# Exercício 4 — Servidor de Hora com Threads

## O que faz

- **`servidor.py`**: servidor TCP multithread (uma thread por cliente). Quando recebe a solicitação `HORA`, envia a hora atual no formato `HH:MM:SS`. Mantém um **contador thread-safe** (protegido por `threading.Lock`) do total de clientes atendidos desde que foi iniciado, e esse total aparece **em todas as linhas de log**.
- **`cliente.py`**: conecta ao servidor, pede a hora e mostra a resposta.

Detalhes de implementação:
- o log usa o módulo `logging`, com data/hora em cada linha, e registra cada solicitação recebida e cada atendimento (cliente `IP:porta` e contador);
- `contador += 1` não é uma operação única (lê, soma e grava), por isso é feito dentro de `with trava:`; sem isso, duas threads poderiam ler o mesmo valor e um atendimento seria perdido;
- qualquer falha com um cliente (desconexão, comando inválido, cliente que não envia nada em 10 segundos) é tratada dentro da thread dele, e o servidor continua atendendo os outros;
- o cliente trata servidor desligado e tempo limite de resposta (5 segundos).

## Dependências

Apenas Python 3.10+ (biblioteca padrão). Nada para instalar.

## Como executar

Em um terminal, inicie o servidor:

```bash
python3 servidor.py
```

Em outro terminal, rode o cliente (cada execução faz uma solicitação):

```bash
python3 cliente.py
```

Para simular vários clientes ao mesmo tempo (20 em paralelo):

```bash
for i in $(seq 20); do python3 cliente.py & done; wait
```

Encerre o servidor com `Ctrl+C`.

## Parâmetros

| Script | Parâmetro | Padrão | Descrição |
|---|---|---|---|
| `servidor.py` | `--host` | `0.0.0.0` | Endereço em que o servidor escuta (todas as interfaces) |
| `servidor.py` | `--porta` | `7000` | Porta TCP |
| `cliente.py` | `--host` | `127.0.0.1` | Endereço do servidor |
| `cliente.py` | `--porta` | `7000` | Porta TCP do servidor |

## Exemplo de saída

Servidor:
```
[11/11/2026 14:30:00] Servidor de hora escutando em 0.0.0.0:7000 (Ctrl+C para encerrar) | atendimentos: 0
[11/11/2026 14:30:05] Solicitação recebida de 127.0.0.1:51234: 'HORA' | atendimentos: 0
[11/11/2026 14:30:05] Atendido 127.0.0.1:51234: hora enviada 14:30:05 | atendimentos: 1
[11/11/2026 14:30:09] Solicitação recebida de 127.0.0.1:51240: 'HORA' | atendimentos: 1
[11/11/2026 14:30:09] Atendido 127.0.0.1:51240: hora enviada 14:30:09 | atendimentos: 2
```

Cliente:
```
Hora atual no servidor: 14:30:05
```
