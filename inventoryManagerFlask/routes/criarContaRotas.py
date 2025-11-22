from flask import Blueprint, redirect, render_template, request, url_for
from conn import conexao
from werkzeug.security import generate_password_hash

acc = Blueprint('acc', __name__)

# Página de criação de conta
@acc.route("/criarconta")
def criarconta():
    return render_template("criarConta.html")

# Processar criação de conta
@acc.route("/criarconta-auth", methods=['POST'])
def criarcontaauth():
    usuario = request.form.get("usuario")
    email = request.form.get("email")
    senha = request.form.get("senha")
    senha_hash = generate_password_hash(senha)

    conn = conexao()
    cursor = None

    if conn is None:
        return "Erro ao conectar banco de dados", 500
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM USUARIO WHERE NOME = %s AND EMAIL = %s',
            (usuario, email)
        )
        resultado = cursor.fetchone()

        if resultado:
            return redirect(url_for('acc.criarconta'))
        else:
            cursor.execute(
                'INSERT INTO USUARIO (nome, email, senha) VALUES (%s, %s, %s)',
                (usuario, email, senha_hash)
            )
            conn.commit()
            return redirect(url_for('log.login'))
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
