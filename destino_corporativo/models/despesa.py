from .database import get_connection

def inserir_despesa(viagem_id, assunto, valor, data, comprovante):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO despesa (viagem_id, assunto, valor, data, comprovante)
        VALUES (?, ?, ?, ?, ?)
        """,
        (viagem_id, assunto, valor, data, comprovante)
    )
    conn.commit()
    conn.close()

def listar_despesas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, viagem_id, assunto, valor, data, comprovante FROM despesa")
    despesas = cursor.fetchall()
    conn.close()
    return despesas

def buscar_despesa_por_id(despesa_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, viagem_id, assunto, valor, data, comprovante FROM despesa WHERE id = ?", (despesa_id,))
    despesa = cursor.fetchone()
    conn.close()
    return despesa

def atualizar_despesa(despesa_id, viagem_id, assunto, valor, data, comprovante):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE despesa SET viagem_id = ?, assunto = ?, valor = ?, data = ?, comprovante = ?
        WHERE id = ?
        """,
        (viagem_id, assunto, valor, data, comprovante, despesa_id)
    )
    conn.commit()
    conn.close()

def remover_despesa(despesa_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM despesa WHERE id = ?", (despesa_id,))
    conn.commit()
    conn.close()
