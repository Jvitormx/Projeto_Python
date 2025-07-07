
# service/despesa_service.py
# Service para regras de negócio e validação de Despesa
from models.despesa import Despesa
from models.viagem import Viagem
import mimetypes
import os
from datetime import datetime

class DespesaService:
    def __init__(self):
        pass

    def cadastrar_despesa(self, viagem_id, assunto, valor, data, comprovante, nome_arquivo=None):
        # Validação de campos obrigatórios
        if not viagem_id or not assunto or not valor or not data or not comprovante:
            return False, "Todos os campos são obrigatórios."

        # Validação de valor
        try:
            valor = float(valor)
            if valor <= 0:
                return False, "O valor da despesa deve ser positivo."
        except Exception:
            return False, "Valor inválido."

        # Validação de data
        try:
            datetime.strptime(data, "%Y-%m-%d")
        except Exception:
            return False, "Data inválida. Use o formato YYYY-MM-DD."

        # Validação de comprovante (PDF ou imagem)
        if nome_arquivo:
            mimetype, _ = mimetypes.guess_type(nome_arquivo)
            if not mimetype or not (mimetype.startswith('image/') or mimetype == 'application/pdf'):
                return False, "Comprovante deve ser PDF ou imagem."

        # Verifica se a viagem existe e está confirmada/em andamento
        v = Viagem.buscar_por_id(viagem_id)
        if not v:
            return False, "Viagem não encontrada."
        if v.status not in ['confirmada', 'em andamento']:
            return False, "Só é possível registrar despesas para viagens confirmadas ou em andamento."

        # Validação de orçamento (não exceder o orcamento_aprovado da viagem)
        orcamento = v.orcamento_aprovado if v.orcamento_aprovado is not None else 0
        despesas = Despesa.listar_por_viagem(viagem_id)
        total = sum(float(d.valor) for d in despesas) + valor
        if orcamento > 0 and total > orcamento:
            return False, "Despesa excede o orçamento aprovado da viagem."

        try:
            nova_despesa = Despesa(viagem_id=viagem_id, assunto=assunto, valor=valor, data=data, comprovante=comprovante)
            nova_despesa.salvar()
            return True, "Despesa registrada com sucesso."
        except Exception as e:
            return False, f"Erro ao registrar despesa: {str(e)}"

    def listar_despesas(self):
        return Despesa.listar_todas()

    def listar_despesas_por_viagem(self, viagem_id):
        return Despesa.listar_por_viagem(viagem_id)

    def buscar_despesa(self, despesa_id):
        d = Despesa.buscar_por_id(despesa_id)
        if d:
            return True, d
        else:
            return False, "Despesa não encontrada."

    def atualizar_despesa(self, despesa_id, viagem_id, assunto, valor, data, comprovante, nome_arquivo=None):
        # Repete as validações do cadastro
        if not viagem_id or not assunto or not valor or not data or not comprovante:
            return False, "Todos os campos são obrigatórios."
        try:
            valor = float(valor)
            if valor <= 0:
                return False, "O valor da despesa deve ser positivo."
        except Exception:
            return False, "Valor inválido."
        try:
            datetime.strptime(data, "%Y-%m-%d")
        except Exception:
            return False, "Data inválida. Use o formato YYYY-MM-DD."
        if nome_arquivo:
            mimetype, _ = mimetypes.guess_type(nome_arquivo)
            if not mimetype or not (mimetype.startswith('image/') or mimetype == 'application/pdf'):
                return False, "Comprovante deve ser PDF ou imagem."
        v = Viagem.buscar_por_id(viagem_id)
        if not v:
            return False, "Viagem não encontrada."
        if v.status not in ['confirmada', 'em andamento']:
            return False, "Só é possível registrar despesas para viagens confirmadas ou em andamento."
        orcamento = v.orcamento_aprovado if v.orcamento_aprovado is not None else 0
        despesas = Despesa.listar_por_viagem(viagem_id)
        total = sum(float(d.valor) for d in despesas if d.id != despesa_id) + valor
        if orcamento > 0 and total > orcamento:
            return False, "Despesa excede o orçamento aprovado da viagem."
        try:
            d = Despesa.buscar_por_id(despesa_id)
            if not d:
                return False, "Despesa não encontrada."
            d.viagem_id = viagem_id
            d.assunto = assunto
            d.valor = valor
            d.data = data
            d.comprovante = comprovante
            d.salvar()
            return True, "Despesa atualizada com sucesso."
        except Exception as e:
            return False, f"Erro ao atualizar despesa: {str(e)}"

    def remover_despesa(self, despesa_id):
        try:
            d = Despesa.buscar_por_id(despesa_id)
            if not d:
                return False, "Despesa não encontrada."
            d.remover()
            return True, "Despesa removida com sucesso."
        except Exception as e:
            return False, f"Erro ao remover despesa: {str(e)}"
