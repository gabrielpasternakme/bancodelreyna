from datetime import date, datetime
from database import conectar

def rotina_diaria():
    hoje = date.today()
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, nome, telefone, ultimo_pagamento, status
        FROM usuarios
        WHERE ativo = 1
    """)

    notificacoes = []

    for id_, nome, telefone, ult_pag, status in cur.fetchall():
        if not ult_pag:
            continue

        ult_pag = datetime.strptime(ult_pag, "%Y-%m-%d").date()
        dias = (hoje - ult_pag).days

        novo_status = status
        deve_notificar = False

        if dias < 30:
            novo_status = "em_dia"

        elif 30 <= dias < 60 and status != "notif_30":
            novo_status = "notif_30"
            deve_notificar = True

        elif 60 <= dias < 90 and status != "notif_60":
            novo_status = "notif_60"
            deve_notificar = True

        elif 90 <= dias < 120 and status != "notif_90":
            novo_status = "notif_90"
            deve_notificar = True

        elif dias >= 120 and status != "bloqueado":
            novo_status = "bloqueado"
            deve_notificar = True
        
        

        if deve_notificar:
            notificacoes.append({
                "nome": nome,
                "telefone": telefone,
                "dias": dias
            })

        if novo_status != status:
            cur.execute(
                "UPDATE usuarios SET status=? WHERE id=?",
                (novo_status, id_)
            )

    conn.commit()
    conn.close()
    return notificacoes
