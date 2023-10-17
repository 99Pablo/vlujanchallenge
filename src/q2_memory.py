import json

from typing import List, Tuple

import unicodedata
import emoji
from collections import Counter
from typing import List, Tuple



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