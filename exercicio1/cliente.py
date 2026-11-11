# Trabalho 2 - Redes de Computadores 2 - UFVJM
# Exercício 1: Cliente-Servidor TCP (cliente)
# Integrantes: <NOME 1>, <NOME 2>, <NOME 3>

# Cliente TCP que envia mensagens ao servidor até o usuário digitar "sair".

import argparse
import socket


def main():
    # Parâmetros da linha de comando
    parser = argparse.ArgumentParser(description="Cliente TCP do Exercício 1")
    parser.add_argument("--host", default="127.0.0.1", help="endereço do servidor (padrão: 127.0.0.1)")
    parser.add_argument("--porta", type=int, default=5000, help="porta do servidor (padrão: 5000)")
    args = parser.parse_args()

    # AF_INET = IPv4, SOCK_STREAM = TCP
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente.connect((args.host, args.porta))
        print(f"Conectado a {args.host}:{args.porta}. Digite 'sair' para encerrar.")

        while True:
            mensagem = input("Você: ").strip()

            if mensagem.lower() == "sair":
                break

            # Validação: não envia mensagem vazia
            if not mensagem:
                print("Mensagem vazia não é enviada.")
                continue

            # Validação: o servidor lê no máximo 1024 bytes por vez
            if len(mensagem.encode()) > 1024:
                print("Mensagem muito longa (máximo de 1024 bytes).")
                continue

            cliente.sendall(mensagem.encode())  # envia a mensagem em bytes
            resposta = cliente.recv(1024)       # espera a resposta do servidor

            if not resposta:  # resposta vazia = o servidor fechou a conexão
                print("O servidor encerrou a conexão.")
                break
            print(f"Servidor: {resposta.decode()}")

    except ConnectionRefusedError:
        # Ninguém está escutando nessa porta (servidor desligado)
        print("Erro: conexão recusada. O servidor está ligado?")
    except (OSError, OverflowError) as erro:
        # Outros problemas de rede: host inválido, conexão perdida, porta inválida...
        print(f"Erro de conexão: {erro}")
    except (EOFError, KeyboardInterrupt):
        # Ctrl+D ou Ctrl+C: sai sem mostrar erro
        print()
    finally:
        cliente.close()  # sempre fecha a conexão, com ou sem erro
        print("Conexão encerrada.")


if __name__ == "__main__":
    main()
