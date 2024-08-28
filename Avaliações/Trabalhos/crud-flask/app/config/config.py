import os
from dotenv import load_dotenv

load_dotenv()

class Config: #confs gerais
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') #URL DO BANCO AQUI

class DevelopmentConfig(Config): # configs para desenvolvimento
    DEBUG = True
    SQLALCHEMY_ECHO = True #ativa logs das consultas SQL
