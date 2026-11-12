# Trabalho 2 - Redes de Computadores 2 - UFVJM
# Exercício 4: Servidor de Hora com Threads (cliente)
# Integrantes: <NOME 1>, <NOME 2>, <NOME 3>

# Cliente TCP que conecta ao servidor de hora, pede a hora e mostra a resposta.

import argparse
import socket

# Tempo máximo (em segundos) para conectar e para esperar a resposta
TEMPO_LIMITE = 5


def main():
    # Parâmetros da linha de comando
    parser = argparse.ArgumentParser(description="Cliente do servidor de hora do Exercício 4")
    parser.add_argument("--host", default="127.0.0.1", help="endereço do servidor (padrão: 127.0.0.1)")
    parser.add_argument("--porta", type=int, default=7000, help="porta do servidor (padrão: 7000)")
    args = parser.parse_args()

    # AF_INET = IPv4, SOCK_STREAM = TCP
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.settimeout(TEMPO_LIMITE)

    try:
        cliente.connect((args.host, args.porta))

        cliente.sendall("HORA".encode())      # faz a solicitação
        resposta = cliente.recv(1024)         # espera a hora

        if resposta:
            print(f"Hora atual no servidor: {resposta.decode()}")
        else:
            print("O servidor fechou a conexão sem responder.")

    except ConnectionRefusedError:
        # Ninguém está escutando nessa porta (servidor desligado)
        print("Erro: conexão recusada. O servidor está ligado?")
    except socket.timeout:
        print(f"Erro: o servidor não respondeu em {TEMPO_LIMITE} segundos.")
    except (OSError, OverflowError) as erro:
        # Outros problemas de rede: host inválido, conexão perdida, porta inválida...
        print(f"Erro de conexão: {erro}")
    except KeyboardInterrupt:
        print()
    finally:
        cliente.close()  # sempre fecha a conexão, com ou sem erro


if __name__ == "__main__":
    main()
