from .database import get_connection

def inserir_viagem(funcionario_id, tipo_viagem_id, localidade_id, requisicao_id, status, data_saida, data_retorno, duracao_dias, orcamento_aprovado=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO viagem (funcionario_id, tipo_viagem_id, localidade_id, requisicao_id, status, data_saida, data_retorno, duracao_dias, orcamento_aprovado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (funcionario_id, tipo_viagem_id, localidade_id, requisicao_id, status, data_saida, data_retorno, duracao_dias, orcamento_aprovado)
    )
    conn.commit()
    conn.close()

def listar_viagens():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, funcionario_id, tipo_viagem_id, localidade_id, requisicao_id, status, data_saida, data_retorno, duracao_dias, orcamento_aprovado FROM viagem")
    viagens = cursor.fetchall()
    conn.close()
    return viagens

def buscar_viagem_por_id(viagem_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, funcionario_id, tipo_viagem_id, localidade_id, requisicao_id, status, data_saida, data_retorno, duracao_dias, orcamento_aprovado FROM viagem WHERE id = ?", (viagem_id,))
    viagem = cursor.fetchone()
    conn.close()
    return viagem

def atualizar_viagem(viagem_id, funcionario_id, tipo_viagem_id, localidade_id, requisicao_id, status, data_saida, data_retorno, duracao_dias, orcamento_aprovado):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE viagem SET funcionario_id = ?, tipo_viagem_id = ?, localidade_id = ?, requisicao_id = ?, status = ?, data_saida = ?, data_retorno = ?, duracao_dias = ?, orcamento_aprovado = ?
        WHERE id = ?
        """,
        (funcionario_id, tipo_viagem_id, localidade_id, requisicao_id, status, data_saida, data_retorno, duracao_dias, orcamento_aprovado, viagem_id)
    )
    conn.commit()
    conn.close()

def remover_viagem(viagem_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM viagem WHERE id = ?", (viagem_id,))
    conn.commit()
    conn.close()
