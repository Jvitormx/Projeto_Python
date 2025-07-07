from .database import get_connection

class LocalidadeCidade:
    def __init__(self, cidade, localidade_id, id=None):
        self.id = id
        self.cidade = cidade
        self.localidade_id = localidade_id

    def salvar(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                """
                INSERT INTO localidade_cidade (cidade, localidade_id)
                VALUES (?, ?)
                """,
                (self.cidade, self.localidade_id)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                """
                UPDATE localidade_cidade SET cidade = ?, localidade_id = ?
                WHERE id = ?
                """,
                (self.cidade, self.localidade_id, self.id)
            )
        conn.commit()
        conn.close()

    def remover(self):
        if self.id is None:
            raise ValueError("LocalidadeCidade não possui ID para remoção.")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM localidade_cidade WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()

    @classmethod
    def buscar_por_id(cls, localidade_cidade_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, cidade, localidade_id FROM localidade_cidade WHERE id = ?", (localidade_cidade_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row[0], cidade=row[1], localidade_id=row[2])
        return None

    @classmethod
    def listar_todas(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, cidade, localidade_id FROM localidade_cidade")
        cidades = [cls(id=row[0], cidade=row[1], localidade_id=row[2]) for row in cursor.fetchall()]
        conn.close()
        return cidades
