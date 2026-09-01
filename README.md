# 🔗 CodeLink

### Rede social para estudantes de Análise e Desenvolvimento de Sistemas

O **CodeLink** é uma aplicação web desenvolvida como projeto prático de desenvolvimento Full Stack, com o objetivo de criar um espaço onde estudantes de ADS possam compartilhar conhecimento, publicar conteúdos e interagir com outros estudantes.

O projeto utiliza **FastAPI no backend** e **React no frontend**, com autenticação baseada em JWT e persistência de dados em banco SQLite.

---

## 🚀 Funcionalidades

### 👤 Usuários

* Cadastro de usuários
* Login com autenticação JWT
* Consulta do usuário autenticado
* Perfil público
* Edição do perfil
* Atualização de bio, curso e foto

### 👥 Rede social

* Seguir usuários
* Listar seguidores
* Listar usuários seguidos

### 📝 Publicações

* Criar publicação
* Listar publicações
* Visualizar publicação
* Editar publicação
* Excluir publicação
* Identificação do autor da publicação

---

## 🛠️ Tecnologias

### Backend

* 🐍 Python
* ⚡ FastAPI
* 🗄️ SQLAlchemy
* 🔐 JWT
* 🔑 OAuth2
* 🗃️ SQLite
* 📦 Pydantic

### Frontend

* ⚛️ React
* 🟨 JavaScript
* ⚡ Vite
* 🎨 CSS

### Ferramentas

* Git
* GitHub
* Visual Studio Code

---

## 🏗️ Arquitetura

```text
CodeLink
│
├── backend
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── requirements.txt
│
├── frontend
│   ├── src
│   │   ├── pages
│   │   ├── assets
│   │   ├── App.jsx
│   │   └── ...
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── main.py
```

---

## 🔐 Autenticação

A aplicação utiliza autenticação baseada em **JWT (JSON Web Token)**.

Fluxo:

```text
Usuário
   ↓
Login
   ↓
FastAPI
   ↓
Validação das credenciais
   ↓
JWT
   ↓
Frontend
   ↓
localStorage
   ↓
Rotas protegidas
```

---

## 🔌 Principais endpoints

### Usuários

```text
POST   /usuarios
GET    /usuarios
GET    /usuarios/me
PUT    /usuarios/me
GET    /usuarios/{usuario_id}
```

### Seguidores

```text
POST   /usuarios/{usuario_id}/seguir
GET    /usuarios/{usuario_id}/seguidores
GET    /usuarios/{usuario_id}/seguindo
```

### Posts

```text
POST   /posts
GET    /posts
GET    /posts/{post_id}
PUT    /posts/{post_id}
DELETE /posts/{post_id}
```

### Autenticação

```text
POST /login
```

---

## ⚙️ Como executar

### 1. Clone o projeto

```bash
git clone https://github.com/frankcorreia559-stack/CodeLink.git
```

```bash
cd CodeLink
```

---

# Backend

Entre na pasta:

```bash
cd backend
```

Crie e ative o ambiente virtual:

### Windows

```powershell
python -m venv venv
```

```powershell
.\venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

Execute a API:

```powershell
python -m uvicorn main:app --reload
```

A API estará disponível em:

```text
http://127.0.0.1:8000
```

Documentação Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# Frontend

Abra outro terminal.

Entre na pasta:

```powershell
cd frontend
```

Instale as dependências:

```powershell
npm install
```

Execute o projeto:

```powershell
npm run dev
```

O frontend estará disponível em:

```text
http://localhost:5173
```

---

## 📚 Objetivo do projeto

O CodeLink foi desenvolvido para colocar em prática conceitos de desenvolvimento Full Stack, incluindo:

* Desenvolvimento de APIs REST
* Autenticação e autorização
* Banco de dados
* ORM
* CRUD
* Relacionamentos entre entidades
* Desenvolvimento de interfaces React
* Integração entre frontend e backend
* Controle de versões com Git

---

## 🔮 Próximos passos

* [ ] Sistema de notificações
* [ ] Curtidas nas publicações
* [ ] Comentários
* [ ] Busca de usuários
* [ ] Upload de imagens
* [ ] Sistema de mensagens
* [ ] Melhorias na responsividade
* [ ] Deploy da aplicação
* [ ] Testes automatizados

---

## 👨‍💻 Autor

### Frank Correia

🎓 Estudante de Análise e Desenvolvimento de Sistemas

💻 Desenvolvedor Full Stack em formação

🔗 [GitHub](https://github.com/frankcorreia559-stack)

💼 [LinkedIn](https://www.linkedin.com/in/frank-correia-92bb07417/)

---

⭐ Projeto desenvolvido para estudos e evolução profissional em desenvolvimento Full Stack.
