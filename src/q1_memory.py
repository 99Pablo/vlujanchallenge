import json

from datetime import datetime
from typing import List, Tuple
from collections import defaultdict


from typing import List, Tuple


def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Esta función busca optimizar la memoria utilizada al procesar los datos
    al leer el archivo línea por línea y contar los tweets por usuario y fecha
    durante la lectura, evitando cargar todo el archivo en memoria.

    Args:
        file_path: La ruta al archivo JSON que contiene los datos de los tweets.

    Returns:
        Una lista de tuplas con las top 10 fechas con más tweets y el usuario que más publicó en cada fecha.
    """
    # Crear un diccionario para almacenar el conteo de tweets por usuario y fecha
    date_user_count = defaultdict(lambda: defaultdict(int))
    
    # Leer el archivo línea por línea y contar los tweets por usuario y fecha
    with open(file_path, 'r') as file:
        for line in file:
            # Convertir la línea JSON en un diccionario
            tweet = json.loads(line)
            date = datetime.strptime(tweet['date'], '%Y-%m-%dT%H:%M:%S%z').date()
            user = tweet['user']['username']
            date_user_count[date][user] += 1
    
    # Encontrar las top 10 fechas y el usuario que más publicó en cada una
    top_dates = []
    for date in sorted(date_user_count.keys(), key=lambda d: sum(date_user_count[d].values()), reverse=True)[:10]:
        user = max(date_user_count[date], key=date_user_count[date].get)
        top_dates.append((date, user))
        
    return top_dates