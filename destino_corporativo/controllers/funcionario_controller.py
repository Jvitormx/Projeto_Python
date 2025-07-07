# controllers/funcionario_controller.py
# Controller para operações relacionadas ao Funcionário
from service.funcionario_service import FuncionarioService

funcionario_service = FuncionarioService()

def cadastrar_funcionario(nome, departamento, funcao):
    """Recebe dados da view, chama o service e retorna status/mensagem."""
    return funcionario_service.cadastrar_funcionario(nome, departamento, funcao)

def listar_funcionarios():
    """Retorna lista de funcionários cadastrados."""
    return funcionario_service.listar_funcionarios()

def buscar_funcionario(funcionario_id):
    """Busca um funcionário pelo ID."""
    return funcionario_service.buscar_funcionario(funcionario_id)

def atualizar_funcionario(funcionario_id, nome, departamento, funcao):
    """Atualiza dados de um funcionário."""
    return funcionario_service.atualizar_funcionario(funcionario_id, nome, departamento, funcao)

def remover_funcionario(funcionario_id):
    """Remove um funcionário pelo ID."""
    return funcionario_service.remover_funcionario(funcionario_id)

def listar_viagens_do_funcionario(funcionario_id):
    """Retorna todas as viagens de um funcionário."""
    return funcionario_service.listar_viagens_do_funcionario(funcionario_id)
