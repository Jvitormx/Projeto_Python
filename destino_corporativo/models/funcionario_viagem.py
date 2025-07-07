from .database import get_connection

def inserir_funcionario_viagem(funcionario_id, viagem_id, orcamento_pessoal):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO funcionario_viagem (funcionario_id, viagem_id, orcamento_pessoal)
        VALUES (?, ?, ?)
        """,
        (funcionario_id, viagem_id, orcamento_pessoal)
    )
    conn.commit()
    conn.close()

def listar_funcionarios_viagem():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, funcionario_id, viagem_id, orcamento_pessoal FROM funcionario_viagem")
    funcionarios = cursor.fetchall()
    conn.close()
    return funcionarios

def buscar_funcionario_viagem_por_id(funcionario_viagem_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, funcionario_id, viagem_id, orcamento_pessoal FROM funcionario_viagem WHERE id = ?", (funcionario_viagem_id,))
    funcionario = cursor.fetchone()
    conn.close()
    return funcionario

def atualizar_funcionario_viagem(funcionario_viagem_id, funcionario_id, viagem_id, orcamento_pessoal):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE funcionario_viagem SET funcionario_id = ?, viagem_id = ?, orcamento_pessoal = ?
        WHERE id = ?
        """,
        (funcionario_id, viagem_id, orcamento_pessoal, funcionario_viagem_id)
    )
    conn.commit()
    conn.close()

def remover_funcionario_viagem(funcionario_viagem_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM funcionario_viagem WHERE id = ?", (funcionario_viagem_id,))
    conn.commit()
    conn.close()
