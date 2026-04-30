# Tarea-1-Sistemas-Distribuidos

Este proyecto consiste en el diseño e implementación de un sistema distribuido para el procesamiento eficiente de consultas geoespaciales sobre el dataset Google Open Buildings. La arquitectura utiliza microservicios contenerizados y un sistema de caché basado en Redis para optimizar los tiempos de respuesta y el uso de recursos ante patrones de carga variables.

## Arquitectura del Sistema

El diseño de la arquitectura está estructurado en módulos independientes y cohesivos para facilitar su mantenimiento y escalabilidad. Se definen los siguientes servicios principales:

*   **Generador de Tráfico:** Simula solicitudes de empresas de logística utilizando distribuciones de probabilidad Uniforme y de Ley de Potencia (Zipf).
*   **Sistema de Caché:** Actúa como un proxy interceptor que gestiona la lógica de aciertos (hits) y fallos (misses) mediante Redis. Implementa soporte nativo para TTL y políticas de evicción configurables como LRU, LFU o FIFO.
*   **Generador de Respuestas:** Módulo responsable del procesamiento de las consultas (Q1 a Q5). Los datos del dataset se cargan íntegramente en memoria RAM al iniciar el servicio para eliminar la latencia de I/O.
*   **Almacenamiento de Métricas:** Registra todos los eventos del sistema, incluyendo latencias, conteo de hits/misses, throughput y tasa de evicción.
*   **Dashboard de Visualización:** Interfaz gráfica que permite el monitoreo en tiempo real de las métricas relevantes del sistema.

## Requisitos Previos

Para la construcción y ejecución de este proyecto, es indispensable contar con las siguientes herramientas:

*   Docker Engine
*   Docker Compose V2

## Instrucciones de Despliegue

Para inicializar el sistema completo, ejecute el siguiente comando en la raíz del directorio del proyecto:
```bash
docker compose up --build
