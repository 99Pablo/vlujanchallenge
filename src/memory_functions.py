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


def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Función para contar los emojis más usados en un conjunto de tweets.
    Esta función se optimiza para la memoria, calculando los emojis más comunes sin cargar todos en memoria.
    
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
    
    # Calculando los top 10 emojis sin almacenar la lista completa en memoria
    top_10_emojis = []
    for em, count in emoji_count.items():
        if len(top_10_emojis) < 10:
            top_10_emojis.append((em, count))
            top_10_emojis.sort(key=lambda x: x[1], reverse=True)
        elif count > top_10_emojis[-1][1]:
            top_10_emojis[-1] = (em, count)
            top_10_emojis.sort(key=lambda x: x[1], reverse=True)
            
    return top_10_emojis
    

def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Esta función está diseñada para optimizar la memoria utilizada.
    Calcula los 10 usuarios más mencionados, evitando almacenar toda la lista de menciones en memoria.
    
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
    
    # Calculando el top 10 sin almacenar toda la lista de menciones en memoria
    top_10_mentions = []
    for mention, count in mentions_count.items():
        if len(top_10_mentions) < 10:
            top_10_mentions.append((mention, count))
            top_10_mentions.sort(key=lambda x: x[1], reverse=True)  # Ordena la lista cada vez que se añade un nuevo elemento
        elif count > top_10_mentions[-1][1]:  # Si el conteo de menciones es mayor al último elemento de la lista top 10
            top_10_mentions[-1] = (mention, count)  # Reemplaza el último elemento
            top_10_mentions.sort(key=lambda x: x[1], reverse=True)  # Vuelve a ordenar la lista
            
    return top_10_mentions
