from .database import get_connection

class FuncionarioViagem:
    def __init__(self, funcionario_id, viagem_id, orcamento_pessoal, id=None):
        self.id = id
        self.funcionario_id = funcionario_id
        self.viagem_id = viagem_id
        self.orcamento_pessoal = orcamento_pessoal

    def salvar(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                """
                INSERT INTO funcionario_viagem (funcionario_id, viagem_id, orcamento_pessoal)
                VALUES (?, ?, ?)
                """,
                (self.funcionario_id, self.viagem_id, self.orcamento_pessoal)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                """
                UPDATE funcionario_viagem SET funcionario_id = ?, viagem_id = ?, orcamento_pessoal = ?
                WHERE id = ?
                """,
                (self.funcionario_id, self.viagem_id, self.orcamento_pessoal, self.id)
            )
        conn.commit()
        conn.close()

    def remover(self):
        if self.id is None:
            raise ValueError("FuncionarioViagem não possui ID para remoção.")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM funcionario_viagem WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()

    @classmethod
    def buscar_por_id(cls, funcionario_viagem_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, funcionario_id, viagem_id, orcamento_pessoal FROM funcionario_viagem WHERE id = ?", (funcionario_viagem_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row[0], funcionario_id=row[1], viagem_id=row[2], orcamento_pessoal=row[3])
        return None

    @classmethod
    def listar_todos(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, funcionario_id, viagem_id, orcamento_pessoal FROM funcionario_viagem")
        funcionarios = [cls(id=row[0], funcionario_id=row[1], viagem_id=row[2], orcamento_pessoal=row[3]) for row in cursor.fetchall()]
        conn.close()
        return funcionarios
