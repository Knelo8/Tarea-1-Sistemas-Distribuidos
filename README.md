# Tarea-1-Sistemas-Distribuidos

Este proyecto consiste en el diseño e implementación de un sistema distribuido para el procesamiento eficiente de consultas geoespaciales sobre el dataset Google Open Buildings. La arquitectura utiliza microservicios contenerizados y un sistema de caché basado en Redis para optimizar los tiempos de respuesta y el uso de recursos ante distintos patrones de carga.

## Arquitectura del Sistema

La arquitectura se basa en módulos independientes y cohesivos que interactúan de manera secuencial para garantizar la escalabilidad y portabilidad del entorno.

*   **Generador de Tráfico:** Simula solicitudes de empresas de logística utilizando distribuciones de probabilidad Uniforme y de Ley de Potencia (Zipf).
*   **Sistema de Caché:** Proxy interceptor implementado en FastAPI que gestiona la lógica de aciertos (hits) y fallos (misses) consultando a Redis.
*   **Generador de Respuestas:** Módulo encargado del procesamiento de las consultas (Q1 a Q5) directamente en memoria RAM al iniciar el servicio.
*   **Almacenamiento de Métricas:** Servicio centralizado que recolecta latencias, tasas de acierto y throughput para análisis técnico.
*   **Dashboard:** Interfaz gráfica desarrollada en Streamlit para la visualización de métricas en tiempo real.

## Requisitos del Sistema

Para garantizar la reproducibilidad del entorno, se requiere el uso de Docker como tecnología de virtualización.

*   Docker Engine
*   Docker Compose V2

## Instrucciones de Despliegue

Para la construcción y ejecución de todos los servicios implementados, ejecute el siguiente comando en la raíz del repositorio:
```bash
docker compose up --build

Una vez que el despliegue finalice, las interfaces estarán disponibles en las siguientes direcciones:

Dashboard Visual: http://localhost:8501

Sistema de Métricas (JSON): http://localhost:8001/stats

Interceptor de Caché: http://localhost:8003

Configuraciones Experimentales
El sistema permite la evaluación del rendimiento bajo distintos escenarios de configuración definidos en el enunciado:

Distribuciones de Tráfico: Modificables mediante la variable de entorno DISTRIBUCION en el servicio generador_trafico (Uniforme o Zipf).

Políticas de Remoción: Configurables en el archivo redis.conf mediante la directiva maxmemory-policy (LRU, LFU, FIFO).

Tamaño de Memoria: Ajustable en redis.conf mediante el parámetro maxmemory (e.g., 50MB, 200MB, 500MB).

Tiempo de Vida (TTL): Configurable mediante la variable de entorno CACHE_TTL en el servicio sistema_cache.
