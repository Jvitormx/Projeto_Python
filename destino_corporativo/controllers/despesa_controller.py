# controllers/despesa_controller.py
# Controller para orquestrar operações de Despesa via DespesaService
from service.despesa_service import DespesaService

class DespesaController:
    def __init__(self):
        self.service = DespesaService()

    def cadastrar_despesa(self, viagem_id, assunto, valor, data, comprovante, nome_arquivo=None):
        """
        Registra uma nova despesa vinculada a uma viagem.
        Retorna (True, mensagem) em caso de sucesso, (False, erro) em caso de falha.
        """
        return self.service.cadastrar_despesa(viagem_id, assunto, valor, data, comprovante, nome_arquivo)

    def listar_despesas(self):
        """
        Lista todas as despesas do sistema.
        """
        return self.service.listar_despesas()

    def listar_despesas_por_viagem(self, viagem_id):
        """
        Lista todas as despesas vinculadas a uma viagem específica.
        """
        return self.service.listar_despesas_por_viagem(viagem_id)

    def buscar_despesa(self, despesa_id):
        """
        Busca uma despesa pelo seu ID.
        Retorna (True, despesa) se encontrada, (False, erro) se não encontrada.
        """
        return self.service.buscar_despesa(despesa_id)

    def atualizar_despesa(self, despesa_id, viagem_id, assunto, valor, data, comprovante, nome_arquivo=None):
        """
        Atualiza os dados de uma despesa existente.
        Retorna (True, mensagem) em caso de sucesso, (False, erro) em caso de falha.
        """
        return self.service.atualizar_despesa(despesa_id, viagem_id, assunto, valor, data, comprovante, nome_arquivo)

    def remover_despesa(self, despesa_id):
        """
        Remove uma despesa pelo seu ID.
        Retorna (True, mensagem) em caso de sucesso, (False, erro) em caso de falha.
        """
        return self.service.remover_despesa(despesa_id)
