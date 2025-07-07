
# service/funcionario_service.py
# Service para regras de negócio e validação de Funcionário
from models.funcionario import Funcionario

class FuncionarioService:
    def __init__(self):
        pass

    def cadastrar_funcionario(self, nome, departamento, funcao):
        # Validação de campos obrigatórios
        if not nome or not departamento or not funcao:
            return False, "Nome, departamento e função são obrigatórios."

        # Checagem de duplicidade (nome já cadastrado)
        funcionarios = Funcionario.listar_todos()
        for f in funcionarios:
            if f.nome.strip().lower() == nome.strip().lower():
                return False, "Já existe um funcionário com este nome."

        try:
            novo_funcionario = Funcionario(nome=nome, departamento=departamento, funcao=funcao)
            novo_funcionario.salvar()
            return True, "Funcionário cadastrado com sucesso."
        except Exception as e:
            return False, f"Erro ao cadastrar funcionário: {str(e)}"


    def listar_funcionarios(self):
        return Funcionario.listar_todos()

    def listar_viagens_do_funcionario(self, funcionario_id):
        funcionario_obj = Funcionario.buscar_por_id(funcionario_id)
        if not funcionario_obj:
            return False, "Funcionário não encontrado."
        viagens = funcionario_obj.listar_viagens()
        if viagens:
            return True, viagens
        else:
            return False, "Nenhuma viagem encontrada para este funcionário."


    def buscar_funcionario(self, funcionario_id):
        f = Funcionario.buscar_por_id(funcionario_id)
        if f:
            return True, f
        else:
            return False, "Funcionário não encontrado ou cadastro pendente."

    def atualizar_funcionario(self, funcionario_id, nome, departamento, funcao):
        if not nome or not departamento or not funcao:
            return False, "Nome, departamento e função são obrigatórios."

        # Checagem de duplicidade (exceto o próprio)
        funcionarios = Funcionario.listar_todos()
        for f in funcionarios:
            if f.id != funcionario_id and f.nome.strip().lower() == nome.strip().lower():
                return False, "Já existe outro funcionário com este nome."

        try:
            funcionario_obj = Funcionario.buscar_por_id(funcionario_id)
            if not funcionario_obj:
                return False, "Funcionário não encontrado."
            funcionario_obj.nome = nome
            funcionario_obj.departamento = departamento
            funcionario_obj.funcao = funcao
            funcionario_obj.salvar()
            return True, "Funcionário atualizado com sucesso."
        except Exception as e:
            return False, f"Erro ao atualizar funcionário: {str(e)}"

    def remover_funcionario(self, funcionario_id):
        try:
            funcionario_obj = Funcionario.buscar_por_id(funcionario_id)
            if not funcionario_obj:
                return False, "Funcionário não encontrado."
            funcionario_obj.remover()
            return True, "Funcionário removido com sucesso."
        except Exception as e:
            return False, f"Erro ao remover funcionário: {str(e)}"
