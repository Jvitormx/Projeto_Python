from .database import get_connection

class Despesa:
    def __init__(self, viagem_id, assunto, valor, data, comprovante, id=None):
        self.id = id
        self.viagem_id = viagem_id
        self.assunto = assunto
        self.valor = valor
        self.data = data
        self.comprovante = comprovante

    def salvar(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                """
                INSERT INTO despesa (viagem_id, assunto, valor, data, comprovante)
                VALUES (?, ?, ?, ?, ?)
                """,
                (self.viagem_id, self.assunto, self.valor, self.data, self.comprovante)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                """
                UPDATE despesa SET viagem_id = ?, assunto = ?, valor = ?, data = ?, comprovante = ?
                WHERE id = ?
                """,
                (self.viagem_id, self.assunto, self.valor, self.data, self.comprovante, self.id)
            )
        conn.commit()
        conn.close()

    def remover(self):
        if self.id is None:
            raise ValueError("Despesa não possui ID para remoção.")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM despesa WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()

    @classmethod
    def buscar_por_id(cls, despesa_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, viagem_id, assunto, valor, data, comprovante FROM despesa WHERE id = ?", (despesa_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row[0], viagem_id=row[1], assunto=row[2], valor=row[3], data=row[4], comprovante=row[5])
        return None

    @classmethod
    def listar_todas(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, viagem_id, assunto, valor, data, comprovante FROM despesa")
        despesas = [cls(id=row[0], viagem_id=row[1], assunto=row[2], valor=row[3], data=row[4], comprovante=row[5]) for row in cursor.fetchall()]
        conn.close()
        return despesas

    @classmethod
    def listar_por_viagem(cls, viagem_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, viagem_id, assunto, valor, data, comprovante FROM despesa WHERE viagem_id = ?", (viagem_id,))
        despesas = [cls(id=row[0], viagem_id=row[1], assunto=row[2], valor=row[3], data=row[4], comprovante=row[5]) for row in cursor.fetchall()]
        conn.close()
        return despesas
