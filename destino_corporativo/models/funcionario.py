from .database import get_connection

def inserir_funcionario(nome, departamento, funcao):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO funcionario (nome, departamento, funcao) VALUES (?, ?, ?)", (nome, departamento, funcao))
    conn.commit()
    conn.close()

def listar_funcionarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, departamento, funcao FROM funcionario")
    funcionarios = cursor.fetchall()
    conn.close()
    return funcionarios

def buscar_funcionario_por_id(funcionario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, departamento, funcao FROM funcionario WHERE id = ?", (funcionario_id,))
    funcionario = cursor.fetchone()
    conn.close()
    return funcionario

def atualizar_funcionario(funcionario_id, nome, departamento, funcao):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE funcionario SET nome = ?, departamento = ?, funcao = ? WHERE id = ?", (nome, departamento, funcao, funcionario_id))
    conn.commit()
    conn.close()

def remover_funcionario(funcionario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM funcionario WHERE id = ?", (funcionario_id,))
    conn.commit()
    conn.close()

def listar_viagens_do_funcionario(funcionario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM viagem WHERE funcionario_id = ?", (funcionario_id,))
    viagens = cursor.fetchall()
    conn.close()
    return viagens
