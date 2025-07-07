from .database import get_connection

def inserir_localidade_cidade(cidade, localidade_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO localidade_cidade (cidade, localidade_id)
        VALUES (?, ?)
        """,
        (cidade, localidade_id)
    )
    conn.commit()
    conn.close()

def listar_localidades_cidade():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, cidade, localidade_id FROM localidade_cidade")
    cidades = cursor.fetchall()
    conn.close()
    return cidades

def buscar_localidade_cidade_por_id(localidade_cidade_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, cidade, localidade_id FROM localidade_cidade WHERE id = ?", (localidade_cidade_id,))
    cidade = cursor.fetchone()
    conn.close()
    return cidade

def atualizar_localidade_cidade(localidade_cidade_id, cidade, localidade_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE localidade_cidade SET cidade = ?, localidade_id = ?
        WHERE id = ?
        """,
        (cidade, localidade_id, localidade_cidade_id)
    )
    conn.commit()
    conn.close()

def remover_localidade_cidade(localidade_cidade_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM localidade_cidade WHERE id = ?", (localidade_cidade_id,))
    conn.commit()
    conn.close()
