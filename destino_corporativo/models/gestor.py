from .database import get_connection

class Gestor:
    def __init__(self, nome, departamento, id=None):
        self.id = id
        self.nome = nome
        self.departamento = departamento

    def salvar(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                "INSERT INTO gestor (nome, departamento) VALUES (?, ?)",
                (self.nome, self.departamento)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE gestor SET nome = ?, departamento = ? WHERE id = ?",
                (self.nome, self.departamento, self.id)
            )
        conn.commit()
        conn.close()

    def remover(self):
        if self.id is None:
            raise ValueError("Gestor não possui ID para remoção.")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM gestor WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()

    @classmethod
    def buscar_por_id(cls, gestor_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, departamento FROM gestor WHERE id = ?", (gestor_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row[0], nome=row[1], departamento=row[2])
        return None

    @classmethod
    def buscar_por_nome(cls, nome):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, departamento FROM gestor WHERE LOWER(nome) = ?", (nome.lower(),))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row[0], nome=row[1], departamento=row[2])
        return None

    @classmethod
    def listar_todos(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, departamento FROM gestor")
        gestores = [cls(id=row[0], nome=row[1], departamento=row[2]) for row in cursor.fetchall()]
        conn.close()
        return gestores
