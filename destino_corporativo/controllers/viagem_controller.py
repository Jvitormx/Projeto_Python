# controllers/viagem_controller.py
# Controller para operações relacionadas à Viagem
from service.viagem_service import ViagemService

viagem_service = ViagemService()

def cadastrar_viagem(funcionario_id, tipo_viagem_id, localidade_id, requisicao_id, data_saida, data_retorno, orcamento_aprovado=None):
    """Recebe dados da view, chama o service e retorna status/mensagem."""
    return viagem_service.cadastrar_viagem(funcionario_id, tipo_viagem_id, localidade_id, requisicao_id, data_saida, data_retorno, orcamento_aprovado)

def listar_viagens():
    """Retorna lista de viagens cadastradas."""
    return viagem_service.listar_viagens()

def buscar_viagem(viagem_id):
    """Busca uma viagem pelo ID."""
    return viagem_service.buscar_viagem(viagem_id)

def atualizar_status_viagem(viagem_id, novo_status):
    """Atualiza o status de uma viagem."""
    return viagem_service.atualizar_status_viagem(viagem_id, novo_status)

def atualizar_viagem(viagem_id, funcionario_id, tipo_viagem_id, localidade_id, requisicao_id, status, data_saida, data_retorno, duracao_dias, orcamento_aprovado):
    """Atualiza todos os dados de uma viagem."""
    return viagem_service.atualizar_viagem(viagem_id, funcionario_id, tipo_viagem_id, localidade_id, requisicao_id, status, data_saida, data_retorno, duracao_dias, orcamento_aprovado)

def remover_viagem(viagem_id):
    """Remove uma viagem pelo ID."""
    return viagem_service.remover_viagem(viagem_id)

def confirmar_viagem(viagem_id):
    """Confirma uma viagem (status 'aprovado' para 'confirmada')."""
    return viagem_service.confirmar_viagem(viagem_id)

def cancelar_viagem(viagem_id):
    """Cancela uma viagem (status para 'cancelada')."""
    return viagem_service.cancelar_viagem(viagem_id)
