from .database import get_connection

def inserir_tipo_viagem(motivo, quant_pessoal_max_estimado, duracao_dias_max_estimado, motivo_base, programacao_base):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO tipo_viagem (motivo, quant_pessoal_max_estimado, duracao_dias_max_estimado, motivo_base, programacao_base)
        VALUES (?, ?, ?, ?, ?)
        """,
        (motivo, quant_pessoal_max_estimado, duracao_dias_max_estimado, motivo_base, programacao_base)
    )
    conn.commit()
    conn.close()

def listar_tipos_viagem():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, motivo, quant_pessoal_max_estimado, duracao_dias_max_estimado, motivo_base, programacao_base FROM tipo_viagem")
    tipos = cursor.fetchall()
    conn.close()
    return tipos

def buscar_tipo_viagem_por_id(tipo_viagem_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, motivo, quant_pessoal_max_estimado, duracao_dias_max_estimado, motivo_base, programacao_base FROM tipo_viagem WHERE id = ?", (tipo_viagem_id,))
    tipo = cursor.fetchone()
    conn.close()
    return tipo

def atualizar_tipo_viagem(tipo_viagem_id, motivo, quant_pessoal_max_estimado, duracao_dias_max_estimado, motivo_base, programacao_base):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE tipo_viagem SET motivo = ?, quant_pessoal_max_estimado = ?, duracao_dias_max_estimado = ?, motivo_base = ?, programacao_base = ?
        WHERE id = ?
        """,
        (motivo, quant_pessoal_max_estimado, duracao_dias_max_estimado, motivo_base, programacao_base, tipo_viagem_id)
    )
    conn.commit()
    conn.close()

def remover_tipo_viagem(tipo_viagem_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tipo_viagem WHERE id = ?", (tipo_viagem_id,))
    conn.commit()
    conn.close()
