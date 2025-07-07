
# service/funcionario_service.py
# Service para regras de negócio e validação de Funcionário
from models import funcionario

class FuncionarioService:
    def __init__(self):
        pass

    def cadastrar_funcionario(self, nome, departamento, funcao):
        # Validação de campos obrigatórios
        if not nome or not departamento or not funcao:
            return False, "Nome, departamento e função são obrigatórios."

        # Checagem de duplicidade (nome já cadastrado)
        funcionarios = funcionario.listar_funcionarios()
        for f in funcionarios:
            if f[1].strip().lower() == nome.strip().lower():
                return False, "Já existe um funcionário com este nome."

        try:
            funcionario.inserir_funcionario(nome, departamento, funcao)
            return True, "Funcionário cadastrado com sucesso."
        except Exception as e:
            return False, f"Erro ao cadastrar funcionário: {str(e)}"


    def listar_funcionarios(self):
        return funcionario.listar_funcionarios()

    def listar_viagens_do_funcionario(self, funcionario_id):
        # Retorna todas as viagens do funcionário
        viagens = funcionario.listar_viagens_do_funcionario(funcionario_id)
        if viagens:
            return True, viagens
        else:
            return False, "Nenhuma viagem encontrada para este funcionário."


    def buscar_funcionario(self, funcionario_id):
        f = funcionario.buscar_funcionario_por_id(funcionario_id)
        if f:
            return True, f
        else:
            return False, "Funcionário não encontrado ou cadastro pendente."

    def atualizar_funcionario(self, funcionario_id, nome, departamento, funcao):
        if not nome or not departamento or not funcao:
            return False, "Nome, departamento e função são obrigatórios."

        # Checagem de duplicidade (exceto o próprio)
        funcionarios = funcionario.listar_funcionarios()
        for f in funcionarios:
            if f[0] != funcionario_id and f[1].strip().lower() == nome.strip().lower():
                return False, "Já existe outro funcionário com este nome."

        try:
            funcionario.atualizar_funcionario(funcionario_id, nome, departamento, funcao)
            return True, "Funcionário atualizado com sucesso."
        except Exception as e:
            return False, f"Erro ao atualizar funcionário: {str(e)}"

    def remover_funcionario(self, funcionario_id):
        try:
            funcionario.remover_funcionario(funcionario_id)
            return True, "Funcionário removido com sucesso."
        except Exception as e:
            return False, f"Erro ao remover funcionário: {str(e)}"
