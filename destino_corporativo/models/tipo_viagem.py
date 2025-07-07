from .database import get_connection

class TipoViagem:
    def __init__(self, motivo, quant_pessoal_max_estimado, duracao_dias_max_estimado, motivo_base, programacao_base, id=None):
        self.id = id
        self.motivo = motivo
        self.quant_pessoal_max_estimado = quant_pessoal_max_estimado
        self.duracao_dias_max_estimado = duracao_dias_max_estimado
        self.motivo_base = motivo_base
        self.programacao_base = programacao_base

    def salvar(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                """
                INSERT INTO tipo_viagem (motivo, quant_pessoal_max_estimado, duracao_dias_max_estimado, motivo_base, programacao_base)
                VALUES (?, ?, ?, ?, ?)
                """,
                (self.motivo, self.quant_pessoal_max_estimado, self.duracao_dias_max_estimado, self.motivo_base, self.programacao_base)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                """
                UPDATE tipo_viagem SET motivo = ?, quant_pessoal_max_estimado = ?, duracao_dias_max_estimado = ?, motivo_base = ?, programacao_base = ?
                WHERE id = ?
                """,
                (self.motivo, self.quant_pessoal_max_estimado, self.duracao_dias_max_estimado, self.motivo_base, self.programacao_base, self.id)
            )
        conn.commit()
        conn.close()

    def remover(self):
        if self.id is None:
            raise ValueError("TipoViagem não possui ID para remoção.")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tipo_viagem WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()

    @classmethod
    def buscar_por_id(cls, tipo_viagem_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, motivo, quant_pessoal_max_estimado, duracao_dias_max_estimado, motivo_base, programacao_base FROM tipo_viagem WHERE id = ?", (tipo_viagem_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row[0], motivo=row[1], quant_pessoal_max_estimado=row[2], duracao_dias_max_estimado=row[3], motivo_base=row[4], programacao_base=row[5])
        return None

    @classmethod
    def listar_todos(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, motivo, quant_pessoal_max_estimado, duracao_dias_max_estimado, motivo_base, programacao_base FROM tipo_viagem")
        tipos = [cls(id=row[0], motivo=row[1], quant_pessoal_max_estimado=row[2], duracao_dias_max_estimado=row[3], motivo_base=row[4], programacao_base=row[5]) for row in cursor.fetchall()]
        conn.close()
        return tipos
