# controllers/requisicao_viagem_controller.py
# Controller para operações relacionadas à Requisição de Viagem
from service.requisicao_viagem_service import requisicao_viagem_service

def solicitar_viagem(funcionario_id, requisicao_orcamento, quantidade_pessoal, motivacao, programacao_viagem, data_saida):
    """Solicita uma nova viagem, validando antecedência e regras de negócio."""
    try:
        requisicao_id = requisicao_viagem_service.solicitar_viagem(
            funcionario_id, requisicao_orcamento, quantidade_pessoal, motivacao, programacao_viagem, data_saida
        )
        return True, requisicao_id
    except Exception as e:
        return False, str(e)

def listar_requisicoes_pendentes():
    """Lista todas as requisições de viagem pendentes de aprovação."""
    return requisicao_viagem_service.listar_requisicoes_pendentes()

def aprovar_requisicao(requisicao_id, gestor_id):
    """Aprova uma requisição de viagem."""
    try:
        requisicao_viagem_service.aprovar_requisicao(requisicao_id, gestor_id)
        return True, "Requisição aprovada com sucesso."
    except Exception as e:
        return False, str(e)

def rejeitar_requisicao(requisicao_id, motivo_negacao=None):
    """Rejeita uma requisição de viagem."""
    try:
        requisicao_viagem_service.rejeitar_requisicao(requisicao_id, motivo_negacao)
        return True, "Requisição rejeitada com sucesso."
    except Exception as e:
        return False, str(e)

def colocar_em_reserva(requisicao_id):
    """Coloca uma requisição em status de reserva."""
    try:
        requisicao_viagem_service.colocar_em_reserva(requisicao_id)
        return True, "Requisição colocada em reserva."
    except Exception as e:
        return False, str(e)

def reenviar_requisicao(requisicao_id, novas_infos):
    """Reenvia uma requisição negada, atualizando informações."""
    try:
        requisicao_viagem_service.reenviar_requisicao(requisicao_id, novas_infos)
        return True, "Requisição reenviada para análise."
    except Exception as e:
        return False, str(e)

def excluir_requisicao_expirada(requisicao_id):
    """Exclui uma requisição expirada do sistema."""
    try:
        requisicao_viagem_service.excluir_requisicao_expirada(requisicao_id)
        return True, "Requisição expirada excluída."
    except Exception as e:
        return False, str(e)

def verificar_prazo_aprovacao():
    """Verifica requisições pendentes além do prazo de aprovação e retorna notificações."""
    return requisicao_viagem_service.verificar_prazo_aprovacao()

def get_requisicao(requisicao_id):
    """Busca uma requisição de viagem pelo ID."""
    return requisicao_viagem_service.get_requisicao(requisicao_id)
