# Trabalho 2 - Redes de Computadores 2 - UFVJM
# Exercício 2: Servidor Echo UDP (cliente)
# Integrantes: <NOME 1>, <NOME 2>, <NOME 3>

# Cliente UDP que envia mensagens ao servidor e mostra o eco, até o usuário digitar "sair".

import argparse
import socket

# Maior mensagem possível em um datagrama UDP sobre IPv4:
# 65535 (tamanho máximo do pacote IP) - 20 (cabeçalho IP) - 8 (cabeçalho UDP) = 65507 bytes
TAMANHO_MAXIMO = 65507

# Tempo máximo (em segundos) esperando o eco do servidor
TEMPO_LIMITE = 3


def main():
    # Parâmetros da linha de comando
    parser = argparse.ArgumentParser(description="Cliente Echo UDP do Exercício 2")
    parser.add_argument("--host", default="127.0.0.1", help="endereço do servidor (padrão: 127.0.0.1)")
    parser.add_argument("--porta", type=int, default=6000, help="porta do servidor (padrão: 6000)")
    args = parser.parse_args()

    # AF_INET = IPv4, SOCK_DGRAM = UDP
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Sem timeout, o recvfrom() esperaria para sempre se o eco nunca chegasse
    cliente.settimeout(TEMPO_LIMITE)

    try:
        print(f"Enviando para {args.host}:{args.porta}. Digite 'sair' para encerrar.")

        while True:
            mensagem = input("Você: ").strip()

            if mensagem.lower() == "sair":
                break

            # Validação: não envia mensagem vazia
            if not mensagem:
                print("Mensagem vazia não é enviada.")
                continue

            # Validação do tamanho: medido em BYTES (depois do encode), não em caracteres.
            # Ex.: "ç" é 1 caractere, mas ocupa 2 bytes em UTF-8.
            dados = mensagem.encode()
            if len(dados) > TAMANHO_MAXIMO:
                print(f"Mensagem muito grande: {len(dados)} bytes (máximo de {TAMANHO_MAXIMO}).")
                continue

            # No UDP não há connect(): cada envio diz para onde vai
            cliente.sendto(dados, (args.host, args.porta))

            try:
                resposta, _ = cliente.recvfrom(65535)  # espera o eco
                print(f"Eco: {resposta.decode(errors='replace')}")
            except socket.timeout:
                # O UDP não avisa se o datagrama se perdeu ou se o servidor está desligado
                print(f"Sem resposta em {TEMPO_LIMITE}s. O servidor está ligado?")
            except ConnectionResetError:
                # No Windows, o aviso de "porta fechada" chega como este erro
                print("O servidor não está ativo nessa porta.")

    except (OSError, OverflowError) as erro:
        # Outros problemas de rede: host inválido, porta inválida...
        print(f"Erro de comunicação: {erro}")
    except (EOFError, KeyboardInterrupt):
        # Ctrl+D ou Ctrl+C: sai sem mostrar erro
        print()
    finally:
        cliente.close()  # sempre fecha o socket, com ou sem erro
        print("Cliente encerrado.")


if __name__ == "__main__":
    main()
