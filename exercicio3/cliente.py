# Trabalho 2 - Redes de Computadores 2 - UFVJM
# Exercício 3: Chat em Rede TCP (cliente)
# Integrantes: Rafael Guimaraes, Álex Herivelton

# Cliente de chat: uma thread fica recebendo as mensagens dos outros
# enquanto a thread principal lê o que o usuário digita.
#
# Protocolo: cada mensagem é uma linha terminada em '\n'.
# A primeira linha enviada ao servidor é o nickname.

import argparse
import os
import socket
import threading


def receber_mensagens(cliente):
    """Roda em uma thread separada: mostra tudo o que chega do servidor."""
    buffer = b""  # guarda os bytes recebidos até formar uma linha completa
    try:
        while True:
            dados = cliente.recv(1024)
            if not dados:  # recv vazio = o servidor fechou a conexão
                break

            # Acumula no buffer e mostra cada linha completa (terminada em '\n')
            buffer += dados
            while b"\n" in buffer:
                linha, buffer = buffer.split(b"\n", 1)
                print(linha.decode(errors="replace"))
    except OSError:
        pass  # a conexão caiu

    # Se chegou aqui, a conexão com o servidor acabou.
    # A thread principal está parada no input(), então encerramos o programa daqui.
    print("\nA conexão com o servidor foi encerrada.")
    os._exit(0)


def main():
    # Parâmetros da linha de comando
    parser = argparse.ArgumentParser(description="Cliente de chat TCP do Exercício 3")
    parser.add_argument("--host", default="127.0.0.1", help="endereço do servidor (padrão: 127.0.0.1)")
    parser.add_argument("--porta", type=int, default=5001, help="porta do servidor (padrão: 5001)")
    args = parser.parse_args()

    # AF_INET = IPv4, SOCK_STREAM = TCP
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Validação: o nickname não pode ser vazio
        nickname = input("Seu nickname: ").strip()
        while not nickname:
            nickname = input("O nickname não pode ser vazio. Seu nickname: ").strip()

        cliente.connect((args.host, args.porta))

        # A primeira linha enviada é o nickname
        cliente.sendall((nickname + "\n").encode())

        # Thread que fica recebendo mensagens enquanto o usuário digita
        thread = threading.Thread(target=receber_mensagens, args=(cliente,), daemon=True)
        thread.start()

        print("Digite suas mensagens e pressione Enter. Digite 'sair' para sair.")

        while True:
            mensagem = input().strip()

            if mensagem.lower() == "sair":
                break

            if not mensagem:
                continue  # não envia mensagens vazias

            cliente.sendall((mensagem + "\n").encode())  # '\n' marca o fim da mensagem

    except ConnectionRefusedError:
        print("Erro: conexão recusada. O servidor está ligado?")
    except (OSError, OverflowError) as erro:
        print(f"Erro de conexão: {erro}")
    except (EOFError, KeyboardInterrupt):
        print()  # Ctrl+D ou Ctrl+C: sai sem mostrar erro
    finally:
        # Fechar o socket avisa o servidor, que avisa os outros que saímos.
        # Só este cliente é encerrado: o servidor e os outros continuam.
        cliente.close()
        print("Você saiu do chat.")


if __name__ == "__main__":
    main()
