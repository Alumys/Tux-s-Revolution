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
    Toma un nombre y un puntaje, lo agrega al ranking existente,
    ordena la lista, mantiene solo el TOP 5 y guarda todo en el JSON.
    """
    # 1. Cargar los puntajes que ya existen
    lista_ranking = cargar_ranking()
    
    # 2. Crear el nuevo registro (un diccionario)
    nuevo_registro = {"nombre": nombre, "puntos": puntaje}
    lista_ranking.append(nuevo_registro)
    
    # 3. Ordenar la lista por puntos de mayor a menor.
    # Usamos itemgetter, que es una forma eficiente y permitida de ordenar diccionarios sin usar lambda.
    from operator import itemgetter
    # 'reverse=True' es para que sea de mayor a menor
    lista_ranking.sort(key=itemgetter("puntos"), reverse=True)
    
    # 4. Mantener solo los mejores 5 (Top 5)
    # Esto corta la lista desde el inicio hasta el elemento 5
    top_5 = lista_ranking[:5]
    
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