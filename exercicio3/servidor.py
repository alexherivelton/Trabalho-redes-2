# Trabalho 2 - Redes de Computadores 2 - UFVJM
# Exercício 3: Chat em Rede TCP (servidor)
# Integrantes: <NOME 1>, <NOME 2>, <NOME 3>

# Servidor de chat: cada cliente tem uma thread; as mensagens de um cliente
# são retransmitidas (broadcast) para todos os outros, com o nickname na frente.
#
# Protocolo: cada mensagem é uma linha terminada em '\n'.
# A primeira linha que o cliente envia é o nickname dele.

import argparse
import socket
import threading
from datetime import datetime

# Lista de clientes conectados: {conexao: nickname}
clientes = {}

# Trava que protege o dicionário "clientes", porque várias threads mexem nele
# ao mesmo tempo (uma entrando, outra saindo, outra enviando mensagens)
trava = threading.Lock()


def log(texto):
    """Mostra uma linha no console do servidor com data e hora."""
    hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"[{hora}] {texto}")


def enviar_para_todos(mensagem, exceto=None):
    """Envia a mensagem para todos os clientes conectados, menos para 'exceto'."""
    dados = (mensagem + "\n").encode()
    with trava:  # só uma thread por vez percorre a lista
        for conexao in clientes:
            if conexao is not exceto:
                try:
                    conexao.sendall(dados)
                except OSError:
                    pass  # esse cliente caiu; a thread dele vai removê-lo da lista


def atender_cliente(conexao, endereco):
    """Roda em uma thread separada para cada cliente."""
    cliente = f"{endereco[0]}:{endereco[1]}"
    nickname = None  # ainda não sabemos o nome; ele vem na primeira linha
    buffer = b""     # guarda os bytes recebidos até formar uma linha completa

    try:
        while True:
            dados = conexao.recv(1024)
            if not dados:  # recv vazio = o cliente fechou a conexão
                break

            # O TCP pode juntar ou partir mensagens, então acumulamos tudo no buffer
            # e só tratamos quando aparece um '\n' (fim de uma mensagem)
            buffer += dados
            while b"\n" in buffer:
                linha, buffer = buffer.split(b"\n", 1)  # separa a 1ª linha do resto
                texto = linha.decode(errors="replace").strip()

                if not texto:
                    continue  # ignora linhas vazias

                if nickname is None:
                    # Primeira linha: é o nickname. Adiciona o cliente à lista.
                    nickname = texto
                    with trava:
                        clientes[conexao] = nickname
                    log(f"{nickname} ({cliente}) entrou no chat")
                    conexao.sendall(f"*** Bem-vindo ao chat, {nickname}! ***\n".encode())
                    enviar_para_todos(f"*** {nickname} entrou no chat ***", exceto=conexao)
                else:
                    # Demais linhas: mensagens do chat, enviadas para os outros
                    log(f"{nickname}: {texto}")
                    enviar_para_todos(f"{nickname}: {texto}", exceto=conexao)

    except ConnectionError:
        log(f"A conexão com {cliente} caiu inesperadamente")
    finally:
        # Remove o cliente da lista, mesmo que ele tenha caído de repente
        with trava:
            clientes.pop(conexao, None)
        conexao.close()

        if nickname is not None:
            log(f"{nickname} ({cliente}) saiu do chat")
            enviar_para_todos(f"*** {nickname} saiu do chat ***")


def main():
    # Parâmetros da linha de comando
    parser = argparse.ArgumentParser(description="Servidor de chat TCP do Exercício 3")
    parser.add_argument("--host", default="0.0.0.0", help="endereço do servidor (padrão: 0.0.0.0)")
    parser.add_argument("--porta", type=int, default=5001, help="porta do servidor (padrão: 5001)")
    args = parser.parse_args()

    # AF_INET = IPv4, SOCK_STREAM = TCP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permite reusar a porta logo depois de reiniciar o servidor
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        servidor.bind((args.host, args.porta))
        servidor.listen()
        log(f"Servidor de chat escutando em {args.host}:{args.porta} (Ctrl+C para encerrar)")

        # O accept() desiste a cada 1 segundo, para o Ctrl+C funcionar também no Windows
        servidor.settimeout(1)

        while True:
            try:
                conexao, endereco = servidor.accept()
            except socket.timeout:
                continue  # ninguém conectou neste segundo: volta a esperar

            # Uma thread por cliente; a principal volta a esperar novos clientes
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
