import json
import pandas as pd
from datetime import datetime
from typing import List, Tuple
from collections import defaultdict
import unicodedata
import emoji
from collections import Counter
from typing import List, Tuple
import re


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

# Pregunta 2
def q2_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Función para contar los emojis más usados en un conjunto de tweets.
    Esta función se optimiza para el tiempo, cargando todos los emojis en memoria antes de calcular los más comunes.
    
    Args:
        file_path: Ruta al archivo JSON que contiene los tweets.
        
    Returns:
        Una lista de tuplas que contiene los 10 emojis más comunes y sus respectivos conteos.
    """
    emoji_count = Counter()
    
    with open(file_path, 'r') as file:
        for line in file:
            tweet = json.loads(line)
            # Normalizando y decodificando el texto del tweet para identificar correctamente los emojis
            tweet_text = unicodedata.normalize('NFKD', tweet.get('content', '')).encode('utf-16', 'surrogatepass').decode('utf-16')
            
            # Obteniendo la lista de emojis del texto del tweet
            emoji_pattern = list(map(lambda x: x['emoji'], emoji.emoji_list(tweet_text)))
            
            # Contando la ocurrencia de cada emoji
            for char in emoji_pattern:
                emoji_count[char] += 1
                    
    return emoji_count.most_common(10)

# Pregunta 3

def q3_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Esta función está diseñada para optimizar el tiempo de ejecución,
    y devuelve los 10 usuarios más mencionados en el conjunto de tweets.
    
    Args:
        file_path: La ruta al archivo que contiene los datos de los tweets.
        
    Returns:
        Una lista de tuplas con el nombre del usuario y el número de menciones,
        ordenada en orden descendente de menciones.
    """
    mentions_count = Counter()
    
    with open(file_path, 'r') as file:
        for line in file:
            tweet = json.loads(line)
            tweet_text = tweet.get('content', '')
            mentions = re.findall(r"@(\w+)", tweet_text)  # Encuentra todas las menciones en el texto del tweet
            mentions_count.update(mentions)  # Actualiza el contador con las menciones encontradas
    
    # Retorna las 10 menciones más comunes
    return mentions_count.most_common(10)
