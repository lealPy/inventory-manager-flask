from flask import Blueprint, redirect, render_template, jsonify, request, url_for, make_response, session
from conn import conexao
from werkzeug.security import check_password_hash

log = Blueprint('log', __name__)

# Página de login
@log.route("/login")
def login():
    return render_template("login.html")

# Autenticação do usuário
@log.route("/login-auth", methods=['POST'])
def loginauth():
    email = request.form.get("email")
    senha = request.form.get("senha")

    conn = conexao()
    cursor = None

    if conn is None:
        return "Erro ao conectar banco de dados", 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM USUARIO WHERE EMAIL = %s", (email,))
        resultado = cursor.fetchone()

        if resultado and check_password_hash(resultado['SENHA'], senha):
            session['usuario'] = resultado['NOME']
            return redirect(url_for('main.paginaprincipal'))
        else:
            return redirect(url_for('log.login'))
        
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
