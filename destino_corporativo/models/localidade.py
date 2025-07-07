from .database import get_connection

class Localidade:
    def __init__(self, pais, numero_agencia, id=None):
        self.id = id
        self.pais = pais
        self.numero_agencia = numero_agencia

    def salvar(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                """
                INSERT INTO localidade (pais, numero_agencia)
                VALUES (?, ?)
                """,
                (self.pais, self.numero_agencia)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                """
                UPDATE localidade SET pais = ?, numero_agencia = ?
                WHERE id = ?
                """,
                (self.pais, self.numero_agencia, self.id)
            )
        conn.commit()
        conn.close()

    def remover(self):
        if self.id is None:
            raise ValueError("Localidade não possui ID para remoção.")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM localidade WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()

    @classmethod
    def buscar_por_id(cls, localidade_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, pais, numero_agencia FROM localidade WHERE id = ?", (localidade_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row[0], pais=row[1], numero_agencia=row[2])
        return None

    @classmethod
    def listar_todas(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, pais, numero_agencia FROM localidade")
        localidades = [cls(id=row[0], pais=row[1], numero_agencia=row[2]) for row in cursor.fetchall()]
        conn.close()
        return localidades
