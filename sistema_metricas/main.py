from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import time

app = FastAPI()

# Modelo de datos que esperamos recibir desde la Caché
class MetricEvent(BaseModel):
    tipo: str  # Puede ser "hit", "miss" o "eviction"
    consulta: str # Ej: "Q1", "Q2"
    latencia_ms: float

# Base de datos en memoria para los logs
logs_eventos: List[MetricEvent] = []

@app.post("/log")
def registrar_evento(evento: MetricEvent):
    """Recibe un evento desde la caché y lo guarda."""
    logs_eventos.append(evento)
    return {"status": "ok"}

@app.get("/stats")
def obtener_estadisticas():
    """Calcula las métricas."""
    total_hits = sum(1 for e in logs_eventos if e.tipo == "hit")
    total_misses = sum(1 for e in logs_eventos if e.tipo == "miss")
    total_consultas = total_hits + total_misses
    
    # Cálculo del Hit Rate
    hit_rate = 0.0
    if total_consultas > 0:
        hit_rate = total_hits / total_consultas
        
    # Latencia promedio
    latencias = [e.latencia_ms for e in logs_eventos if e.tipo in ("hit", "miss")]
    avg_latencia = sum(latencias) / len(latencias) if latencias else 0.0

    return {
        "total_eventos": len(logs_eventos),
        "hits": total_hits,
        "misses": total_misses,
        "hit_rate": round(hit_rate, 4),
        "latencia_promedio_ms": round(avg_latencia, 2)
    }

@app.delete("/reset")
def limpiar_metricas():
    """Útil para limpiar los datos entre un experimento y otro."""
    logs_eventos.clear()
    return {"status": "limpio"}