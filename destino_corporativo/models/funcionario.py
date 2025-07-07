from .database import get_connection

class Funcionario:
    def __init__(self, nome, departamento, funcao, id=None):
        self.id = id
        self.nome = nome
        self.departamento = departamento
        self.funcao = funcao

    def salvar(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                "INSERT INTO funcionario (nome, departamento, funcao) VALUES (?, ?, ?)",
                (self.nome, self.departamento, self.funcao)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE funcionario SET nome = ?, departamento = ?, funcao = ? WHERE id = ?",
                (self.nome, self.departamento, self.funcao, self.id)
            )
        conn.commit()
        conn.close()

    def remover(self):
        if self.id is None:
            raise ValueError("Funcionário não possui ID para remoção.")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM funcionario WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()

    def listar_viagens(self):
        if self.id is None:
            return []
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM viagem WHERE funcionario_id = ?", (self.id,))
        viagens = cursor.fetchall()
        conn.close()
        return viagens

    @classmethod
    def buscar_por_id(cls, funcionario_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, departamento, funcao FROM funcionario WHERE id = ?", (funcionario_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row[0], nome=row[1], departamento=row[2], funcao=row[3])
        return None

    @classmethod
    def buscar_por_nome(cls, nome):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, departamento, funcao FROM funcionario WHERE LOWER(nome) = ?", (nome.lower(),))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row[0], nome=row[1], departamento=row[2], funcao=row[3])
        return None

    @classmethod
    def listar_todos(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, departamento, funcao FROM funcionario")
        funcionarios = [cls(id=row[0], nome=row[1], departamento=row[2], funcao=row[3]) for row in cursor.fetchall()]
        conn.close()
        return funcionarios
