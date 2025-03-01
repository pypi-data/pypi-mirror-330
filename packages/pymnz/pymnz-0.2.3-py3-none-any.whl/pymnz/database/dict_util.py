
def replace_invalid_values(values: dict):
    """Função para substituir valores indesejados por None"""
    # Importar somente quando é necessário
    import pandas as pd

    if not isinstance(values, (dict, list)):
        raise TypeError("O argumento deve ser um dicionário ou lista")

    # Interagir com o dicionário
    for record in values:
        for key, value in record.items():
            # Substituir pd.NaT, np.nan, e datas inválidas por None
            if pd.isna(value):
                record[key] = None

    return values
