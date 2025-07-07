from .database import get_connection

def inserir_gestor(nome, departamento):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO gestor (nome, departamento) VALUES (?, ?)", (nome, departamento))
    conn.commit()
    conn.close()

def listar_gestores():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, departamento FROM gestor")
    gestores = cursor.fetchall()
    conn.close()
    return gestores

def buscar_gestor_por_id(gestor_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, departamento FROM gestor WHERE id = ?", (gestor_id,))
    gestor = cursor.fetchone()
    conn.close()
    return gestor

def atualizar_gestor(gestor_id, nome, departamento):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE gestor SET nome = ?, departamento = ? WHERE id = ?", (nome, departamento, gestor_id))
    conn.commit()
    conn.close()

def remover_gestor(gestor_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM gestor WHERE id = ?", (gestor_id,))
    conn.commit()
    conn.close()
