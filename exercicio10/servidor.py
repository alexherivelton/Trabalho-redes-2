# Trabalho 2 - Redes de Computadores 2 - UFVJM
# Exercício 10: Chat com WebSockets (servidor)
# Integrantes: <NOME 1>, <NOME 2>, <NOME 3>

# Servidor de chat com WebSockets. Cada mensagem recebida de um cliente é
# retransmitida (broadcast) para todos os outros, com o nome de quem enviou.
#
# Protocolo: a primeira mensagem que o cliente envia é o nome dele;
# as demais são mensagens do chat.
#
# Usa asyncio: uma única thread atende todos os clientes. Cada cliente é uma
# "corrotina" que cede a vez para as outras sempre que chega em um "await".

import argparse
import asyncio
from datetime import datetime

import websockets

# Clientes conectados: {websocket: nome}
# Não precisa de Lock: com asyncio só uma corrotina roda por vez, e a troca
# só acontece nos "await" (escalonamento cooperativo, não preemptivo).
clientes = {}


def log(texto):
    """Mostra uma linha no console do servidor com data e hora."""
    hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"[{hora}] {texto}")


async def enviar_para_todos(mensagem, exceto=None):
    """Envia a mensagem para todos os clientes conectados, menos para 'exceto'."""
    # list(...) faz uma cópia: durante o "await" outro cliente pode entrar ou sair
    for websocket in list(clientes):
        if websocket is not exceto:
            try:
                await websocket.send(mensagem)
            except websockets.ConnectionClosed:
                pass  # esse cliente caiu; a corrotina dele vai removê-lo


async def atender_cliente(websocket):
    """Chamada uma vez para cada cliente que se conecta."""
    endereco = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
    nome = None

    try:
        # A primeira mensagem é o nome do usuário
        nome = (await websocket.recv()).strip()
        if not nome:
            await websocket.send("Erro: o nome não pode ser vazio.")
            return

        clientes[websocket] = nome
        log(f"{nome} ({endereco}) entrou no chat")
        await websocket.send(f"*** Bem-vindo ao chat, {nome}! ***")
        await enviar_para_todos(f"*** {nome} entrou no chat ***", exceto=websocket)

        # Cada volta do laço espera a próxima mensagem deste cliente.
        # O laço termina sozinho quando o cliente fecha a conexão normalmente.
        async for mensagem in websocket:
            texto = mensagem.strip()
            if not texto:
                continue  # ignora mensagens vazias
            log(f"{nome}: {texto}")
            await enviar_para_todos(f"{nome}: {texto}", exceto=websocket)

    except websockets.ConnectionClosedError:
        # Desconexão inesperada (aba fechada à força, rede caiu...):
        # afeta só este cliente, o servidor continua funcionando
        log(f"A conexão com {nome or endereco} caiu inesperadamente")
    except websockets.ConnectionClosedOK:
        pass  # o cliente fechou normalmente antes de enviar o nome
    finally:
        # Remove o cliente da lista e avisa os outros
        if websocket in clientes:
            del clientes[websocket]
            log(f"{nome} ({endereco}) saiu do chat")
            await enviar_para_todos(f"*** {nome} saiu do chat ***")


async def iniciar_servidor(host, porta):
    """Inicia o servidor WebSocket e o mantém rodando para sempre."""
    async with websockets.serve(atender_cliente, host, porta):
        log(f"Servidor WebSocket escutando em ws://{host}:{porta} (Ctrl+C para encerrar)")
        await asyncio.Future()  # um "await" que nunca termina: mantém o servidor ligado


def main():
    # Parâmetros da linha de comando
    parser = argparse.ArgumentParser(description="Servidor de chat WebSocket do Exercício 10")
    parser.add_argument("--host", default="0.0.0.0", help="endereço do servidor (padrão: 0.0.0.0)")
    parser.add_argument("--porta", type=int, default=8765, help="porta do servidor (padrão: 8765)")
    args = parser.parse_args()

    try:
        # asyncio.run() inicia o "laço de eventos", que alterna entre as corrotinas
        asyncio.run(iniciar_servidor(args.host, args.porta))
    except (OSError, OverflowError) as erro:
        # Ex.: porta já em uso ou porta fora do intervalo 0-65535
        print(f"Erro no servidor: {erro}")
    except KeyboardInterrupt:
        print("\nServidor encerrado.")


if __name__ == "__main__":
    main()
