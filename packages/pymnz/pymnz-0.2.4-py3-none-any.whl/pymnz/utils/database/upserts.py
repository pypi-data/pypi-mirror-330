from .updates import update_table_from_dataframe
from .inspections import table_exists
from .changes import unique_column, id_autoincrement
import pandas as pd


def upsert_table_database(
    df: pd.DataFrame, conn, table_name, key_col
) -> int | None:
    """
    Insere ou atualiza registros de cercas na web.

    :param df: pandas.DataFrame contendo os dados a serem inseridos
    ou atualizados.
    :param conn: Conexão ativa com o banco de dados.
    :return: Número de linhas afetadas ou None.
    """
    # Substituir valores NaN por None
    df = df.where(pd.notnull(df), None)

    # Verifica se a tabela existe
    if not table_exists(conn, table_name):

        # Criar tabela usando pandas.to_sql
        df.to_sql(
            table_name,
            conn,
            if_exists='replace',
            index=False,
            chunksize=500,
        )

        # Definir uma coluna id com autoincrement
        id_autoincrement(conn, table_name)

        # Definir coluna key unique
        unique_column(conn, table_name, key_col)

        return len(df)  # Número de linhas inseridas

    # Atualizar a tabela existente em chunks
    chunksize = 1000

    # Para rastrear o total de linhas afetadas
    total_rows_affected = 0

    # Iterar sobre os chunks do DataFrame
    for start in range(0, len(df), chunksize):
        # Separar chunk
        chunk = df.iloc[start:start + chunksize]

        # Atualizar chunk
        rows_affected = update_table_from_dataframe(
            chunk, table_name, key_col, conn
        )

        # Somar as linhas afetadas
        total_rows_affected += rows_affected

    return total_rows_affected
