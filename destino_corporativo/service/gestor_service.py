
# service/gestor_service.py
# Service para regras de negócio e validação de Gestor
from models.gestor import Gestor

class GestorService:
    def __init__(self):
        pass

    def cadastrar_gestor(self, nome, departamento):
        # Validação de campos obrigatórios
        if not nome or not departamento:
            return False, "Nome e departamento são obrigatórios."

        # Checagem de duplicidade (nome já cadastrado)
        gestores = Gestor.listar_todos()
        for g in gestores:
            if g.nome.strip().lower() == nome.strip().lower():
                return False, "Já existe um gestor com este nome."

        try:
            novo_gestor = Gestor(nome=nome, departamento=departamento)
            novo_gestor.salvar()
            return True, "Gestor cadastrado com sucesso."
        except Exception as e:
            return False, f"Erro ao cadastrar gestor: {str(e)}"

    def listar_gestores(self):
        return Gestor.listar_todos()

    def buscar_gestor(self, gestor_id):
        g = Gestor.buscar_por_id(gestor_id)
        if g:
            return True, g
        else:
            return False, "Gestor não encontrado."

    def atualizar_gestor(self, gestor_id, nome, departamento):
        if not nome or not departamento:
            return False, "Nome e departamento são obrigatórios."

        # Checagem de duplicidade (exceto o próprio)
        gestores = Gestor.listar_todos()
        for g in gestores:
            if g.id != gestor_id and g.nome.strip().lower() == nome.strip().lower():
                return False, "Já existe outro gestor com este nome."

        try:
            gestor_obj = Gestor.buscar_por_id(gestor_id)
            if not gestor_obj:
                return False, "Gestor não encontrado."
            gestor_obj.nome = nome
            gestor_obj.departamento = departamento
            gestor_obj.salvar()
            return True, "Gestor atualizado com sucesso."
        except Exception as e:
            return False, f"Erro ao atualizar gestor: {str(e)}"

    def remover_gestor(self, gestor_id):
        try:
            gestor_obj = Gestor.buscar_por_id(gestor_id)
            if not gestor_obj:
                return False, "Gestor não encontrado."
            gestor_obj.remover()
            return True, "Gestor removido com sucesso."
        except Exception as e:
            return False, f"Erro ao remover gestor: {str(e)}"
