import json

from typing import List, Tuple

from collections import Counter
from typing import List, Tuple
import re

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
