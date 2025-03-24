from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key" # Utilizado pelo Flask para proteger as informações armazenadas.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases.db'

login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app) # Importa o db do arquivo database e inicia a variável app onde estão as configurações do banco.
login_manager.login_view = 'login' # Utilizar rota de login.

@login_manager.user_loader # Permite recuperar o objeto cadastrado no banco de dados.
def load_user(user_id):
  return User.query.get(user_id)

@app.route('/login', methods=["POST"]) # Método POST para segurança das informações. 
def login():
  data = request.json # Recuperação das informações
  username = data.get("username") # Adicionar login em 'data' para o request
  password = data.get("password") # Adicionar senha
  adressemail = data.get("adressemail")

  if username and password:
    user = User.query.filter_by(username=username).first() # Busca do username e user vai conter todas as informações do usuário.
    if user and user.password == password:
      login_user(user)
      print(current_user.is_authenticated)
      return jsonify({"message":"autenticação realizada com sucesso!"})
    
  return jsonify({"message":"Desculpe, não autenticado, login ou senha incorretos!"}), 400

@app.route("/hello-world", methods=["GET"])
def hello_world():
  return "Hello World!"

if __name__ == "__main__":
  app.run(debug=True)
