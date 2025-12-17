import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "usuarios.db")

def conectar():
    return sqlite3.connect(DB_PATH)

def criar_tabela():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT,
            ultimo_pagamento DATE,
            status TEXT NOT NULL,
            ativo INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

def listar_usuarios():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, nome, email, telefone, status, ultimo_pagamento
        FROM usuarios
        WHERE ativo = 1
        ORDER BY id
    """)
    dados = cur.fetchall()
    conn.close()
    return dados   # ← sem isso n aparece nada


def adicionar_usuario(nome, email, telefone, ultimo_pag):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO usuarios (nome, email, telefone, ultimo_pagamento, status)
        VALUES (?, ?, ?, ?, 'em_dia')
    """, (nome, email, telefone, ultimo_pag))
    conn.commit()
    conn.close()

def modificar_usuario(id_, email, telefone, pagamento):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        UPDATE usuarios
        SET email=?, telefone=?, ultimo_pagamento=?
        WHERE id=?
    """, (email, telefone, pagamento, id_))
    conn.commit()
    conn.close()

def apagar_usuario(id_):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("UPDATE usuarios SET ativo=0 WHERE id=?", (id_,))
    conn.commit()
    conn.close()

def registrar_pagamento(id_, hoje):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        UPDATE usuarios
        SET ultimo_pagamento=?, status='em_dia'
        WHERE id=?
    """, (hoje, id_))
    conn.commit()
    conn.close()
