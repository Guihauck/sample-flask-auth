from app import db

# Model fornecerá base para o Flask Alchemy reconhecer a classe como algo mapeável.
class User(db.Model): 
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), nullable=False, unique=True)
  passoword = db.Column(db.String(80), nullable=False)
  adressemail = db.Column(db.String(40), nullable=True, unique=True)