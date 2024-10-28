import os
from dotenv import load_dotenv

load_dotenv()

class Config: #configs do banco e orm
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://usuario:senha@localhost:5432/nome_do_banco')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'chave ultra secreta')
    JWT_SECRET_KEY = os.getenv('SECRET_KEY', 'chave ultra secreta')
