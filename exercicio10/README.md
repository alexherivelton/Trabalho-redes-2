# Exercício 10 — Chat com WebSockets

## O que faz

- **`servidor.py`**: servidor de chat em Python com a biblioteca `websockets`. Aceita várias conexões ao mesmo tempo e retransmite (**broadcast**) cada mensagem para todos os outros clientes, identificando quem enviou pelo nome. Avisa quando alguém entra ou sai.
- **`cliente.html`**: página web simples que usa a API WebSocket nativa do navegador. O usuário digita o nome, entra no chat, envia e recebe mensagens em tempo real.

Detalhes de implementação:
- o servidor usa `asyncio`: uma única thread atende todos os clientes, e cada cliente é uma corrotina que cede a vez às outras nos `await`. Por isso a lista de clientes não precisa de `Lock`;
- o WebSocket já separa as mensagens, então não é preciso delimitador como no exercício 3;
- desconexões inesperadas (`ConnectionClosedError`) são tratadas: o cliente é removido, os outros são avisados e o servidor continua funcionando;
- a página valida nome e mensagens vazias e avisa se o servidor estiver desligado.

## Dependências

- Python 3.10+
- Biblioteca `websockets` (versão em `requirements.txt`)
- Um navegador atual (Chrome, Edge, Firefox) para o cliente

Instalação (recomendado usar um ambiente virtual):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Como executar

1. Inicie o servidor (com o ambiente virtual ativado):

   ```bash
   python3 servidor.py
   ```

2. Abra o arquivo `cliente.html` no navegador (duplo clique no arquivo, ou arraste para o navegador).
3. Digite um nome e clique em **Entrar**.
4. Digite as mensagens e clique em **Enviar**. Para sair do chat, feche a aba.
5. Para conversar com outras pessoas, abra o `cliente.html` em outras abas ou janelas, cada uma com um nome.

Encerre o servidor com `Ctrl+C`.

### Servidor no WSL2 e navegador no Windows

O WSL2 repassa automaticamente as portas do Linux para o `localhost` do Windows. Então, com o servidor rodando no WSL2, basta abrir o `cliente.html` no navegador do Windows e usar o endereço `ws://localhost:8765`.

Para abrir o arquivo pelo Windows, ele fica acessível no Explorador de Arquivos em `\\wsl$\Ubuntu\` (no caminho onde o repositório foi clonado), ou rode no terminal do WSL, dentro da pasta `exercicio10`:

```bash
explorer.exe cliente.html
```

### Clientes em outro computador

Com o servidor rodando em `0.0.0.0`, outros computadores da mesma rede podem se conectar trocando, no `cliente.html`, a linha `const SERVIDOR = "ws://localhost:8765";` pelo IP do servidor, por exemplo `"ws://192.168.0.10:8765"`.

## Parâmetros

| Script | Parâmetro | Padrão | Descrição |
|---|---|---|---|
| `servidor.py` | `--host` | `0.0.0.0` | Endereço em que o servidor escuta (todas as interfaces) |
| `servidor.py` | `--porta` | `8765` | Porta do servidor WebSocket |
| `cliente.html` | constante `SERVIDOR` | `ws://localhost:8765` | Endereço do servidor (editável no início do script da página) |

## Exemplo de saída

Servidor:
```
[11/11/2026 14:30:00] Servidor WebSocket escutando em ws://0.0.0.0:8765 (Ctrl+C para encerrar)
[11/11/2026 14:30:05] Ana (127.0.0.1:51234) entrou no chat
[11/11/2026 14:30:09] Bruno (127.0.0.1:51240) entrou no chat
[11/11/2026 14:30:15] Ana: Oi, Bruno!
[11/11/2026 14:30:20] Ana (127.0.0.1:51234) saiu do chat
```

Página do Bruno:
```
*** Bem-vindo ao chat, Bruno! ***
Ana: Oi, Bruno!
Você: Oi, Ana!
*** Ana saiu do chat ***
```
