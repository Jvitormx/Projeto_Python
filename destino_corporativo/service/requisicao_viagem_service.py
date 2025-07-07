import sqlite3
from datetime import datetime, timedelta
from models.database import get_db_connection

class RequisicaoViagemService:
    ANTECEDENCIA_MINIMA_DIAS_UTEIS = 5
    PRAZO_APROVACAO_DIAS_UTEIS = 2
    MAX_TENTATIVAS_REENVIO = 3

    def __init__(self):
        self.conn = get_db_connection()

    def solicitar_viagem(self, funcionario_id, requisicao_orcamento, quantidade_pessoal, motivacao, programacao_viagem, data_saida):
        # Verifica antecedência mínima de 5 dias úteis
        if not self._verificar_antecedencia(data_saida):
            raise ValueError("A solicitação deve ser feita com pelo menos 5 dias úteis de antecedência.")
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO requisicao_viagem (funcionario_id, requisicao_orcamento, quantidade_pessoal, motivacao, programacao_viagem)
            VALUES (?, ?, ?, ?, ?)
        ''', (funcionario_id, requisicao_orcamento, quantidade_pessoal, motivacao, programacao_viagem))
        self.conn.commit()
        return cursor.lastrowid

    def _verificar_antecedencia(self, data_saida):
        # data_saida: string 'YYYY-MM-DD'
        data_saida_dt = datetime.strptime(data_saida, '%Y-%m-%d')
        hoje = datetime.now()
        dias_uteis = 0
        data = hoje
        while data < data_saida_dt:
            if data.weekday() < 5:
                dias_uteis += 1
            data += timedelta(days=1)
        return dias_uteis >= self.ANTECEDENCIA_MINIMA_DIAS_UTEIS

    def listar_requisicoes_pendentes(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM requisicao_viagem WHERE id IN (SELECT requisicao_id FROM viagem WHERE status = 'pendente')
        ''')
        return cursor.fetchall()

    def aprovar_requisicao(self, requisicao_id, gestor_id):
        # Atualiza status da viagem vinculada para 'aprovado'
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE viagem SET status = 'aprovado' WHERE requisicao_id = ?
        ''', (requisicao_id,))
        self.conn.commit()
        # Notificação ao funcionário pode ser implementada na camada de controller/view

    def rejeitar_requisicao(self, requisicao_id, motivo_negacao=None):
        # Atualiza status da viagem vinculada para 'negado'
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE viagem SET status = 'negado' WHERE requisicao_id = ?
        ''', (requisicao_id,))
        self.conn.commit()

    def colocar_em_reserva(self, requisicao_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE viagem SET status = 'reserva' WHERE requisicao_id = ?
        ''', (requisicao_id,))
        self.conn.commit()

    def reenviar_requisicao(self, requisicao_id, novas_infos):
        # novas_infos: dict com campos a atualizar na requisicao_viagem
        cursor = self.conn.cursor()
        set_clause = ', '.join([f"{k} = ?" for k in novas_infos.keys()])
        values = list(novas_infos.values())
        values.append(requisicao_id)
        cursor.execute(f'''
            UPDATE requisicao_viagem SET {set_clause} WHERE id = ?
        ''', values)
        # Atualiza status da viagem para 'pendente' e incrementa tentativas
        cursor.execute('''
            UPDATE viagem SET status = 'pendente' WHERE requisicao_id = ?
        ''', (requisicao_id,))
        self.conn.commit()

    def excluir_requisicao_expirada(self, requisicao_id):
        cursor = self.conn.cursor()
        # Remove viagem vinculada
        cursor.execute('''
            DELETE FROM viagem WHERE requisicao_id = ?
        ''', (requisicao_id,))
        # Remove a própria requisicao
        cursor.execute('''
            DELETE FROM requisicao_viagem WHERE id = ?
        ''', (requisicao_id,))
        self.conn.commit()

    def verificar_prazo_aprovacao(self):
        # Identifica viagens pendentes há mais de 2 dias úteis
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, requisicao_id, data_saida FROM viagem WHERE status = 'pendente'
        ''')
        pendentes = cursor.fetchall()
        notificacoes = []
        for v in pendentes:
            # Supondo que há um campo data_criacao na viagem (se não houver, adicionar)
            # Aqui, para exemplo, usamos data_saida como proxy
            data_saida = v['data_saida']
            if data_saida:
                data_saida_dt = datetime.strptime(data_saida, '%Y-%m-%d')
                hoje = datetime.now()
                dias_uteis = 0
                data = hoje
                while data < data_saida_dt:
                    if data.weekday() < 5:
                        dias_uteis += 1
                    data += timedelta(days=1)
                if dias_uteis > self.PRAZO_APROVACAO_DIAS_UTEIS:
                    notificacoes.append(v)
        return notificacoes

    def get_requisicao(self, requisicao_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM requisicao_viagem WHERE id = ?''', (requisicao_id,))
        return cursor.fetchone()

    def close(self):
        self.conn.close()

# Instância global para uso no sistema
requisicao_viagem_service = RequisicaoViagemService()
