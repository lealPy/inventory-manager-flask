from flask import Blueprint, redirect, render_template, request, url_for
from conn import conexao
from flask import session

cat = Blueprint('cat', __name__)

# Exibir categorias
@cat.route("/categorias")
def categorias():
    if session.get('usuario'):
        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT IDCATEGORIA, NOME FROM CATEGORIA')
            categorias = cursor.fetchall()

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return render_template("categorias.html", categorias=categorias)
    else:
        return redirect(url_for('log.login'))
    

# Cadastrar categoria
@cat.route("/cadastrar-categoria", methods=['POST'])
def cadastrarcategoria():
    if session.get('usuario'):
        nome = request.form.get("nome")
        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM CATEGORIA WHERE NOME = %s', (nome,))
            categorias_existentes = cursor.fetchone()

            if categorias_existentes:
                return redirect(url_for('cat.categorias'))
            else:
                cursor.execute('INSERT INTO CATEGORIA (nome) VALUES (%s)', (nome,))
                conn.commit()

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return redirect(url_for('cat.categorias'))
    else:
        return redirect(url_for('log.login'))


# Pesquisar categoria por ID
@cat.route("/pesquisar-categoria-id", methods=['POST'])
def pesquisarcategoriaid():
    if session.get('usuario'):
        id = request.form.get("id")
        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM CATEGORIA WHERE IDCATEGORIA = %s', (id,))
            categorias = cursor.fetchall()

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return render_template("categorias.html", categorias=categorias)
    else:
        return redirect(url_for('log.login'))


# Pesquisar categoria por nome
@cat.route("/pesquisar-categoria-nome", methods=['POST'])
def pesquisarcategorianome():
    if session.get('usuario'):
        nome = request.form.get("nome")
        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM CATEGORIA WHERE NOME LIKE %s', (f"%{nome}%",))
            categorias = cursor.fetchall()

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return render_template("categorias.html", categorias=categorias)
    else:
        return redirect(url_for('log.login'))


# Deletar categoria
@cat.route("/deletar-categoria/<int:id>")
def deletarcategoria(id):
    if session.get('usuario'):
        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('DELETE FROM CATEGORIA WHERE IDCATEGORIA = %s', (id,))
            conn.commit()

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return redirect(url_for('cat.categorias'))
    else:
        return redirect(url_for('log.login'))
