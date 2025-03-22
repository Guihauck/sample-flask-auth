from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key" # Utilizado pelo Flask para proteger as informações armazenadas.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app) # Criação da instância da classe SQLAlchemy (objeto) para conexão ao banco de dados.

@app.route("/hello-world", methods=["GET"])
def hello_world():
  return "Hello World!"

if __name__ == "__main__":
  app.run(debug=True)
