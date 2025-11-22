from flask import Blueprint, redirect, render_template, request, url_for
from conn import conexao
from flask import session

lote = Blueprint('lote', __name__)

# Listar lotes
@lote.route("/lotes")
def lotes():
    if session.get('usuario'):
        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM LOTE")
            lotes = cursor.fetchall()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return render_template("lotes.html", lotes=lotes)
    else:
        return redirect(url_for('log.login'))


# Cadastrar lote
@lote.route("/cadastrar-lote", methods=["POST"])
def cadastrarlote():
    if session.get('usuario'):
        idproduto = request.form.get("idproduto")
        idfornecedor = request.form.get("idfornecedor")
        datacadastro = request.form.get("datacadastro")
        datavalidade = request.form.get("datavalidade")
        numero = request.form.get("numero")
        quantidade = request.form.get("quantidade")

        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                INSERT INTO LOTE (IDPRODUTO, IDFORNECEDOR, DATA_CADASTRO, DATA_VALIDADE, NUMERO, QUANTIDADE)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (idproduto, idfornecedor, datacadastro, datavalidade, numero, quantidade))

            conn.commit()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return redirect(url_for('lote.lotes'))
    else:
        return redirect(url_for('log.login'))


# Pesquisar por ID
@lote.route("/pesquisar-lote-id", methods=["POST"])
def pesquisarloteid():
    if session.get('usuario'):
        id = request.form.get("id")

        conn = conexao()
        cursor = None
        
        if conn is None:
            return "Erro ao conectar banco de dados", 500
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM LOTE WHERE IDLOTE = %s", (id,))
            lotes = cursor.fetchall()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return render_template("lotes.html", lotes=lotes)
    else:
        return redirect(url_for('log.login'))


# Pesquisar por produto
@lote.route("/pesquisar-lote-produto", methods=["POST"])
def pesquisarloteproduto():
    if session.get('usuario'):
        idproduto = request.form.get("idproduto")

        conn = conexao()
        cursor = None
        
        if conn is None:
            return "Erro ao conectar banco de dados", 500
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM LOTE WHERE IDPRODUTO = %s", (idproduto,))
            lotes = cursor.fetchall()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return render_template("lotes.html", lotes=lotes)
    else:
        return redirect(url_for('log.login'))


# Pesquisar por fornecedor
@lote.route("/pesquisar-lote-fornecedor", methods=["POST"])
def pesquisarlotefornecedor():
    if session.get('usuario'):
        idfornecedor = request.form.get("idfornecedor")

        conn = conexao()
        cursor = None
        
        if conn is None:
            return "Erro ao conectar banco de dados", 500
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM LOTE WHERE IDFORNECEDOR = %s", (idfornecedor,))
            lotes = cursor.fetchall()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return render_template("lotes.html", lotes=lotes)
    else:
        return redirect(url_for('log.login'))


# Deletar lote
@lote.route("/deletar-lote/<int:id>")
def deletarlote(id):
    if session.get('usuario'):
        conn = conexao()
        cursor = None
        
        if conn is None:
            return "Erro ao conectar banco de dados", 500
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("DELETE FROM LOTE WHERE IDLOTE = %s", (id,))
            conn.commit()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return redirect(url_for('lote.lotes'))
    else:
        return redirect(url_for('log.login'))


# Página de edição
@lote.route("/alterar-lote/<int:id>")
def alterarlote(id):
    if session.get('usuario'):
        conn = conexao()
        cursor = None
        
        if conn is None:
            return "Erro ao conectar banco de dados", 500
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM LOTE WHERE IDLOTE = %s", (id,))
            lote = cursor.fetchone()

            return render_template("alterarLote.html", lote=lote)

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    else:
        return redirect(url_for('log.login'))


# Salvar edição
@lote.route("/alterar-lote/<int:id>", methods=["POST"])
def alterarlote_post(id):
    if session.get('usuario'):
        idproduto = request.form.get("idproduto")
        idfornecedor = request.form.get("idfornecedor")
        datacadastro = request.form.get("datacadastro")
        datavalidade = request.form.get("datavalidade")
        numero = request.form.get("numero")
        quantidade = request.form.get("quantidade")

        conn = conexao()
        cursor = None
        
        if conn is None:
            return "Erro ao conectar banco de dados", 500
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                UPDATE LOTE
                SET IDPRODUTO = %s,
                    IDFORNECEDOR = %s,
                    DATA_CADASTRO = %s,
                    DATA_VALIDADE = %s,
                    NUMERO = %s,
                    QUANTIDADE = %s
                WHERE IDLOTE = %s
            """, (idproduto, idfornecedor, datacadastro, datavalidade, numero, quantidade, id))

            conn.commit()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return redirect(url_for('lote.lotes'))
    else:
        return redirect(url_for('log.login'))
