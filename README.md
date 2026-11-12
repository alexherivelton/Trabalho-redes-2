# Trabalho 2 — Redes de Computadores 2 (UFVJM)

Prof. Alessandro Vivas Andrade

**Integrantes:** Rafael Guimaraes, Álex Herivelton

Programação em redes com sockets TCP/UDP, threads, WebSockets e análise de tráfego com Wireshark.

## Requisitos gerais

- Linux (exercícios 1 a 4 e 10 testados em Ubuntu no WSL2; exercícios 5 a 9 feitos em Ubuntu numa máquina virtual do Oracle VirtualBox)
- Python 3.10 ou superior
- Apenas a biblioteca padrão do Python, exceto no exercício 10 (`websockets`)

## Índice dos exercícios

| Exercício | Tema | Porta padrão |
|---|---|---|
| [exercicio1](exercicio1/) | Cliente-servidor TCP com threads | 5000 |
| [exercicio2](exercicio2/) | Servidor echo UDP | 6000 |
| [exercicio3](exercicio3/) | Chat em rede TCP | 5001 |
| [exercicio4](exercicio4/) | Servidor de hora com threads | 7000 |
| [exercicio5](exercicio5/) | Wireshark — HTTP | — |
| [exercicio6](exercicio6/) | Wireshark — conexão TCP (handshake) | — |
| [exercicio7](exercicio7/) | Wireshark — DNS | — |
| [exercicio8](exercicio8/) | Wireshark — ICMP (ping) | — |
| [exercicio9](exercicio9/) | Wireshark — DHCP | — |
| [exercicio10](exercicio10/) | Chat com WebSockets | 8765 |

Cada diretório contém um `README.md` com os comandos exatos para executar. Os exercícios 5 a 9 trazem também a captura do Wireshark (`.pcapng`) e a análise dos pacotes.
