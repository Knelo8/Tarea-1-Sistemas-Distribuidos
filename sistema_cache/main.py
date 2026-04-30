from fastapi import FastAPI, HTTPException
import redis
import httpx
import json
import time
import os

app = FastAPI()

# Conexión a Redis
cache = redis.Redis(host='redis_cache', port=6379, db=0, decode_responses=True)

# URLs
URL_RESPUESTAS = "http://generador_respuestas:8000"
URL_METRICAS = "http://sistema_metricas:8000"

# Time To Live en segundos
TTL_DEFAULT = int(os.getenv("CACHE_TTL", 60))

async def registrar_metrica(tipo: str, consulta: str, latencia_ms: float):
    """Envía el registro al Sistema de Métricas de forma asíncrona."""
    evento = {
        "tipo": tipo,
        "consulta": consulta,
        "latencia_ms": latencia_ms
    }
    async with httpx.AsyncClient() as client:
        try:
            await client.post(f"{URL_METRICAS}/log", json=evento)
        except Exception as e:
            print(f"Error enviando métrica: {e}")

@app.get("/q1/{zone_id}")
async def proxy_q1(zone_id: str, confidence_min: float = 0.0):
    start_time = time.time()
    consulta_tipo = "Q1"
    
    # Generar la Cache Key
    cache_key = f"count:{zone_id}:conf={confidence_min}"
    
    # Existe?
    cached_response = cache.get(cache_key)
    
    if cached_response:
        # HIT
        latencia = (time.time() - start_time) * 1000
        await registrar_metrica("hit", consulta_tipo, latencia)
        return json.loads(cached_response)
    
    # MISS
    async with httpx.AsyncClient() as client:
        try:
            respuesta = await client.get(f"{URL_RESPUESTAS}/q1/{zone_id}?confidence_min={confidence_min}")
            respuesta.raise_for_status()
            datos = respuesta.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail="Error en Generador de Respuestas")
            
    # Almacenar resultado
    cache.setex(cache_key, TTL_DEFAULT, json.dumps(datos))
    
    # Registrar Miss en Métricas y retornar
    latencia = (time.time() - start_time) * 1000
    await registrar_metrica("miss", consulta_tipo, latencia)
    
    return datos

@app.get("/q2/{zone_id}")
async def proxy_q2(zone_id: str, confidence_min: float = 0.0):
    start_time = time.time()
    consulta_tipo = "Q2"
    
    cache_key = f"area:{zone_id}:conf={confidence_min}"
    cached_response = cache.get(cache_key)
    
    if cached_response:
        latencia = (time.time() - start_time) * 1000
        await registrar_metrica("hit", consulta_tipo, latencia)
        return json.loads(cached_response)
    
    async with httpx.AsyncClient() as client:
        try:
            respuesta = await client.get(f"{URL_RESPUESTAS}/q2/{zone_id}?confidence_min={confidence_min}")
            respuesta.raise_for_status()
            datos = respuesta.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail="Error en Generador de Respuestas")
            
    cache.setex(cache_key, TTL_DEFAULT, json.dumps(datos))
    
    latencia = (time.time() - start_time) * 1000
    await registrar_metrica("miss", consulta_tipo, latencia)
    
    return datos

@app.get("/q3/{zone_id}")
async def proxy_q3(zone_id: str, confidence_min: float = 0.0):
    start_time = time.time()
    consulta_tipo = "Q3"
    
    # Cache key: density:{zona_id}:conf={confidence_min}
    cache_key = f"density:{zone_id}:conf={confidence_min}"
    cached_response = cache.get(cache_key)
    
    if cached_response:
        latencia = (time.time() - start_time) * 1000
        await registrar_metrica("hit", consulta_tipo, latencia)
        return json.loads(cached_response)
    
    async with httpx.AsyncClient() as client:
        try:
            respuesta = await client.get(f"{URL_RESPUESTAS}/q3/{zone_id}?confidence_min={confidence_min}")
            respuesta.raise_for_status()
            datos = respuesta.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail="Error en Generador de Respuestas")
            
    cache.setex(cache_key, TTL_DEFAULT, json.dumps(datos))
    
    latencia = (time.time() - start_time) * 1000
    await registrar_metrica("miss", consulta_tipo, latencia)
    return datos


@app.get("/q4/{zone_a}/{zone_b}")
async def proxy_q4(zone_a: str, zone_b: str, confidence_min: float = 0.0):
    start_time = time.time()
    consulta_tipo = "Q4"
    
    cache_key = f"compare:density:{zone_a}:{zone_b}:conf={confidence_min}"
    cached_response = cache.get(cache_key)
    
    if cached_response:
        latencia = (time.time() - start_time) * 1000
        await registrar_metrica("hit", consulta_tipo, latencia)
        return json.loads(cached_response)
    
    async with httpx.AsyncClient() as client:
        try:
            respuesta = await client.get(f"{URL_RESPUESTAS}/q4/{zone_a}/{zone_b}?confidence_min={confidence_min}")
            respuesta.raise_for_status()
            datos = respuesta.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail="Error en Generador de Respuestas")
            
    cache.setex(cache_key, TTL_DEFAULT, json.dumps(datos))
    
    latencia = (time.time() - start_time) * 1000
    await registrar_metrica("miss", consulta_tipo, latencia)
    return datos


@app.get("/q5/{zone_id}")
async def proxy_q5(zone_id: str, bins: int = 5):
    start_time = time.time()
    consulta_tipo = "Q5"
    
    cache_key = f"confidence_dist:{zone_id}:bins={bins}"
    cached_response = cache.get(cache_key)
    
    if cached_response:
        latencia = (time.time() - start_time) * 1000
        await registrar_metrica("hit", consulta_tipo, latencia)
        return json.loads(cached_response)
    
    async with httpx.AsyncClient() as client:
        try:
            # Q5 utiliza un parámetro diferente (bins)
            respuesta = await client.get(f"{URL_RESPUESTAS}/q5/{zone_id}?bins={bins}")
            respuesta.raise_for_status()
            datos = respuesta.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail="Error en Generador de Respuestas")
            
    cache.setex(cache_key, TTL_DEFAULT, json.dumps(datos))
    
    latencia = (time.time() - start_time) * 1000
    await registrar_metrica("miss", consulta_tipo, latencia)
    return datos