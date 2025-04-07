from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key" # Utilizado pelo Flask para proteger as informações armazenadas.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:gui123@127.0.0.1:3306/flask-crud' # Troca de banco de dados para o mysql utilizando a biblioteca pymysql

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
    if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
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
    hash_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt()) 
    user = User(username=username, password=hash_password, adressemail=adressemail, role='user')
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

  if id_user != current_user.id and current_user.role == 'user':
    return jsonify({"message": "Usuário na operação sem permissão."}), 403
  
  if user and data.get("password"):
    user.password = data.get("password")
    user.adressemail = data.get("adressemail")
    db.session.commit()
    return jsonify({"message": f"Usuário {id_user} atualizado!"})
  
  return jsonify({"message": "Usuário não encontrado!"}),404

@app.route('/user/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user):
  user = User.query.get(id_user)

  if current_user.role != 'admin':
    return jsonify({"message": "Usuário sem permissão de administrador para esta ação."}), 403

  if id_user == current_user.id:
    return jsonify({"message": "Sem permissão para deletar o usuário."}), 403
  
  if user:
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"O usuário {id_user} foi deletado com sucesso."})
  
  return jsonify({"message": "Usuário não encontrado."})

if __name__ == "__main__":
  app.run(debug=True)