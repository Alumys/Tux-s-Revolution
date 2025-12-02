import json
import os # Necesario para verificar si el archivo existe

# Nombre del archivo donde se guardarán los datos.
# Se creará en la carpeta principal del proyecto.
ARCHIVO_JSON = "ranking.json"

def cargar_ranking():
    """
    Lee el archivo JSON y devuelve la lista de los mejores puntajes.
    Si el archivo no existe o está dañado, devuelve una lista vacía.
    """
    # Verificamos si el archivo existe antes de intentar abrirlo
    if not os.path.exists(ARCHIVO_JSON):
        return [] # No hay ranking todavía
    
    try:
        with open(ARCHIVO_JSON, "r") as archivo:
            datos = json.load(archivo)
        return datos
    except (json.JSONDecodeError, IOError):
        print(f"Advertencia: No se pudo leer {ARCHIVO_JSON}. Se iniciará un ranking nuevo.")
        return []

def guardar_puntaje_en_ranking(nombre, puntaje):
    """
    Agrega un nuevo puntaje al ranking, lo ordena y guarda los 5 mejores.

    Esta función realiza los siguientes pasos:
    1. Carga el historial existente desde el archivo JSON.
    2. Agrega el puntaje actual del jugador.
    3. Ordena la lista de mayor a menor basándose en los puntos.
    4. Recorta la lista para mantener solo el Top 5.
    5. Sobrescribe el archivo JSON con la lista actualizada.

    Args:
        nombre (str): El nombre o apodo ingresado por el jugador.
        puntaje (int): La cantidad de puntos obtenidos en la partida.
    """
    
    lista_ranking = cargar_ranking() # 1. Cargar los puntajes que ya existen
    
    
    nuevo_registro = {"nombre": nombre, "puntos": puntaje} # 2. Crear el nuevo registro (un diccionario)
    lista_ranking.append(nuevo_registro)
    
    
    # 3. Ordenar la lista (Lógica principal de ordenamiento) Como tenemos una lista de diccionarios, sort() no sabe por qué campo ordenar.
    from operator import itemgetter # Usamos itemgetter("puntos") para indicarle que debe comparar los valores de la clave "puntos".
    lista_ranking.sort(key=itemgetter("puntos"), reverse=True) # 'reverse=True' es para que sea de mayor a menor
    
    # 4. Mantener solo los mejores 5 (Top 5)
    top_5 = lista_ranking[:5] # Usamos slicing de listas para quedarnos con los primeros 5 elementos.
    
    # 5. Guardar la lista actualizada en el archivo JSON
    try:
        with open(ARCHIVO_JSON, "w") as archivo:
            # indent=4 hace que el archivo JSON sea fácil de leer para humanos
            json.dump(top_5, archivo, indent=4)
        print(f"-> Puntaje de {nombre} ({puntaje} pts) guardado en el ranking.")
    except IOError:
        print("Error crítico: No se pudo guardar el puntaje en el archivo.")

# --- Bloque de prueba rápida ---
# Si ejecutas este archivo directamente, probará que el guardado funciona.
if __name__ == "__main__":
    print("Probando módulo de puntuaciones...")
    guardar_puntaje_en_ranking("JugadorPrueba", 1500)
    print("Ranking actual:", cargar_ranking())