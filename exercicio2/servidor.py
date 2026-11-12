# Trabalho 2 - Redes de Computadores 2 - UFVJM
# Exercício 2: Servidor Echo UDP (servidor)
# Integrantes: Rafael Guimaraes, Álex Herivelton

# Servidor UDP que devolve (eco) cada mensagem recebida para quem a enviou.

import argparse
import socket
from datetime import datetime


def main():
    # Parâmetros da linha de comando
    parser = argparse.ArgumentParser(description="Servidor Echo UDP do Exercício 2")
    parser.add_argument("--host", default="0.0.0.0", help="endereço do servidor (padrão: 0.0.0.0)")
    parser.add_argument("--porta", type=int, default=6000, help="porta do servidor (padrão: 6000)")
    args = parser.parse_args()

    # AF_INET = IPv4, SOCK_DGRAM = UDP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # No UDP só existe o bind: não há listen() nem accept(), porque não há conexão
        servidor.bind((args.host, args.porta))
        print(f"Servidor UDP escutando em {args.host}:{args.porta} (Ctrl+C para encerrar)")

        # O recvfrom() desiste a cada 1 segundo. Assim o Ctrl+C é percebido
        # também no Windows, onde ele não interrompe um recvfrom() parado.
        servidor.settimeout(1)

        while True:
            # recvfrom() espera um datagrama e devolve os dados E o endereço de quem enviou
            try:
                dados, endereco = servidor.recvfrom(65535)
            except socket.timeout:
                continue  # nada chegou neste segundo: volta a esperar

            # Mostra a mensagem com data/hora e o endereço do remetente
            mensagem = dados.decode(errors="replace")
            hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"[{hora}] {endereco[0]}:{endereco[1]} enviou {len(dados)} bytes: {mensagem}")

            # Eco: devolve exatamente os mesmos bytes para o endereço do remetente
            servidor.sendto(dados, endereco)

    except (OSError, OverflowError) as erro:
        # Ex.: porta já em uso ou porta fora do intervalo 0-65535
        print(f"Erro no servidor: {erro}")
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        servidor.close()


if __name__ == "__main__":
    main()
