from flask import Blueprint, redirect, render_template, request, url_for, session
from conn import conexao

forn = Blueprint('forn', __name__)

# Exibir fornecedores
@forn.route("/fornecedores")
def fornecedores():
    if session.get('usuario'):
        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM FORNECEDOR")
            fornecedores = cursor.fetchall()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return render_template("fornecedores.html", fornecedores=fornecedores)
    else:
        return redirect(url_for('log.login'))


# Cadastrar fornecedor
@forn.route("/cadastrar-fornecedor", methods=["POST"])
def cadastrarfornecedor():
    if session.get('usuario'):
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        email = request.form.get("email")

        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500

        try:
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM FORNECEDOR WHERE NOME = %s", (nome,))
            fornecedor_existente = cursor.fetchone()

            if fornecedor_existente:
                return redirect(url_for('forn.fornecedores'))

            cursor.execute("""
                INSERT INTO FORNECEDOR (nome, telefone, email)
                VALUES (%s, %s, %s)
            """, (nome, telefone, email))
            conn.commit()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return redirect(url_for('forn.fornecedores'))
    else:
        return redirect(url_for('log.login'))


# Pesquisar fornecedor por ID
@forn.route("/pesquisar-fornecedor-id", methods=["POST"])
def pesquisarfornecedorid():
    if session.get('usuario'):
        id = request.form.get("id")

        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM FORNECEDOR WHERE IDFORNECEDOR = %s", (id,))
            fornecedores = cursor.fetchall()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return render_template("fornecedores.html", fornecedores=fornecedores)
    else:
        return redirect(url_for('log.login'))


# Pesquisar fornecedor por nome
@forn.route("/pesquisar-fornecedor-nome", methods=["POST"])
def pesquisarfornecedornome():
    if session.get('usuario'):
        nome = request.form.get("nome")

        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM FORNECEDOR WHERE NOME LIKE %s", (f"%{nome}%",))
            fornecedores = cursor.fetchall()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return render_template("fornecedores.html", fornecedores=fornecedores)
    else:
        return redirect(url_for('log.login'))


# Deletar fornecedor
@forn.route("/deletar-fornecedor/<int:id>")
def deletarfornecedor(id):
    if session.get('usuario'):
        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("DELETE FROM FORNECEDOR WHERE IDFORNECEDOR = %s", (id,))
            conn.commit()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return redirect(url_for('forn.fornecedores'))
    else:
        return redirect(url_for('log.login'))


# Página de alteração
@forn.route("/alterar-fornecedor/<int:id>")
def alterarfornecedor(id):
    if session.get('usuario'):
        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM FORNECEDOR WHERE IDFORNECEDOR = %s", (id,))
            fornecedor = cursor.fetchone()

            return render_template("alterarFornecedor.html", fornecedor=fornecedor)

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    else:
        return redirect(url_for('log.login'))


# Salvar alteração do fornecedor
@forn.route("/alterar-fornecedor/<int:id>", methods=["POST"])
def alterarfornecedor_post(id):
    if session.get('usuario'):
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        email = request.form.get("email")

        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                UPDATE FORNECEDOR
                SET nome = %s, telefone = %s, email = %s
                WHERE IDFORNECEDOR = %s
            """, (nome, telefone, email, id))
            conn.commit()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return redirect(url_for('forn.fornecedores'))
    else:
        return redirect(url_for('log.login'))
