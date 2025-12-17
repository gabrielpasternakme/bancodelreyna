from flask import Flask, render_template, request, redirect
from database import *
from rotina import rotina_diaria
from datetime import date

app = Flask(__name__)
from database import criar_tabela
criar_tabela()

@app.route("/")
def home():
    usuarios = listar_usuarios()
    return render_template("index.html", usuarios=usuarios)


@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    if request.method == "POST":
        adicionar_usuario(
            request.form["nome"],
            request.form["email"],
            request.form["telefone"],
            request.form["ultimo_pagamento"]
        )
        return redirect("/")
    return render_template("adicionar.html")

@app.route("/rotina")
def rotina():
    notificacoes = rotina_diaria()
    return render_template("notificacoes.html", notificacoes=notificacoes)



def buscar_usuario(id_):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, nome, email, telefone, ultimo_pagamento
        FROM usuarios
        WHERE id = ?
    """, (id_,))
    u = cur.fetchone()
    conn.close()
    return u
@app.route("/editar/<int:id_>", methods=["GET", "POST"])
def editar(id_):
    if request.method == "POST":
        modificar_usuario(
            id_,
            request.form["email"],
            request.form["telefone"],
            request.form["ultimo_pagamento"]
        )
        return redirect("/")

    usuario = buscar_usuario(id_)
    return render_template("editar.html", u=usuario)

@app.route("/deletar/<int:id_>")
def deletar(id_):
    apagar_usuario(id_)
    return redirect("/")

from datetime import date

@app.route("/pagar/<int:id>")
def registrar_pagamento(id):
    conn = conectar()
    cursor = conn.cursor()
    hoje = date.today().isoformat()
    cursor.execute("""
        UPDATE usuarios
        SET status = 'em_dia',
            ultimo_pagamento = ?
        WHERE id = ?
    """, (hoje, id))
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    app.run()

