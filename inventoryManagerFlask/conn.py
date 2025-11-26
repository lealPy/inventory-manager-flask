import mysql.connector
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def conexao():
    # Abre conexão com o banco de dados MySQL
    conn = mysql.connector.connect(
        host= os.getenv("DB_HOST"),
        user= os.getenv("DB_USER"),
        password= os.getenv("DB_PASSWORD"),
        auth_plugin= os.getenv("DB_AUTH_PLUGIN"),
        database= os.getenv("DB_NAME")
    )

    # Retorna a conexão ativa
    return conn
