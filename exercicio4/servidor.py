# Trabalho 2 - Redes de Computadores 2 - UFVJM
# Exercício 4: Servidor de Hora com Threads (servidor)
# Integrantes: <NOME 1>, <NOME 2>, <NOME 3>

# Servidor TCP multithread que envia a hora atual (HH:MM:SS) a cada cliente que
# pedir. Mantém um contador thread-safe do total de clientes atendidos, que
# aparece em todas as linhas de log.
#
# Protocolo: o cliente envia "HORA" e o servidor responde com a hora, ex.: "14:30:05".

import argparse
import logging
import socket
import threading
from datetime import datetime

# Contador de clientes atendidos desde que o servidor foi iniciado
contador = 0

# Trava que protege o contador. "contador += 1" são 3 passos (ler, somar, gravar);
# sem a trava, duas threads poderiam ler o mesmo valor e um atendimento se perderia.
trava = threading.Lock()

# Configura o log: cada linha começa com data e hora.
# O módulo logging é seguro para várias threads (as linhas não se misturam).
logging.basicConfig(format="[%(asctime)s] %(message)s", datefmt="%d/%m/%Y %H:%M:%S", level=logging.INFO)


def registrar_atendimento():
    """Soma 1 ao contador de forma segura e devolve o novo total."""
    global contador
    with trava:  # só uma thread por vez entra aqui
        contador += 1
        return contador


def log(texto):
    """Escreve uma linha de log sempre com o total de atendimentos no final."""
    with trava:
        total = contador  # lê o contador também protegido pela trava
    logging.info(f"{texto} | atendimentos: {total}")


def atender_cliente(conexao, endereco):
    """Roda em uma thread separada para cada cliente."""
    cliente = f"{endereco[0]}:{endereco[1]}"

    try:
        # Se o cliente não enviar nada em 10 segundos, desistimos dele
        conexao.settimeout(10)

        pedido = conexao.recv(1024).decode(errors="replace").strip()
        if not pedido:
            log(f"{cliente} desconectou sem fazer solicitação")
            return

        log(f"Solicitação recebida de {cliente}: '{pedido}'")

        # Validação: o único comando aceito é HORA
        if pedido.upper() != "HORA":
            conexao.sendall("ERRO: comando inválido (envie HORA)".encode())
            log(f"Solicitação inválida de {cliente} recusada")
            return

        # Envia a hora no formato HH:MM:SS e conta o atendimento
        hora = datetime.now().strftime("%H:%M:%S")
        conexao.sendall(hora.encode())
        registrar_atendimento()
        log(f"Atendido {cliente}: hora enviada {hora}")

    except Exception as erro:
        # Qualquer falha com ESTE cliente fica só nesta thread:
        # o servidor continua atendendo os outros normalmente.
        log(f"Falha ao atender {cliente}: {erro}")
    finally:
        conexao.close()


def main():
    # Parâmetros da linha de comando
    parser = argparse.ArgumentParser(description="Servidor de hora do Exercício 4")
    parser.add_argument("--host", default="0.0.0.0", help="endereço do servidor (padrão: 0.0.0.0)")
    parser.add_argument("--porta", type=int, default=7000, help="porta do servidor (padrão: 7000)")
    args = parser.parse_args()

    # AF_INET = IPv4, SOCK_STREAM = TCP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permite reusar a porta logo depois de reiniciar o servidor
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        servidor.bind((args.host, args.porta))
        servidor.listen()
        log(f"Servidor de hora escutando em {args.host}:{args.porta} (Ctrl+C para encerrar)")

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
        print()
        log("Servidor encerrado")
    finally:
        servidor.close()


if __name__ == "__main__":
    main()
