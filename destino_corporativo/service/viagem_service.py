
# service/viagem_service.py
# Service para regras de negócio e validação de Viagem
from models.viagem import Viagem
from datetime import datetime, timedelta


class ViagemService:
    def __init__(self):
        pass

    def cadastrar_viagem(self, funcionario_id, tipo_viagem_id, localidade_id, requisicao_id, data_saida, data_retorno, orcamento_aprovado=None):
        # Validação de campos obrigatórios
        if not funcionario_id or not tipo_viagem_id or not localidade_id or not requisicao_id or not data_saida or not data_retorno:
            return False, "Todos os campos são obrigatórios."

        # Validação de datas (data_saida >= hoje + 5 dias úteis)
        try:
            data_saida_dt = datetime.strptime(data_saida, "%Y-%m-%d")
            hoje = datetime.now()
            dias_uteis = 0
            data_temp = hoje
            while dias_uteis < 5:
                data_temp += timedelta(days=1)
                if data_temp.weekday() < 5:
                    dias_uteis += 1
            if data_saida_dt < data_temp:
                return False, "A solicitação deve ser feita com pelo menos 5 dias úteis de antecedência."
        except Exception:
            return False, "Data de saída inválida. Use o formato YYYY-MM-DD."

        # Calcular duração da viagem
        try:
            data_retorno_dt = datetime.strptime(data_retorno, "%Y-%m-%d")
            duracao_dias = (data_retorno_dt - data_saida_dt).days
            if duracao_dias <= 0:
                return False, "A data de retorno deve ser posterior à data de saída."
        except Exception:
            return False, "Data de retorno inválida. Use o formato YYYY-MM-DD."

        # Não permitir viagens duplicadas para o mesmo funcionário, localidade e datas
        viagens = Viagem.listar_todas()
        for v in viagens:
            if v.funcionario_id == funcionario_id and v.localidade_id == localidade_id and v.data_saida == data_saida and v.data_retorno == data_retorno:
                return False, "Já existe uma viagem cadastrada para este funcionário, localidade e datas."

        try:
            nova_viagem = Viagem(
                funcionario_id=funcionario_id,
                tipo_viagem_id=tipo_viagem_id,
                localidade_id=localidade_id,
                requisicao_id=requisicao_id,
                status='pendente',
                data_saida=data_saida,
                data_retorno=data_retorno,
                duracao_dias=duracao_dias,
                orcamento_aprovado=orcamento_aprovado
            )
            nova_viagem.salvar()
            return True, "Solicitação de viagem cadastrada com sucesso."
        except Exception as e:
            return False, f"Erro ao cadastrar viagem: {str(e)}"


    def listar_viagens(self):
        return Viagem.listar_todas()


    def buscar_viagem(self, viagem_id):
        v = Viagem.buscar_por_id(viagem_id)
        if v:
            return True, v
        else:
            return False, "Viagem não encontrada."


    def atualizar_status_viagem(self, viagem_id, novo_status):
        v = Viagem.buscar_por_id(viagem_id)
        if not v:
            return False, "Viagem não encontrada."
        try:
            v.status = novo_status
            v.salvar()
            return True, f"Status da viagem atualizado para '{novo_status}'."
        except Exception as e:
            return False, f"Erro ao atualizar status: {str(e)}"


    def atualizar_viagem(self, viagem_id, funcionario_id, tipo_viagem_id, localidade_id, requisicao_id, status, data_saida, data_retorno, duracao_dias, orcamento_aprovado):
        try:
            v = Viagem.buscar_por_id(viagem_id)
            if not v:
                return False, "Viagem não encontrada."
            v.funcionario_id = funcionario_id
            v.tipo_viagem_id = tipo_viagem_id
            v.localidade_id = localidade_id
            v.requisicao_id = requisicao_id
            v.status = status
            v.data_saida = data_saida
            v.data_retorno = data_retorno
            v.duracao_dias = duracao_dias
            v.orcamento_aprovado = orcamento_aprovado
            v.salvar()
            return True, "Viagem atualizada com sucesso."
        except Exception as e:
            return False, f"Erro ao atualizar viagem: {str(e)}"


    def remover_viagem(self, viagem_id):
        try:
            v = Viagem.buscar_por_id(viagem_id)
            if not v:
                return False, "Viagem não encontrada."
            v.remover()
            return True, "Viagem removida com sucesso."
        except Exception as e:
            return False, f"Erro ao remover viagem: {str(e)}"


    def confirmar_viagem(self, viagem_id):
        v = Viagem.buscar_por_id(viagem_id)
        if not v:
            return False, "Viagem não encontrada."
        if v.status != 'aprovado':
            return False, "A viagem só pode ser confirmada se estiver com status 'aprovado'."
        try:
            v.status = 'confirmada'
            v.salvar()
            return True, "Viagem confirmada com sucesso."
        except Exception as e:
            return False, f"Erro ao confirmar viagem: {str(e)}"


    def cancelar_viagem(self, viagem_id):
        v = Viagem.buscar_por_id(viagem_id)
        if not v:
            return False, "Viagem não encontrada."
        if v.status not in ['pendente', 'agendada', 'confirmada']:
            return False, "Só é possível cancelar viagens pendentes, agendadas ou confirmadas."
        try:
            v.status = 'cancelada'
            v.salvar()
            return True, "Viagem cancelada com sucesso."
        except Exception as e:
            return False, f"Erro ao cancelar viagem: {str(e)}"
