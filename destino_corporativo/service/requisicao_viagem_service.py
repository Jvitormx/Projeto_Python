from datetime import datetime, timedelta
from models.requisicao_viagem import RequisicaoViagem
from models.viagem import Viagem

class RequisicaoViagemService:
    ANTECEDENCIA_MINIMA_DIAS_UTEIS = 5
    PRAZO_APROVACAO_DIAS_UTEIS = 2
    MAX_TENTATIVAS_REENVIO = 3

    def __init__(self):
        pass

    def solicitar_viagem(self, funcionario_id, requisicao_orcamento, quantidade_pessoal, motivacao, programacao_viagem, data_saida):
        # Verifica antecedência mínima de 5 dias úteis
        if not self._verificar_antecedencia(data_saida):
            raise ValueError("A solicitação deve ser feita com pelo menos 5 dias úteis de antecedência.")
        nova_req = RequisicaoViagem(
            funcionario_id=funcionario_id,
            requisicao_orcamento=requisicao_orcamento,
            quantidade_pessoal=quantidade_pessoal,
            motivacao=motivacao,
            programacao_viagem=programacao_viagem
        )
        nova_req.salvar()
        return nova_req.id

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
        # Retorna objetos RequisicaoViagem com viagem pendente
        pendentes = []
        for req in RequisicaoViagem.listar_todas():
            viagens = [v for v in Viagem.listar_todas() if v.requisicao_id == req.id and v.status == 'pendente']
            if viagens:
                pendentes.append(req)
        return pendentes

    def aprovar_requisicao(self, requisicao_id, gestor_id=None):
        # Atualiza status da viagem vinculada para 'aprovado'
        viagens = [v for v in Viagem.listar_todas() if v.requisicao_id == requisicao_id]
        for v in viagens:
            v.status = 'aprovado'
            v.salvar()
        # Notificação ao funcionário pode ser implementada na camada de controller/view

    def rejeitar_requisicao(self, requisicao_id, motivo_negacao=None):
        # Atualiza status da viagem vinculada para 'negado'
        viagens = [v for v in Viagem.listar_todas() if v.requisicao_id == requisicao_id]
        for v in viagens:
            v.status = 'negado'
            v.salvar()

    def colocar_em_reserva(self, requisicao_id):
        viagens = [v for v in Viagem.listar_todas() if v.requisicao_id == requisicao_id]
        for v in viagens:
            v.status = 'reserva'
            v.salvar()

    def reenviar_requisicao(self, requisicao_id, novas_infos):
        # novas_infos: dict com campos a atualizar na requisicao_viagem
        req = RequisicaoViagem.buscar_por_id(requisicao_id)
        if not req:
            return False, "Requisição não encontrada."
        for k, v in novas_infos.items():
            if hasattr(req, k):
                setattr(req, k, v)
        req.salvar()
        # Atualiza status da viagem para 'pendente'
        viagens = [v for v in Viagem.listar_todas() if v.requisicao_id == requisicao_id]
        for v in viagens:
            v.status = 'pendente'
            v.salvar()
        return True, "Requisição reenviada com sucesso."

    def excluir_requisicao_expirada(self, requisicao_id):
        # Remove viagens vinculadas
        viagens = [v for v in Viagem.listar_todas() if v.requisicao_id == requisicao_id]
        for v in viagens:
            v.remover()
        # Remove a própria requisicao
        req = RequisicaoViagem.buscar_por_id(requisicao_id)
        if req:
            req.remover()

    def verificar_prazo_aprovacao(self):
        # Identifica viagens pendentes há mais de 2 dias úteis
        pendentes = [v for v in Viagem.listar_todas() if v.status == 'pendente']
        notificacoes = []
        for v in pendentes:
            data_saida = v.data_saida
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
        return RequisicaoViagem.buscar_por_id(requisicao_id)

    def close(self):
        pass

# Instância global para uso no sistema
requisicao_viagem_service = RequisicaoViagemService()
