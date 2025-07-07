from .database import get_connection

class Viagem:
    def __init__(self, funcionario_id, tipo_viagem_id, localidade_id, requisicao_id, status, data_saida, data_retorno, duracao_dias, orcamento_aprovado=None, id=None):
        self.id = id
        self.funcionario_id = funcionario_id
        self.tipo_viagem_id = tipo_viagem_id
        self.localidade_id = localidade_id
        self.requisicao_id = requisicao_id
        self.status = status
        self.data_saida = data_saida
        self.data_retorno = data_retorno
        self.duracao_dias = duracao_dias
        self.orcamento_aprovado = orcamento_aprovado

    def salvar(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                """
                INSERT INTO viagem (funcionario_id, tipo_viagem_id, localidade_id, requisicao_id, status, data_saida, data_retorno, duracao_dias, orcamento_aprovado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (self.funcionario_id, self.tipo_viagem_id, self.localidade_id, self.requisicao_id, self.status, self.data_saida, self.data_retorno, self.duracao_dias, self.orcamento_aprovado)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                """
                UPDATE viagem SET funcionario_id = ?, tipo_viagem_id = ?, localidade_id = ?, requisicao_id = ?, status = ?, data_saida = ?, data_retorno = ?, duracao_dias = ?, orcamento_aprovado = ?
                WHERE id = ?
                """,
                (self.funcionario_id, self.tipo_viagem_id, self.localidade_id, self.requisicao_id, self.status, self.data_saida, self.data_retorno, self.duracao_dias, self.orcamento_aprovado, self.id)
            )
        conn.commit()
        conn.close()

    def remover(self):
        if self.id is None:
            raise ValueError("Viagem não possui ID para remoção.")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM viagem WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()

    @classmethod
    def buscar_por_id(cls, viagem_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, funcionario_id, tipo_viagem_id, localidade_id, requisicao_id, status, data_saida, data_retorno, duracao_dias, orcamento_aprovado FROM viagem WHERE id = ?", (viagem_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row[0], funcionario_id=row[1], tipo_viagem_id=row[2], localidade_id=row[3], requisicao_id=row[4], status=row[5], data_saida=row[6], data_retorno=row[7], duracao_dias=row[8], orcamento_aprovado=row[9])
        return None

    @classmethod
    def listar_todas(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, funcionario_id, tipo_viagem_id, localidade_id, requisicao_id, status, data_saida, data_retorno, duracao_dias, orcamento_aprovado FROM viagem")
        viagens = [cls(id=row[0], funcionario_id=row[1], tipo_viagem_id=row[2], localidade_id=row[3], requisicao_id=row[4], status=row[5], data_saida=row[6], data_retorno=row[7], duracao_dias=row[8], orcamento_aprovado=row[9]) for row in cursor.fetchall()]
        conn.close()
        return viagens
