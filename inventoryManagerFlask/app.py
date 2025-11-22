from flask import Flask
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


# Importa rotas (blueprints)
from routes.loginRotas import log
from routes.criarContaRotas import acc
from routes.paginaPrincipalRotas import main
from routes.categoriaRotas import cat
from routes.produtosRotas import pro
from routes.fornecedoresRotas import forn
from routes.loteRotas import lote
from routes.movimentacaoRotas import mov

# Cria a aplicação Flask
app = Flask(__name__)

# Gera chave secreta para sessões
app.secret_key = os.getenv("SECRET_TOKEN")

# Registra todas as rotas (blueprints)
app.register_blueprint(acc)
app.register_blueprint(log)
app.register_blueprint(main)
app.register_blueprint(cat)
app.register_blueprint(pro)
app.register_blueprint(forn)
app.register_blueprint(lote)
app.register_blueprint(mov)

# Inicia o servidor em modo debug
if __name__ == "__main__":
    app.run(debug=True)
