from flask import Blueprint, redirect, render_template, request, url_for, session
from conn import conexao

# Rotas relacionadas a produtos
pro = Blueprint('pro', __name__)

# Listar todos os produtos
@pro.route("/produtos")
def produtos():
    if session.get('usuario'):
        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('select * from PRODUTO')
            produtos = cursor.fetchall()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return render_template("produtos.html", produtos=produtos)

    return redirect(url_for('log.login'))


# Cadastrar novo produto
@pro.route("/cadastrar-produtos", methods=['POST'])
def cadastrarproduto():
    if session.get('usuario'):
        nome = request.form.get("nome")
        idcategoria = request.form.get("idcategoria")
        descricao = request.form.get("descricao")
        controlevalidade = request.form.get("controlevalidade")
        estoqueminimo = request.form.get("estoqueminimo")

        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('select * from PRODUTO where NOME = %s', (nome,))
            produtos_existentes = cursor.fetchone()

            if produtos_existentes:
                return redirect(url_for('pro.produtos'))

            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                'insert into PRODUTO (idcategoria, nome, descricao, controle_validade, estoque_minimo) values (%s, %s, %s, %s, %s)',
                (idcategoria, nome, descricao, controlevalidade, estoqueminimo)
            )
            conn.commit()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return redirect(url_for('pro.produtos'))

    return redirect(url_for('log.login'))


# Pesquisar produto pelo ID
@pro.route("/pesquisar-produto-id", methods=['POST'])
def pesquisarprodutoid():
    if session.get('usuario'):
        id = request.form.get("id")

        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('select * from PRODUTO where IDPRODUTO = %s', (id,))
            produtos = cursor.fetchall()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return render_template('produtos.html', produtos=produtos)

    return redirect(url_for('log.login'))


# Pesquisar produto pelo nome
@pro.route("/pesquisar-produto-nome", methods=['POST'])
def pesquisarprodutonome():
    if session.get('usuario'):
        nome = request.form.get("nome")

        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('select * from PRODUTO where NOME like %s', (f"%{nome}%",))
            produtos = cursor.fetchall()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return render_template('produtos.html', produtos=produtos)

    return redirect(url_for('log.login'))


# Pesquisar produto pela categoria
@pro.route("/pesquisar-produto-categoria", methods=['POST'])
def pesquisarprodutocategoria():
    if session.get('usuario'):
        idcategoria = request.form.get("idcategoria")

        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('select * from PRODUTO where IDCATEGORIA = %s', (idcategoria,))
            produtos = cursor.fetchall()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return render_template('produtos.html', produtos=produtos)

    return redirect(url_for('log.login'))


# Deletar produto
@pro.route("/deletar-produto/<int:id>")
def deletarproduto(id):
    if session.get('usuario'):
        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('delete from PRODUTO where IDPRODUTO = %s', (id,))
            conn.commit()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return redirect(url_for('pro.produtos'))

    return redirect(url_for('log.login'))


# Abrir formulário de edição
@pro.route("/alterar-produto/<int:id>")
def alterarproduto(id):
    if session.get('usuario'):
        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('select * from PRODUTO where IDPRODUTO = %s', (id,))
            produto = cursor.fetchone()

            return render_template('alterarProduto.html', produto=produto)

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    return redirect(url_for('log.login'))


# Salvar alterações do produto
@pro.route("/alterar-produto/<int:id>", methods=['POST'])
def alterarproduto_post(id):
    if session.get('usuario'):
        nome = request.form.get("nome")
        idcategoria = request.form.get("idcategoria")
        descricao = request.form.get("descricao")
        controlevalidade = request.form.get("controlevalidade")
        estoqueminimo = request.form.get("estoqueminimo")

        conn = conexao()
        cursor = None

        if conn is None:
            return "Erro ao conectar banco de dados", 500
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                'update produto set nome = %s, idcategoria = %s, descricao = %s, controle_validade = %s, estoque_minimo = %s where idproduto = %s',
                (nome, idcategoria, descricao, controlevalidade, estoqueminimo, id)
            )
            conn.commit()

        finally:
            if cursor: cursor.close()
            if conn: conn.close()

        return redirect(url_for('pro.produtos'))

    return redirect(url_for('log.login'))
