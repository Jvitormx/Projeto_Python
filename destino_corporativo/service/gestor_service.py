
# service/gestor_service.py
# Service para regras de negócio e validação de Gestor
from models import gestor

class GestorService:
    def __init__(self):
        pass

    def cadastrar_gestor(self, nome, departamento):
        # Validação de campos obrigatórios
        if not nome or not departamento:
            return False, "Nome e departamento são obrigatórios."

        # Checagem de duplicidade (nome já cadastrado)
        gestores = gestor.listar_gestores()
        for g in gestores:
            if g[1].strip().lower() == nome.strip().lower():
                return False, "Já existe um gestor com este nome."

        try:
            gestor.inserir_gestor(nome, departamento)
            return True, "Gestor cadastrado com sucesso."
        except Exception as e:
            return False, f"Erro ao cadastrar gestor: {str(e)}"

    def listar_gestores(self):
        return gestor.listar_gestores()

    def buscar_gestor(self, gestor_id):
        g = gestor.buscar_gestor_por_id(gestor_id)
        if g:
            return True, g
        else:
            return False, "Gestor não encontrado."

    def atualizar_gestor(self, gestor_id, nome, departamento):
        if not nome or not departamento:
            return False, "Nome e departamento são obrigatórios."

        # Checagem de duplicidade (exceto o próprio)
        gestores = gestor.listar_gestores()
        for g in gestores:
            if g[0] != gestor_id and g[1].strip().lower() == nome.strip().lower():
                return False, "Já existe outro gestor com este nome."

        try:
            gestor.atualizar_gestor(gestor_id, nome, departamento)
            return True, "Gestor atualizado com sucesso."
        except Exception as e:
            return False, f"Erro ao atualizar gestor: {str(e)}"

    def remover_gestor(self, gestor_id):
        try:
            gestor.remover_gestor(gestor_id)
            return True, "Gestor removido com sucesso."
        except Exception as e:
            return False, f"Erro ao remover gestor: {str(e)}"
