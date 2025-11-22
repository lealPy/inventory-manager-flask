from flask import Blueprint, redirect, render_template, request, url_for, session
from conn import conexao

mov = Blueprint('mov', __name__)

# Listar todas as movimentações
@mov.route("/movimentacoes")
def movimentacoes():
    if session.get('usuario'):
        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar ao banco de dados", 500
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM MOVIMENTACAO")
            movimentacoes = cursor.fetchall()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return render_template("movimentacoes.html", movimentacoes=movimentacoes)

    return redirect(url_for('log.login'))


# Cadastrar nova movimentação
@mov.route("/cadastrar-movimentacao", methods=["POST"])
def cadastrarmovimentacao():
    if session.get('usuario'):
        tipo = request.form.get("tipo")
        quantidade = request.form.get("quantidade")
        idlote = request.form.get("idlote")
        data = request.form.get("data")

        conn = conexao()
        cursor = None
        
        if conn is None:
            return "Erro ao conectar ao banco de dados", 500

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                INSERT INTO MOVIMENTACAO (TIPO, QUANTIDADE, IDLOTE, DATA_MOV)
                VALUES (%s, %s, %s, %s)
            """, (tipo, quantidade, idlote, data))
            conn.commit()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return redirect(url_for('mov.movimentacoes'))

    return redirect(url_for('log.login'))


# Pesquisar movimentação pelo ID
@mov.route("/pesquisar-movimentacao-id", methods=["POST"])
def pesquisarmovid():
    if session.get('usuario'):
        idmov = request.form.get("id")

        conn = conexao()
        cursor = None
        
        if conn is None:
            return "Erro ao conectar ao banco de dados", 500

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM MOVIMENTACAO WHERE IDMOVIMENTACAO = %s", (idmov,))
            movimentacoes = cursor.fetchall()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return render_template("movimentacoes.html", movimentacoes=movimentacoes)

    return redirect(url_for('log.login'))


# Pesquisar movimentação pelo tipo
@mov.route("/pesquisar-movimentacao-tipo", methods=["POST"])
def pesquisarmovtipo():
    if session.get('usuario'):
        tipo = request.form.get("tipo")

        conn = conexao()
        cursor = None
        
        if conn is None:
            return "Erro ao conectar ao banco de dados", 500

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM MOVIMENTACAO WHERE TIPO LIKE %s", (f"%{tipo}%",))
            movimentacoes = cursor.fetchall()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return render_template("movimentacoes.html", movimentacoes=movimentacoes)

    return redirect(url_for('log.login'))


# Deletar movimentação
@mov.route("/deletar-movimentacao/<int:id>")
def deletarmovimentacao(id):
    if session.get('usuario'):
        conn = conexao()
        cursor = None
        
        if conn is None:
            return "Erro ao conectar ao banco de dados", 500

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("DELETE FROM MOVIMENTACAO WHERE IDMOVIMENTACAO = %s", (id,))
            conn.commit()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return redirect(url_for('mov.movimentacoes'))

    return redirect(url_for('log.login'))


# Página de edição de movimentação
@mov.route("/alterar-movimentacao/<int:id>")
def alterarmovimentacao(id):
    if session.get('usuario'):
        conn = conexao()
        cursor = None
        
        if conn is None:
            return "Erro ao conectar ao banco de dados", 500

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM MOVIMENTACAO WHERE IDMOVIMENTACAO = %s", (id,))
            mov_data = cursor.fetchone()

            return render_template("alterarMovimentacao.html", mov=mov_data)

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    return redirect(url_for('log.login'))


# Salvar edição da movimentação
@mov.route("/alterar-movimentacao/<int:id>", methods=["POST"])
def alterarmovimentacao_post(id):
    if session.get('usuario'):
        tipo = request.form.get("tipo")
        quantidade = request.form.get("quantidade")
        idlote = request.form.get("idlote")
        data = request.form.get("data")

        conn = conexao()
        cursor = None
        
        if conn is None:
            return "Erro ao conectar ao banco de dados", 500

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                UPDATE MOVIMENTACAO
                SET TIPO = %s, QUANTIDADE = %s, IDLOTE = %s, DATA_MOV = %s
                WHERE IDMOVIMENTACAO = %s
            """, (tipo, quantidade, idlote, data, id))
            conn.commit()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return redirect(url_for('mov.movimentacoes'))

    return redirect(url_for('log.login'))
