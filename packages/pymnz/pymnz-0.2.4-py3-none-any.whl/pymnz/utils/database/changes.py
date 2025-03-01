from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent


def unique_column(conn, table_name, key_col):
    """Alterar coluna para que seja única"""

    # Definir caminho do SQL
    PATH = ROOT_DIR / 'sql' / 'unique_columns.sql'

    # Abrir arquivo SQL
    with open(PATH, 'r', encoding='utf-8') as file:
        query = file.read()

    # Executar query
    params = {'table_name', table_name, 'key_col', key_col}
    result = conn.execute(query, params)

    return result.scalar()


def id_autoincrement(conn, table_name):
    """Alterar tabela para adicionar a coluna 'id' com autoincrement"""
    # Definir caminho do SQL
    PATH = ROOT_DIR / 'sql' / 'id_autoincrement.sql'

    # Abrir arquivo SQL
    with open(PATH, 'r', encoding='utf-8') as file:
        query = file.read()

    # Executar query
    params = {'table_name': table_name}
    result = conn.execute(query, params)

    return result.scalar()
