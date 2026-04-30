from fastapi import FastAPI, HTTPException
import numpy as np

app = FastAPI()

# 1. Precarga de Datos en memoria
# Para simplificar, usamos una clase básica que represente cada fila del dataset
class BuildingRecord:
    def __init__(self, confidence: float, area: float):
        self.confidence = confidence
        self.area = area

# Simulamos las áreas en km2 de las zonas predefinidas (Z1 a Z5)
zone_area_km2 = {
    "Z1": 14.4,  # Providencia
    "Z2": 99.4,  # Las Condes
    "Z3": 133.0, # Maipú
    "Z4": 22.4,  # Santiago Centro
    "Z5": 197.0  # Pudahuel
}

# Simulamos la carga en memoria del Google Open Buildings [cite: 90]
data = {
    "Z1": [BuildingRecord(0.8, 120), BuildingRecord(0.5, 90), BuildingRecord(0.9, 150)],
    "Z2": [BuildingRecord(0.9, 200), BuildingRecord(0.7, 150)],
    "Z3": [BuildingRecord(0.6, 100), BuildingRecord(0.4, 80)],
    "Z4": [BuildingRecord(0.85, 80), BuildingRecord(0.4, 60)],
    "Z5": [BuildingRecord(0.95, 300)]
}

# 2. Implementación de Consultas

@app.get("/q1/{zone_id}")
def q1_count(zone_id: str, confidence_min: float = 0.0):
    """Conteo de edificios en una zona [cite: 98]"""
    if zone_id not in data:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    
    records = data[zone_id]
    count = sum(1 for r in records if r.confidence >= confidence_min) # [cite: 106]
    return {"zone": zone_id, "count": count}


@app.get("/q2/{zone_id}")
def q2_area(zone_id: str, confidence_min: float = 0.0):
    """Área promedio y área total de edificaciones [cite: 109]"""
    if zone_id not in data:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    
    areas = [r.area for r in data[zone_id] if r.confidence >= confidence_min] # [cite: 115]
    if not areas:
        return {"avg_area": 0, "total_area": 0, "n": 0}
    
    return {
        "avg_area": sum(areas) / len(areas), 
        "total_area": sum(areas),            
        "n": len(areas)                      
    }


@app.get("/q3/{zone_id}")
def q3_density(zone_id: str, confidence_min: float = 0.0):
    """Densidad de edificaciones por km2 [cite: 122]"""
    if zone_id not in data or zone_id not in zone_area_km2:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    
    # Reutilizamos la lógica de Q1
    count = sum(1 for r in data[zone_id] if r.confidence >= confidence_min)
    area_km2 = zone_area_km2[zone_id]
    
    return {"zone": zone_id, "density": count / area_km2}


@app.get("/q4/{zone_a}/{zone_b}")
def q4_compare(zone_a: str, zone_b: str, confidence_min: float = 0.0):
    """Comparación de densidad entre dos zonas [cite: 134]"""
    try:
        da = q3_density(zone_a, confidence_min)["density"]
        db = q3_density(zone_b, confidence_min)["density"]
    except HTTPException:
        raise HTTPException(status_code=404, detail="Alguna de las zonas no existe")

    winner = zone_a if da > db else zone_b
    return {"zone_a": da, "zone_b": db, "winner": winner}


@app.get("/q5/{zone_id}")
def q5_confidence_dist(zone_id: str, bins: int = 5):
    """Distribución de confianza en una zona [cite: 146]"""
    if zone_id not in data:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    
    scores = [r.confidence for r in data[zone_id]] 
    counts, edges = np.histogram(scores, bins=bins, range=(0.0, 1.0)) 
    
    dist = [
        {
            "bucket": i, 
            "min": float(edges[i]), 
            "max": float(edges[i+1]), 
            "count": int(counts[i])
        } for i in range(bins) 
    ]
    
    return {"zone": zone_id, "distribution": dist}