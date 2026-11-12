# Trabalho 2 - Redes de Computadores 2 - UFVJM
# Exercício 1: Cliente-Servidor TCP (servidor)
# Integrantes: Rafael Guimaraes, Álex Herivelton

# Servidor TCP que atende vários clientes ao mesmo tempo (uma thread por cliente).

import argparse
import socket
import threading
from datetime import datetime


def atender_cliente(conexao, endereco):
    """Roda em uma thread separada e conversa com um único cliente."""
    cliente = f"{endereco[0]}:{endereco[1]}"  # texto no formato IP:porta
    print(f"Cliente conectado: {cliente}")

    try:
        while True:
            dados = conexao.recv(1024)  # espera até 1024 bytes do cliente
            if not dados:               # recv vazio = o cliente fechou a conexão
                break

            # Converte os bytes em texto (errors="replace" evita erro com bytes inválidos)
            mensagem = dados.decode(errors="replace").strip()

            # Validação: mensagem vazia não é aceita
            if not mensagem:
                conexao.sendall("Erro: mensagem vazia".encode())
                continue

            # Mostra a mensagem com data/hora e IP:porta do cliente
            hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"[{hora}] {cliente}: {mensagem}")

            # Responde ao cliente confirmando o recebimento
            conexao.sendall("Mensagem recebida".encode())

    except ConnectionError:
        # O cliente caiu de repente; só esta thread é afetada
        print(f"A conexão com {cliente} caiu inesperadamente")
    finally:
        conexao.close()  # sempre fecha a conexão, com ou sem erro
        print(f"Cliente desconectado: {cliente}")


def main():
    # Parâmetros da linha de comando
    parser = argparse.ArgumentParser(description="Servidor TCP do Exercício 1")
    parser.add_argument("--host", default="0.0.0.0", help="endereço do servidor (padrão: 0.0.0.0)")
    parser.add_argument("--porta", type=int, default=5000, help="porta do servidor (padrão: 5000)")
    args = parser.parse_args()

    # AF_INET = IPv4, SOCK_STREAM = TCP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permite reusar a porta logo depois de reiniciar o servidor
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        servidor.bind((args.host, args.porta))
        servidor.listen()
        print(f"Servidor escutando em {args.host}:{args.porta} (Ctrl+C para encerrar)")

        # O accept() desiste a cada 1 segundo. Assim o Ctrl+C é percebido
        servidor.settimeout(1)

        while True:
            # accept() espera um cliente e devolve uma conexão só para ele
            try:
                conexao, endereco = servidor.accept()
            except socket.timeout:
                continue  # ninguém conectou neste segundo: volta a esperar

            # Cria uma thread para esse cliente; a principal volta a esperar outros
            thread = threading.Thread(target=atender_cliente, args=(conexao, endereco), daemon=True)
            thread.start()

    except (OSError, OverflowError) as erro:
        # Ex.: porta já em uso ou porta fora do intervalo 0-65535
        print(f"Erro no servidor: {erro}")
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        servidor.close()


if __name__ == "__main__":
    main()
