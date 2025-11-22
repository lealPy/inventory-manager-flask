from flask import Blueprint, redirect, render_template, url_for, session

main = Blueprint('main', __name__)

# Página principal do sistema
@main.route("/paginaprincipal")
def paginaprincipal():
    if session.get('usuario'):
        return render_template("paginaPrincipal.html", usuario=session.get('usuario'))
    return redirect(url_for('log.login'))

# Encerrar sessão e voltar ao login
@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('log.login'))
