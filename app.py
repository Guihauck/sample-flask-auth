from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

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

@app.route('/logout', methods=['GET'])
@login_required # Verifica se o login já está autenticado.
def logout():
  logout_user()
  return jsonify({"message": "Logout realizado com êxito!"})

@app.route('/user', methods=['POST'])
def create_user():
  data = request.json
  username = data.get("username")
  password = data.get("password")
  adressemail = data.get("adressemail")

  if username and password:
    user = User(username=username, password=password, adressemail=adressemail)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Usuário cadastrado com sucesso!"})
  
  return jsonify({"message": "Cadastro incorreto, verifique os dados cadastrados."}),400

@app.route('/user/<int:id_user>', methods=['GET'])
@login_required
def user_read(id_user):
  user =  User.query.get(id_user)

  if user:
    return jsonify({"message": f"username: {user.username} adressemail: {user.adressemail}"})
  
  return jsonify({"message": "Usuário não encontrado!"}), 404

@app.route('/user/<int:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):
  data = request.json
  user = User.query.get(id_user)

  if user and data.get("password"):
    user.password = data.get("password")
    user.adressemail = data.get("adressemail")
    db.session.commit()
    return jsonify({"message": f"Usuário {id_user} atualizado!"})
  
  return jsonify({"message": "Usuário não encontrado!"}),404

@app.route("/hello-world", methods=["GET"])
def hello_world():
  return "Hello World!"

if __name__ == "__main__":
  app.run(debug=True)
