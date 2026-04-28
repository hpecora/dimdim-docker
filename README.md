\# DimDim – API de Clientes com Docker



Projeto do 2º Checkpoint – DevOps Tools \& Cloud Computing – FIAP



\## Integrantes



| RM | Nome |

|--------|------|

| 556612 | Henrique Pecora |

| 98420 | Santhiago |



---



\## Arquitetura



\- \*\*app-556612\*\* → API Python/Flask com CRUD de clientes (porta 5000)

\- \*\*db-556612\*\* → Banco de dados PostgreSQL 16 com volume nomeado (porta 5432)

\- \*\*dimdim-network\*\* → Rede Docker para comunicação entre os containers

\- \*\*dimdim-556612-pgdata\*\* → Volume nomeado para persistência dos dados



---



\## Pré-requisitos



\- Docker Desktop instalado e em execução

\- Git



---



\## Como executar (How-to)



\### 1. Clone o repositório



```bash

git clone https://github.com/hpecora/dimdim-docker.git

cd dimdim-docker

```



\### 2. Suba os containers



```bash

docker compose up -d

```



\### 3. Verifique se está funcionando



```bash

docker ps

docker network ls

docker volume ls

docker image ls

```



\### 4. Teste a API



```bash

curl http://localhost:5000/health

```



---



\## Endpoints da API



| Método | Rota | Descrição |

|--------|------|-----------|

| GET | /health | Health check |

| POST | /clientes | Criar cliente |

| GET | /clientes | Listar clientes |

| GET | /clientes/{id} | Buscar cliente |

| PUT | /clientes/{id} | Atualizar cliente |

| DELETE | /clientes/{id} | Deletar cliente |



---



\## Exemplos de uso (CRUD)



\### CREATE

```bash

curl -X POST http://localhost:5000/clientes -H "Content-Type: application/json" -d "{\"nome\":\"Joao Silva\",\"cpf\":\"111.222.333-44\",\"email\":\"joao@dimdim.com\",\"saldo\":1500.00}"

```



\### READ

```bash

curl http://localhost:5000/clientes

```



\### UPDATE

```bash

curl -X PUT http://localhost:5000/clientes/1 -H "Content-Type: application/json" -d "{\"nome\":\"Joao Silva Atualizado\",\"email\":\"novo@dimdim.com\",\"saldo\":2500.00}"

```



\### DELETE

```bash

curl -X DELETE http://localhost:5000/clientes/1

```



\### Verificar direto no banco

```bash

docker exec -it db-556612 psql -U dimdim -d dimdim -c "SELECT \* FROM clientes;"

```



---



\## Remover tudo



```bash

docker compose down -v

```

