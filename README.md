# 🧑‍💻 Flask User CRUD API

Este projeto é uma API RESTful desenvolvida com **Flask** que realiza autenticação de usuários com **Flask-Login**, criptografia de senhas com **bcrypt**, e persistência de dados com **SQLAlchemy** conectada a um banco de dados **MySQL**.

---

## 🚀 Funcionalidades

- 🔐 Login e Logout de usuários
- 👤 Criação de novos usuários
- 📄 Leitura de dados de um usuário específico
- ✏️ Atualização de informações do usuário
- ❌ Exclusão de usuários (apenas administradores)

---

## 🧰 Tecnologias Utilizadas

- [Flask](https://flask.palletsprojects.com/)
- [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PyMySQL](https://pymysql.readthedocs.io/en/latest/)
- [bcrypt](https://pypi.org/project/bcrypt/)

---

## ⚙️ Configuração do Ambiente

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/seu-repo.git
   cd seu-repo
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure seu banco de dados MySQL:**

   Certifique-se de ter um banco MySQL rodando e atualize a URI de conexão em `app.config['SQLALCHEMY_DATABASE_URI']`.

5. **Inicialize o banco:**
   ```python
   from app import db
   db.create_all()
   ```

---

## 🔐 Rotas da API

### Login
```http
POST /login
```
**Body:**
```json
{
  "username": "exemplo",
  "password": "senha123",
  "adressemail": "email@exemplo.com"
}
```

### Logout
```http
GET /logout
```
**Requer autenticação**

---

### Criar usuário
```http
POST /user
```
**Body:**
```json
{
  "username": "novo_usuario",
  "password": "senha_segura",
  "adressemail": "email@exemplo.com"
}
```

---

### Obter dados de um usuário
```http
GET /user/<id>
```
**Requer autenticação**

---

### Atualizar usuário
```http
PUT /user/<id>
```
**Requer autenticação**

**Body:**
```json
{
  "password": "nova_senha",
  "adressemail": "novoemail@exemplo.com"
}
```

---

### Deletar usuário
```http
DELETE /user/<id>
```
**Requer autenticação (admin)**

---

## 🔐 Controle de Permissões

- Apenas usuários **autenticados** podem acessar rotas de leitura, atualização e exclusão.
- Apenas **admins** podem deletar usuários.
- Um usuário só pode atualizar suas próprias informações (exceto se for admin).

---

## 📁 Estrutura do Projeto

```
.
├── app.py
├── models/
│   └── user.py
├── database.py
├── requirements.txt
└── README.md
```

---

## 📝 Observações

- Substitua `"your_secret_key"` por uma chave segura no ambiente de produção.
- As senhas são armazenadas com hash utilizando `bcrypt`.
- Para criar um usuário admin, é necessário configurar o atributo `role` como `'admin'` diretamente no banco.
