from .database import get_connection

def inserir_requisicao_viagem(funcionario_id, requisicao_orcamento, quantidade_pessoal, motivacao, programacao_viagem):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO requisicao_viagem (funcionario_id, requisicao_orcamento, quantidade_pessoal, motivacao, programacao_viagem)
        VALUES (?, ?, ?, ?, ?)
        """,
        (funcionario_id, requisicao_orcamento, quantidade_pessoal, motivacao, programacao_viagem)
    )
    conn.commit()
    conn.close()

def listar_requisicoes_viagem():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, funcionario_id, requisicao_orcamento, quantidade_pessoal, motivacao, programacao_viagem FROM requisicao_viagem")
    requisicoes = cursor.fetchall()
    conn.close()
    return requisicoes

def buscar_requisicao_viagem_por_id(requisicao_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, funcionario_id, requisicao_orcamento, quantidade_pessoal, motivacao, programacao_viagem FROM requisicao_viagem WHERE id = ?", (requisicao_id,))
    requisicao = cursor.fetchone()
    conn.close()
    return requisicao

def atualizar_requisicao_viagem(requisicao_id, funcionario_id, requisicao_orcamento, quantidade_pessoal, motivacao, programacao_viagem):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE requisicao_viagem SET funcionario_id = ?, requisicao_orcamento = ?, quantidade_pessoal = ?, motivacao = ?, programacao_viagem = ?
        WHERE id = ?
        """,
        (funcionario_id, requisicao_orcamento, quantidade_pessoal, motivacao, programacao_viagem, requisicao_id)
    )
    conn.commit()
    conn.close()

def remover_requisicao_viagem(requisicao_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM requisicao_viagem WHERE id = ?", (requisicao_id,))
    conn.commit()
    conn.close()
