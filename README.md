# 📚 MADR

Projeto final do curso **FastAPI do Zero**
🔗 Curso: [https://fastapidozero.dunossauro.com](https://fastapidozero.dunossauro.com)

---

## 🧠 Sobre o projeto

O **MADR** é uma API REST desenvolvida em **FastAPI** para gerenciar:

* 👤 Contas de usuários (autenticação e autorização)
* 📖 Livros
* ✍️ Romancistas

O projeto foi criado como um exercício prático final para consolidar os conceitos abordados no curso, incluindo:

* FastAPI
* Pydantic
* JWT
* SQLAlchemy ORM
* Testes com Pytest
* Containers
* Boas práticas de APIs REST

---

## 🏗️ Arquitetura geral

A API é dividida em **três routers principais**:

```
/conta        → gerenciamento de usuários e autenticação
/livro        → gerenciamento de livros
/romancista   → gerenciamento de romancistas
```

### Principais decisões técnicas

| Tema               | Escolha          |
| ------------------ | ---------------- |
| Linguagem          | Python 3.13+     |
| Framework          | FastAPI          |
| ORM                | SQLAlchemy       |
| Banco de dados     | SQLite/PostgreSQL|
| Autenticação       | JWT (HS256)      |
| Expiração do token | 60 minutos       |
| Containers         | Docker           |
| Testes             | Pytest           |
| Configuração       | `pyproject.toml` |

---

## 🔐 Autenticação

* Autenticação via **JWT Bearer Token**
* O `subject (sub)` do token é o **email**
* Algoritmo: **HS256**
* Expiração: **60 minutos**
* Endpoints protegidos exigem o header:

```http
Authorization: Bearer <token>
```

---

## 📦 Modelagem do banco de dados

### Entidades

#### User

* `id` (PK)
* `email` (unique)
* `username` (unique)
* `senha` (hash)

#### Romancista

* `id` (PK)
* `nome` (unique)

#### Livro

* `id` (PK)
* `titulo` (unique)
* `ano`
* `romancista_id` (FK → Romancista)

📌 Relacionamento:

* Um **romancista** pode ter **vários livros**
* Um **livro** pertence a **um romancista**

---

## 🚀 Como executar o projeto

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/seu-usuario/madr.git
cd madr
```

### 2️⃣ Configure as variáveis de ambiente

Crie um arquivo `.env`:

```env
POSTGRES_DB=app_db
POSTGRES_USER=app_user
POSTGRES_PASSWORD=app_password
DATABASE_URL=postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
SECRET_KEY=super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 3️⃣ Suba os containers

```bash
docker compose up --build
```

### 4️⃣ Acesse a documentação interativa

* Swagger UI:
  👉 [http://localhost:8000/docs](http://localhost:8000/docs)

* ReDoc:
  👉 [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Executando os testes

O projeto foi desenvolvido com foco em **alta cobertura de testes**.
### Executando tests
```bash
pytest
```
### Executando tests with taskipy
```bash
task test
```

📌 Os testes cobrem:

* Casos de sucesso
* Casos de erro
* Autenticação e autorização
* Conflitos
* Filtros e paginação

---

## 📡 Endpoints principais

### 👤 Contas

| Método | Endpoint         |
| ------ | ---------------- |
| POST   | `/conta`         |
| PUT    | `/conta/{id}`    |
| DELETE | `/conta/{id}`    |
| POST   | `/token`         |
| POST   | `/refresh-token` |

---

### 📖 Livros

| Método | Endpoint              |
| ------ | --------------------- |
| POST   | `/livro`              |
| GET    | `/livro/{id}`         |
| GET    | `/livro?titulo=&ano=` |
| PATCH  | `/livro/{id}`         |
| DELETE | `/livro/{id}`         |

---

### ✍️ Romancistas

| Método | Endpoint            |
| ------ | ------------------- |
| POST   | `/romancista`       |
| GET    | `/romancista/{id}`  |
| GET    | `/romancista?nome=` |
| PATCH  | `/romancista/{id}`  |
| DELETE | `/romancista/{id}`  |

---

## ⚠️ Padrão de erros

### ❌ Autenticação inválida — `400`

```json
{
  "message": "Email ou senha incorretos"
}
```

### 🚫 Não autorizado — `401`

```json
{
  "message": "Não autorizado"
}
```

### 🔍 Não encontrado — `404`

```json
{
  "message": "Livro não consta no MADR"
}
```

```json
{
  "message": "Romancista não consta no MADR"
}
```

### 🔁 Conflito — `409`

```json
{
  "message": "livro já consta no MADR"
}
```

---

## 📚 Aprendizados aplicados

* Arquitetura limpa em FastAPI
* Validação com Pydantic
* Autenticação JWT
* Relacionamentos com SQLAlchemy
* Testes orientados a comportamento
* Boas práticas REST
* Containers e ambientes isolados

---

## 🏁 Considerações finais

Este projeto representa a consolidação prática de tudo que foi ensinado no **FastAPI do Zero**.
O foco foi **clareza, previsibilidade, testes e simplicidade**, evitando funcionalidades fora do escopo do curso.

🎉 Obrigado ao **Dunossauro** e à comunidade pelo excelente conteúdo!

---