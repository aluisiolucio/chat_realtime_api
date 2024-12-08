# CHAT REALTIME API

A CHAT REALTIME API é uma aplicação backend desenvolvida com `Python` e `FastAPI` para oferecer um sistema de chat em tempo real com autenticação via JWT, WebSocket para comunicação instantânea e persistência de mensagens em banco de dados. A API foi projetada para ser fácil de usar e segura, oferecendo uma solução para chats entre múltiplos usuários.

## 📋 Especificações

Esta API atende aos seguintes requisitos principais:

1. **Gerenciamento de Usuários e Salas de Chat**:
   - Usuários autenticados podem criar e entrar em salas de chat.
   - Cada sala possui um identificador único.

2. **Comunicação em Tempo Real**:
   - Comunicação por WebSocket para troca de mensagens em tempo real.
   - Suporte a múltiplos usuários conectados à mesma sala.

3. **Histórico de Mensagens**:
   - As mensagens enviadas são armazenadas em um banco de dados relacional.
   - Ao entrar em uma sala, o cliente recebe o histórico de mensagens.

4. **Segurança**:
   - Autenticação e autorização via JWT.
   - Apenas usuários autenticados podem acessar as rotas WebSocket.

## 🚀 Tecnologias Utilizadas

- **Python 3.12+**
- **FastAPI** para criação da API e WebSocket.
- **PostgreSQL** como banco principal.
- **Alembic** para controle de versões do banco de dados.
- **Docker e Docker Compose** para configuração do ambiente.
- **Pytest** para testes.
- **Poetry** para gerenciamento de dependências.

## 🗂️ Estrutura do Projeto

A estrutura do projeto está organizada da seguinte forma:

```
├── chat_realtime_api
│   ├── api
│   │   └── v1
│   │       ├── errors               # Contém manipuladores de erros e exceções
│   │       ├── routers              # Rotas e endpoints da API
│   │       │   ├── rooms.py         # Lógica de rotas para salas de chat
│   │       │   ├── token.py         # Lógica de rotas para token JWT
│   │       │   ├── users.py         # Lógica de rotas para usuários
│   │       │   └── ws               # WebSocket para chat em tempo real
│   │       │       ├── chat.py      # WebSocket para gerenciamento de chat
│   │       └── schemas              # Schemas Pydantic para validação de dados
│   │           ├── history.py       # Schema para histórico de mensagens
│   │           ├── rooms.py         # Schema para sala de chat
│   │           ├── token.py         # Schema para token JWT
│   │           └── users.py         # Schema para usuário
│   ├── app.py                       # Arquivo principal da aplicação FastAPI
│   ├── infra
│   │   ├── config                   # Configurações da aplicação
│   │   │   ├── security.py          # Segurança e autenticação (JWT)
│   │   │   └── settings.py          # Configurações gerais (URLs, chave secreta, etc.)
│   │   ├── db                       # Gerenciamento do banco de dados
│   │   │   └── session.py           # Sessões de conexão com o banco de dados
│   │   ├── models                   # Modelos do banco de dados (SQLAlchemy)
│   │   │   ├── base.py              # Modelo base para herança
│   │   │   ├── messages.py          # Modelo de mensagens
│   │   │   ├── rooms.py             # Modelo de salas de chat
│   │   │   └── users.py             # Modelo de usuários
│   │   └── sqlalchemy_repositories  # Repositórios para interação com o banco de dados
│   │       ├── messages.py          # Repositório para mensagens
│   │       ├── rooms.py             # Repositório para salas de chat
│   │       └── users.py             # Repositório para usuários
│   ├── repositories                 # Repositórios de lógica de negócio
│   │   ├── messages.py              # Lógica para mensagens
│   │   ├── rooms.py                 # Lógica para salas de chat
│   │   └── users.py                 # Lógica para usuários
│   └── services                     # Serviços da aplicação
│       ├── auth                     # Serviços de autenticação
│       │   └── token.py             # Geração e validação de tokens JWT
│       ├── errors                   # Tratamento de erros e exceções
│       │   ├── exceptions.py        # Exceções personalizadas
│       ├── messages                 # Serviços para mensagens
│       │   ├── create.py            # Lógica para criação de mensagens
│       │   ├── get.py               # Lógica para recuperar mensagens
│       ├── rooms                    # Serviços para salas de chat
│       │   ├── create.py            # Lógica para criação de salas
│       │   ├── get_history.py       # Lógica para pegar o histórico de salas
│       │   ├── get.py               # Lógica para obter detalhes de salas
│       └── users                    # Serviços para usuários
│           ├── create.py            # Lógica para criação de usuários
├── docker-compose.yaml              # Arquivo de configuração Docker Compose
├── Dockerfile                       # Arquivo Docker para criação da imagem
├── entrypoint.sh                    # Script para inicializar a aplicação com Docker
├── LICENSE                          # Licença do projeto
├── alembic.ini                      # Arquivo de configuração do Alembic
├── migrations                       # Arquivos de migração do banco de dados
│   ├── env.py                       # Configuração do Alembic
│   ├── README                       # Documentação das migrações
│   ├── script.py.mako               # Template do script de migração
│   └── versions                     # Migrações específicas de versões
├── poetry.lock                      # Arquivo de bloqueio do Poetry
├── pyproject.toml                   # Configurações de dependências do Poetry
├── README.md                        # Documento principal do projeto
└── tests                            # Testes automatizados
    ├── conftest.py                  # Configuração do pytest
    ├── test_rooms.py                # Testes das salas de chat
    ├── test_token.py                # Testes de autenticação
    └── test_users.py                # Testes de usuários
```

## 🛠️ Instalação e Configuração

1. **Clone o Repositório**

   ```bash
   git clone https://github.com/aluisiolucio/chat_realtime_api
   cd chat_realtime_api
   ```

2. **Configuração de Ambiente**

   Copie o arquivo `.env.example` para `.env` e configure as variáveis:

   ```env
   DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<dbname>
   DB_USER=<user>
   DB_PASSWORD=<password>
   DB_NAME=<dbname>
   SECRET_KEY=<sua-chave-secreta>
   ALGORITHM=<Algoritmo para JWT>
   ACCESS_TOKEN_EXPIRE_MINUTES=<Tempo para expiração do token>
   ```

3. **Execução com Docker**

   Certifique-se de ter **Docker** e **Docker Compose** instalados.

   ```bash
   docker compose up --build
   ```

   Isso iniciará os serviços da API e do banco de dados.

## 🔍 Documentação da API

A documentação interativa está acessível via Swagger UI em: `http://localhost:8000/docs`.

### Principais Endpoints

#### **1. WebSocket**
- **Conectar ao WebSocket**
  - **URL:** `ws://localhost:8000/api/v1/chat/{room_id}`
  - **Parâmetros Requeridos:**
    - `room_id` ID da sala
    - `token:` Token JWT no formato `Bearer <token>`
  - **Descrição:** Permite ao cliente conectar-se a uma sala de chat em tempo real.

#### **2. Salas**
- **Criar Sala**
  - **POST /api/v1/rooms**
  - Entrada: JSON com os dados da sala.
  - Saída: Detalhes da sala criada.

- **Obter Todas as Salas Criadas**
  - **GET /api/v1/rooms**
  - Saída: Lista das salas criadas.

- **Obter Histórico de Mensagens**
  - **GET /api/v1/rooms/{room_id}/history**
  - Parâmetros: ID da sala; Página atual (page); Quatidade por página (size)
  - Saída: Detalhes da sala, paginação e lista com histórico de mensagens da sala.

#### **3. Usuários**
- **Criar Usuário**
  - **POST /api/v1/users**
  - Entrada: JSON com nome de usuário, username e senha.

#### **4. Auth**
- **Login**
  - **POST /api/v1/auth/login**
  - Entrada: JSON com username e senha.
  - Saída: Token JWT.

- **Refresh Token**
  - **POST /api/v1/auth/refresh_token**
  - Saída: Token JWT.

## 🧪 Testes

Para executar os testes:

1. **Instale as Dependências**

   Caso ainda não tenha o Poetry instalado, siga as instruções oficiais [aqui](https://python-poetry.org/docs/#installation).

   Instale as dependências:

   ```bash
   poetry install
   ```

2. **Execute os Testes**

   Use o comando:

   ```bash
   poetry run task test
   ```

## 🤝 Contribuição

Contribuições são bem-vindas! Siga os passos descritos abaixo:

1. **Faça um Fork do Repositório**  
   Crie uma cópia do projeto no seu GitHub utilizando o botão "Fork".

2. **Clone o Repositório Forkado**

   ```bash
   git clone https://github.com/aluisiolucio/chat_realtime_api
   cd chat_realtime_api
   ```

3. **Crie uma Branch para suas Alterações**

   ```bash
   git checkout -b feature/sua-funcionalidade
   ```

4. **Faça Alterações no Código e Teste-as**

   Garanta que todos os testes passam:

   ```bash
   poetry run pytest
   ```

5. **Envie Suas Alterações**

   ```bash
   git push origin feature/sua-funcionalidade
   ```

6. **Abra um Pull Request**  
   Descreva suas alterações no PR e aguarde revisão.

## ⚖️ Licença

Distribuído sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.