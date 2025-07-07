
# service/viagem_service.py
# Service para regras de negócio e validação de Viagem
from models import viagem
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
        viagens = viagem.listar_viagens()
        for v in viagens:
            if v[1] == funcionario_id and v[3] == localidade_id and v[6] == data_saida and v[7] == data_retorno:
                return False, "Já existe uma viagem cadastrada para este funcionário, localidade e datas."

        try:
            viagem.inserir_viagem(funcionario_id, tipo_viagem_id, localidade_id, requisicao_id, 'pendente', data_saida, data_retorno, duracao_dias, orcamento_aprovado)
            return True, "Solicitação de viagem cadastrada com sucesso."
        except Exception as e:
            return False, f"Erro ao cadastrar viagem: {str(e)}"


    def listar_viagens(self):
        return viagem.listar_viagens()


    def buscar_viagem(self, viagem_id):
        v = viagem.buscar_viagem_por_id(viagem_id)
        if v:
            return True, v
        else:
            return False, "Viagem não encontrada."


    def atualizar_status_viagem(self, viagem_id, novo_status):
        v = viagem.buscar_viagem_por_id(viagem_id)
        if not v:
            return False, "Viagem não encontrada."
        try:
            viagem.atualizar_viagem(viagem_id, v[1], v[2], v[3], v[4], novo_status, v[6], v[7], v[8], v[9])
            return True, f"Status da viagem atualizado para '{novo_status}'."
        except Exception as e:
            return False, f"Erro ao atualizar status: {str(e)}"


    def atualizar_viagem(self, viagem_id, funcionario_id, tipo_viagem_id, localidade_id, requisicao_id, status, data_saida, data_retorno, duracao_dias, orcamento_aprovado):
        # Permite atualização completa, mas pode adicionar regras específicas se necessário
        try:
            viagem.atualizar_viagem(viagem_id, funcionario_id, tipo_viagem_id, localidade_id, requisicao_id, status, data_saida, data_retorno, duracao_dias, orcamento_aprovado)
            return True, "Viagem atualizada com sucesso."
        except Exception as e:
            return False, f"Erro ao atualizar viagem: {str(e)}"


    def remover_viagem(self, viagem_id):
        try:
            viagem.remover_viagem(viagem_id)
            return True, "Viagem removida com sucesso."
        except Exception as e:
            return False, f"Erro ao remover viagem: {str(e)}"


    def confirmar_viagem(self, viagem_id):
        # Confirma viagem se status for 'aprovado'
        v = viagem.buscar_viagem_por_id(viagem_id)
        if not v:
            return False, "Viagem não encontrada."
        if v[5] != 'aprovado':
            return False, "A viagem só pode ser confirmada se estiver com status 'aprovado'."
        try:
            viagem.atualizar_viagem(viagem_id, v[1], v[2], v[3], v[4], 'confirmada', v[6], v[7], v[8], v[9])
            return True, "Viagem confirmada com sucesso."
        except Exception as e:
            return False, f"Erro ao confirmar viagem: {str(e)}"


    def cancelar_viagem(self, viagem_id):
        # Só permite cancelar se status for 'pendente', 'agendada' ou 'confirmada'
        v = viagem.buscar_viagem_por_id(viagem_id)
        if not v:
            return False, "Viagem não encontrada."
        if v[5] not in ['pendente', 'agendada', 'confirmada']:
            return False, "Só é possível cancelar viagens pendentes, agendadas ou confirmadas."
        try:
            viagem.atualizar_viagem(viagem_id, v[1], v[2], v[3], v[4], 'cancelada', v[6], v[7], v[8], v[9])
            return True, "Viagem cancelada com sucesso."
        except Exception as e:
            return False, f"Erro ao cancelar viagem: {str(e)}"
