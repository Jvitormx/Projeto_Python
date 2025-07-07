import sqlite3
import os

DB_NAME = os.path.join(os.path.dirname(__file__), '..', 'data', 'viagens.db')

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS gestor (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nome TEXT NOT NULL,
      departamento TEXT
    );

    CREATE TABLE IF NOT EXISTS funcionario (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nome TEXT NOT NULL,
      departamento TEXT,
      funcao TEXT
    );

    CREATE TABLE IF NOT EXISTS tipo_viagem (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      motivo TEXT,
      quant_pessoal_max_estimado INTEGER,
      duracao_dias_max_estimado INTEGER,
      motivo_base TEXT,
      programacao_base TEXT
    );

    CREATE TABLE IF NOT EXISTS localidade (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      pais TEXT,
      numero_agencia INTEGER
    );

    CREATE TABLE IF NOT EXISTS localidade_cidade (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      cidade TEXT,
      localidade_id INTEGER,
      FOREIGN KEY(localidade_id) REFERENCES localidade(id)
    );

    CREATE TABLE IF NOT EXISTS requisicao_viagem (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      funcionario_id INTEGER,
      requisicao_orcamento REAL,
      quantidade_pessoal INTEGER,
      motivacao TEXT,
      programacao_viagem TEXT,
      FOREIGN KEY(funcionario_id) REFERENCES funcionario(id)
    );

    CREATE TABLE IF NOT EXISTS viagem (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      funcionario_id INTEGER NOT NULL,
      tipo_viagem_id INTEGER,
      localidade_id INTEGER,
      requisicao_id INTEGER,
      status TEXT DEFAULT 'pendente',
      data_saida TEXT,
      data_retorno TEXT,
      duracao_dias INTEGER,
      orcamento_aprovado REAL,
      FOREIGN KEY(funcionario_id) REFERENCES funcionario(id),
      FOREIGN KEY(tipo_viagem_id) REFERENCES tipo_viagem(id),
      FOREIGN KEY(localidade_id) REFERENCES localidade(id),
      FOREIGN KEY(requisicao_id) REFERENCES requisicao_viagem(id)
    );

    CREATE TABLE IF NOT EXISTS funcionario_viagem (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      funcionario_id INTEGER,
      viagem_id INTEGER,
      orcamento_pessoal REAL,
      FOREIGN KEY(funcionario_id) REFERENCES funcionario(id),
      FOREIGN KEY(viagem_id) REFERENCES viagem(id)
    );

    CREATE TABLE IF NOT EXISTS despesa (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      viagem_id INTEGER NOT NULL,
      assunto TEXT,
      valor REAL,
      data TEXT,
      comprovante BLOB,
      FOREIGN KEY(viagem_id) REFERENCES viagem(id)
    );
    """)

    conn.commit()
    conn.close()
