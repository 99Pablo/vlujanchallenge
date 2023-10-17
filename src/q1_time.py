
import pandas as pd
from datetime import datetime
from typing import List, Tuple
from collections import defaultdict

from typing import List, Tuple


def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Esta función busca optimizar el tiempo de procesamiento de los datos
    al leer el archivo completo una sola vez usando Pandas,
    para luego realizar las transformaciones necesarias.

    Args:
        file_path: La ruta al archivo JSON que contiene los datos de los tweets.

    Returns:
        Una lista de tuplas con las top 10 fechas con más tweets y el usuario que más publicó en cada fecha.
    """
    # Leer el archivo JSON
    df = pd.read_json(file_path, lines=True)
    
    # Crear un diccionario para almacenar el conteo de tweets por usuario y fecha
    date_user_count = defaultdict(lambda: defaultdict(int))
    
    # Iterar sobre el DataFrame y contar los tweets por usuario y fecha
    for index, row in df.iterrows():
        date = row['date'].date()
        user = row['user']['username']
        date_user_count[date][user] += 1
    
    # Encontrar las top 10 fechas y el usuario que más publicó en cada una
    top_dates = []
    for date in sorted(date_user_count.keys(), key=lambda d: sum(date_user_count[d].values()), reverse=True)[:10]:
        user = max(date_user_count[date], key=date_user_count[date].get)
        top_dates.append((date, user))
        
    return top_dates