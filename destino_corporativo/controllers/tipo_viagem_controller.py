
# controllers/tipo_viagem_controller.py
# Controller para orquestrar operações de TipoViagem, integrando com o model tipo_viagem
from models.tipo_viagem import TipoViagem

def cadastrar_tipo_viagem(motivo, quant_pessoal_max_estimado, duracao_dias_max_estimado, motivo_base, programacao_base):
    """
    Controller para cadastrar um novo tipo de viagem.
    Retorna (status, mensagem).
    """
    if not motivo or quant_pessoal_max_estimado is None or duracao_dias_max_estimado is None:
        return False, "Motivo, quantidade máxima de pessoal e duração máxima são obrigatórios."
    try:
        quant_pessoal_max_estimado = int(quant_pessoal_max_estimado)
        duracao_dias_max_estimado = int(duracao_dias_max_estimado)
        if quant_pessoal_max_estimado <= 0 or duracao_dias_max_estimado <= 0:
            return False, "Quantidade máxima de pessoal e duração devem ser positivos."
    except Exception:
        return False, "Quantidade máxima de pessoal e duração devem ser números inteiros."
    try:
        novo_tipo = TipoViagem(
            motivo=motivo,
            quant_pessoal_max_estimado=quant_pessoal_max_estimado,
            duracao_dias_max_estimado=duracao_dias_max_estimado,
            motivo_base=motivo_base,
            programacao_base=programacao_base
        )
        novo_tipo.salvar()
        return True, "Tipo de viagem cadastrado com sucesso."
    except Exception as e:
        return False, f"Erro ao cadastrar tipo de viagem: {str(e)}"

def listar_tipos_viagem():
    """
    Controller para listar todos os tipos de viagem.
    Retorna lista de objetos TipoViagem.
    """
    return TipoViagem.listar_todos()

def buscar_tipo_viagem(tipo_viagem_id):
    """
    Controller para buscar um tipo de viagem pelo ID.
    Retorna (status, tipo_viagem ou mensagem).
    """
    tipo = TipoViagem.buscar_por_id(tipo_viagem_id)
    if tipo:
        return True, tipo
    else:
        return False, "Tipo de viagem não encontrado."

def atualizar_tipo_viagem(tipo_viagem_id, motivo, quant_pessoal_max_estimado, duracao_dias_max_estimado, motivo_base, programacao_base):
    """
    Controller para atualizar um tipo de viagem existente.
    Retorna (status, mensagem).
    """
    if not motivo or quant_pessoal_max_estimado is None or duracao_dias_max_estimado is None:
        return False, "Motivo, quantidade máxima de pessoal e duração máxima são obrigatórios."
    try:
        quant_pessoal_max_estimado = int(quant_pessoal_max_estimado)
        duracao_dias_max_estimado = int(duracao_dias_max_estimado)
        if quant_pessoal_max_estimado <= 0 or duracao_dias_max_estimado <= 0:
            return False, "Quantidade máxima de pessoal e duração devem ser positivos."
    except Exception:
        return False, "Quantidade máxima de pessoal e duração devem ser números inteiros."
    try:
        tipo = TipoViagem.buscar_por_id(tipo_viagem_id)
        if not tipo:
            return False, "Tipo de viagem não encontrado."
        tipo.motivo = motivo
        tipo.quant_pessoal_max_estimado = quant_pessoal_max_estimado
        tipo.duracao_dias_max_estimado = duracao_dias_max_estimado
        tipo.motivo_base = motivo_base
        tipo.programacao_base = programacao_base
        tipo.salvar()
        return True, "Tipo de viagem atualizado com sucesso."
    except Exception as e:
        return False, f"Erro ao atualizar tipo de viagem: {str(e)}"

def remover_tipo_viagem(tipo_viagem_id):
    """
    Controller para remover um tipo de viagem pelo ID.
    Retorna (status, mensagem).
    """
    try:
        tipo = TipoViagem.buscar_por_id(tipo_viagem_id)
        if not tipo:
            return False, "Tipo de viagem não encontrado."
        tipo.remover()
        return True, "Tipo de viagem removido com sucesso."
    except Exception as e:
        return False, f"Erro ao remover tipo de viagem: {str(e)}"
