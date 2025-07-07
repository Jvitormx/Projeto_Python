from .database import get_connection

def inserir_localidade(pais, numero_agencia):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO localidade (pais, numero_agencia)
        VALUES (?, ?)
        """,
        (pais, numero_agencia)
    )
    conn.commit()
    conn.close()

def listar_localidades():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, pais, numero_agencia FROM localidade")
    localidades = cursor.fetchall()
    conn.close()
    return localidades

def buscar_localidade_por_id(localidade_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, pais, numero_agencia FROM localidade WHERE id = ?", (localidade_id,))
    localidade = cursor.fetchone()
    conn.close()
    return localidade

def atualizar_localidade(localidade_id, pais, numero_agencia):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE localidade SET pais = ?, numero_agencia = ?
        WHERE id = ?
        """,
        (pais, numero_agencia, localidade_id)
    )
    conn.commit()
    conn.close()

def remover_localidade(localidade_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM localidade WHERE id = ?", (localidade_id,))
    conn.commit()
    conn.close()
