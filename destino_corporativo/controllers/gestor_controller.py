# controllers/gestor_controller.py
# Controller para operações relacionadas ao Gestor
from service.gestor_service import GestorService

gestor_service = GestorService()

def cadastrar_gestor(nome, departamento):
    """Recebe dados da view, chama o service e retorna status/mensagem."""
    return gestor_service.cadastrar_gestor(nome, departamento)

def listar_gestores():
    """Retorna lista de gestores cadastrados."""
    return gestor_service.listar_gestores()

def buscar_gestor(gestor_id):
    """Busca um gestor pelo ID."""
    return gestor_service.buscar_gestor(gestor_id)

def atualizar_gestor(gestor_id, nome, departamento):
    """Atualiza dados de um gestor."""
    return gestor_service.atualizar_gestor(gestor_id, nome, departamento)

def remover_gestor(gestor_id):
    """Remove um gestor pelo ID."""
    return gestor_service.remover_gestor(gestor_id)
