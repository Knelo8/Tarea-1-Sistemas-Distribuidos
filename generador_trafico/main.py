import requests
import numpy as np
import time
import random
import os

# Configuración del generador
URL_CACHE = "http://sistema_cache:8000"
ZONAS = ["Z1", "Z2", "Z3", "Z4", "Z5"]
TIPOS_CONSULTA = ["Q1", "Q2", "Q3", "Q4", "Q5"]

# Uniforme o Zipf
DISTRIBUCION_ACTUAL = os.getenv("DISTRIBUCION", "zipf") 
TIEMPO_ESPERA_SEG = 0.5 # Tiempo entre cada petición (tasa de arribo)

def elegir_zona(distribucion):
    """Elige una zona basándose en la distribución seleccionada."""
    if distribucion == "uniforme":
        # Todas las zonas tienen la misma probabilidad
        return random.choice(ZONAS)
    elif distribucion == "zipf":
        rango = np.random.zipf(a=1.5) 
        indice = min(rango - 1, len(ZONAS) - 1)
        return ZONAS[indice]

def generar_peticion():
    """Construye y envía una petición aleatoria a la Caché."""
    consulta = random.choice(TIPOS_CONSULTA)
    zona = elegir_zona(DISTRIBUCION_ACTUAL)
    confianza = random.choice([0.0, 0.5, 0.8]) # Simulamos distintos parámetros
    
    try:
        if consulta == "Q1":
            requests.get(f"{URL_CACHE}/q1/{zona}?confidence_min={confianza}")
        elif consulta == "Q2":
            requests.get(f"{URL_CACHE}/q2/{zona}?confidence_min={confianza}")
        elif consulta == "Q3":
            requests.get(f"{URL_CACHE}/q3/{zona}?confidence_min={confianza}")
        elif consulta == "Q4":
            zona_b = elegir_zona(DISTRIBUCION_ACTUAL)
            requests.get(f"{URL_CACHE}/q4/{zona}/{zona_b}?confidence_min={confianza}")
        elif consulta == "Q5":
            bins = random.choice([5, 10])
            requests.get(f"{URL_CACHE}/q5/{zona}?bins={bins}")
            
        print(f"Enviada {consulta} para {zona} (Dist: {DISTRIBUCION_ACTUAL})")
    except requests.exceptions.RequestException as e:
        print(f"Error conectando a la caché: {e}")

if __name__ == "__main__":
    print("Iniciando Generador de Tráfico...")
    # Esperamos unos segundos
    time.sleep(5) 
    
    while True:
        generar_peticion()
        time.sleep(TIEMPO_ESPERA_SEG)