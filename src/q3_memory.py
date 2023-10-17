import json

from typing import List, Tuple


from collections import Counter
from typing import List, Tuple
import re

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