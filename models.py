from db import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)


    nome = db.Column(db.String(30), nullable=False)
    senha = db.Column(db.String())