# VisionLean | Smart Mobility & Computer Vision 🚦

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-00FF00?style=for-the-badge&logo=ultralytics&logoColor=black)

**VisionLean** es un sistema de análisis de tráfico inteligente que utiliza **Deep Learning** para transformar flujos de video en tiempo real en métricas accionables para la planificación urbana. El sistema automatiza el conteo y clasificación de vehículos y peatones, eliminando el error humano y optimizando la recolección de datos de movilidad.

---

## Características Principales

* **Detección Multiclase:** Identificación precisa de automóviles, motocicletas, buses, camiones y peatones utilizando **YOLOv8**.
* **Análisis Direccional (Counting Gates):** Implementación de líneas lógicas configurables para monitorear el flujo vehicular en direcciones específicas (Norte, Sur, Izquierda, Derecha).
* **Procesamiento en Tiempo Real:** Optimizado con **OpenCV** para manejar flujos de video con baja latencia.
* **Métricas de Impacto:** Generación de datos sobre densidad de tráfico y picos de flujo para la toma de decisiones basada en evidencia.

---

## Stack Técnico

* **Lenguaje:** Python 3.x
* **Visión Artificial:** OpenCV (Procesamiento de imagen y lógica de tracking).
* **IA & Deep Learning:** Ultralytics YOLOv8 (Inferencia de modelos).
* **Gestión de Datos:** NumPy / Pandas para el procesamiento de logs y métricas.

---

## Arquitectura del Sistema

El sistema opera bajo un flujo de tres capas:
1.  **Ingesta:** Captura de frames de video en vivo o archivos locales.
2.  **Inferencia:** El modelo YOLOv8 detecta y clasifica los objetos en cada frame.
3.  **Lógica de Conteo:** Se rastrea el centroide de cada objeto. Si el centroide cruza una "Counting Gate" (coordenadas de píxeles predefinidas), se registra el evento en la dirección correspondiente.

---

## Configuración e Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/vision-lean.git](https://github.com/tu-usuario/vision-lean.git)
   cd vision-lean
2. **Instalar dependencias:**
   ```Bash
   pip install ultralytics opencv-python numpy
