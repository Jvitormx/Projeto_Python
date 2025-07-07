
# service/despesa_service.py
# Service para regras de negócio e validação de Despesa
from models import despesa, viagem
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
        v = viagem.buscar_viagem_por_id(viagem_id)
        if not v:
            return False, "Viagem não encontrada."
        if v[6] not in ['confirmada', 'em andamento']:
            return False, "Só é possível registrar despesas para viagens confirmadas ou em andamento."

        # Validação de orçamento (não exceder o orcamento_aprovado da viagem)
        orcamento = v[7] if v[7] is not None else 0
        despesas = self.listar_despesas_por_viagem(viagem_id)
        total = sum(float(d[3]) for d in despesas) + valor
        if orcamento > 0 and total > orcamento:
            return False, "Despesa excede o orçamento aprovado da viagem."

        try:
            despesa.inserir_despesa(viagem_id, assunto, valor, data, comprovante)
            return True, "Despesa registrada com sucesso."
        except Exception as e:
            return False, f"Erro ao registrar despesa: {str(e)}"

    def listar_despesas(self):
        return despesa.listar_despesas()

    def listar_despesas_por_viagem(self, viagem_id):
        return [d for d in despesa.listar_despesas() if d[1] == viagem_id]

    def buscar_despesa(self, despesa_id):
        d = despesa.buscar_despesa_por_id(despesa_id)
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
        v = viagem.buscar_viagem_por_id(viagem_id)
        if not v:
            return False, "Viagem não encontrada."
        if v[6] not in ['confirmada', 'em andamento']:
            return False, "Só é possível registrar despesas para viagens confirmadas ou em andamento."
        orcamento = v[7] if v[7] is not None else 0
        despesas = self.listar_despesas_por_viagem(viagem_id)
        total = sum(float(d[3]) for d in despesas if d[0] != despesa_id) + valor
        if orcamento > 0 and total > orcamento:
            return False, "Despesa excede o orçamento aprovado da viagem."
        try:
            despesa.atualizar_despesa(despesa_id, viagem_id, assunto, valor, data, comprovante)
            return True, "Despesa atualizada com sucesso."
        except Exception as e:
            return False, f"Erro ao atualizar despesa: {str(e)}"

    def remover_despesa(self, despesa_id):
        try:
            despesa.remover_despesa(despesa_id)
            return True, "Despesa removida com sucesso."
        except Exception as e:
            return False, f"Erro ao remover despesa: {str(e)}"
