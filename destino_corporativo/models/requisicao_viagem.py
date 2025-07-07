from .database import get_connection

class RequisicaoViagem:
    def __init__(self, funcionario_id, requisicao_orcamento, quantidade_pessoal, motivacao, programacao_viagem, id=None):
        self.id = id
        self.funcionario_id = funcionario_id
        self.requisicao_orcamento = requisicao_orcamento
        self.quantidade_pessoal = quantidade_pessoal
        self.motivacao = motivacao
        self.programacao_viagem = programacao_viagem

    def salvar(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                """
                INSERT INTO requisicao_viagem (funcionario_id, requisicao_orcamento, quantidade_pessoal, motivacao, programacao_viagem)
                VALUES (?, ?, ?, ?, ?)
                """,
                (self.funcionario_id, self.requisicao_orcamento, self.quantidade_pessoal, self.motivacao, self.programacao_viagem)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                """
                UPDATE requisicao_viagem SET funcionario_id = ?, requisicao_orcamento = ?, quantidade_pessoal = ?, motivacao = ?, programacao_viagem = ?
                WHERE id = ?
                """,
                (self.funcionario_id, self.requisicao_orcamento, self.quantidade_pessoal, self.motivacao, self.programacao_viagem, self.id)
            )
        conn.commit()
        conn.close()

    def remover(self):
        if self.id is None:
            raise ValueError("RequisicaoViagem não possui ID para remoção.")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM requisicao_viagem WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()

    @classmethod
    def buscar_por_id(cls, requisicao_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, funcionario_id, requisicao_orcamento, quantidade_pessoal, motivacao, programacao_viagem FROM requisicao_viagem WHERE id = ?", (requisicao_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row[0], funcionario_id=row[1], requisicao_orcamento=row[2], quantidade_pessoal=row[3], motivacao=row[4], programacao_viagem=row[5])
        return None

    @classmethod
    def listar_todas(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, funcionario_id, requisicao_orcamento, quantidade_pessoal, motivacao, programacao_viagem FROM requisicao_viagem")
        requisicoes = [cls(id=row[0], funcionario_id=row[1], requisicao_orcamento=row[2], quantidade_pessoal=row[3], motivacao=row[4], programacao_viagem=row[5]) for row in cursor.fetchall()]
        conn.close()
        return requisicoes
