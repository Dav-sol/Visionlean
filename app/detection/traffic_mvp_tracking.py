import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO
import json
from collections import defaultdict

# 1. Configuración de Mobility IQ
print("Iniciando Mobility IQ: Sistema de Puertas Independientes...")
model = YOLO("yolov8n.pt")
video_path = "Video.mp4"
cap = cv2.VideoCapture(video_path)

# Dimensiones reales del video para evitar descuadres
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# 2. Definición de Puertas (Basado en tu dibujo de cuaderno)
# pt1 y pt2 definen los extremos de cada línea de conteo
gates = {
    "Puerta_Norte": { 
        "line": [(int(w*0.42), int(h*0.35)), (int(w*0.58), int(h*0.35))],
        "color": (255,165,0),
        "count": 0,
        "type": "horizontal"
    },

    "Puerta_Sur": { 
        "line": [(int(w*0.50), int(h*0.85)), (int(w*0.70), int(h*0.85))],
        "color": (0,0,255),
        "count": 0,
        "type": "horizontal"
    },

    "Puerta_Izquierda": { 
        "line": [(int(w*0.18), int(h*0.60)), (int(w*0.18), int(h*0.70))],
        "color": (255, 0, 0),
        "count": 0,
        "type": "vertical"
    },

    "Puerta_Derecha": { 
        "line": [(int(w*0.94), int(h*0.65)), (int(w*0.94), int(h*0.84))],
        "color": (0, 0, 255),
        "count": 0,
        "type": "vertical"
    }
}

INTERSECTION_ID = "BRQ_INT_01"
events_file = open("traffic_events.jsonl", "w")

counted_ids = set()
data_log = []
offset = 12 # Sensibilidad del cruce

out_video = cv2.VideoWriter("mobility_iq_gates_final.mp4", 
            cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    # Tracking con ByteTrack
    results = model.track(frame, persist=True, tracker="bytetrack.yaml", verbose=False)

    # Dibujar las Puertas (Líneas del dibujo)
    for name, g in gates.items():
        cv2.line(frame, g["line"][0], g["line"][1], g["color"], 4)
        cv2.putText(frame, name, (g["line"][0][0], g["line"][0][1]-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, g["color"], 2)

    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()
        ids = results[0].boxes.id.cpu().numpy().astype(int)
        clss = results[0].boxes.cls.cpu().numpy().astype(int)

        for box, track_id, cls in zip(boxes, ids, clss):
            x1, y1, x2, y2 = map(int, box)
            label = model.names[cls]
            
            # Filtro de clases: Vehículos y Personas
            if label not in ["car", "motorcycle", "bus", "truck", ]: continue

            # Usamos el punto central del objeto para el cruce de línea
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            base_y = y2

            

            for name, g in gates.items():
                if (track_id, name) in counted_ids: continue
                if "valid_classes" in g and label not in g["valid_classes"]: continue
                crossed = False
                p1, p2 = g["line"]
                if g["type"] == "box":
                    # Lógica de Caja: ¿Está el centro dentro del rectángulo?
                    bx1, by1, bx2, by2 = g["box"]
                    if bx1 < cx < bx2 and by1 < base_y < by2:
                        crossed = True
                # Lógica para Puertas Horizontales (Norte / Sur)
                elif g["type"] == "horizontal":
                    if p1[0] < cx < p2[0] and abs(base_y - p1[1]) < offset:
                        crossed = True
                
                # Lógica para Puertas Verticales (IZQ / Derecha)
                else:
                    if p1[1] < cy < p2[1] and abs(cx - p1[0]) < offset:
                        crossed = True
                if crossed:
                    g["count"] += 1
                    counted_ids.add((track_id, name))
                    data_log.append({
                        "id": track_id, 
                        "puerta": name, 
                        "clase": label, 
                        "tiempo": round(cap.get(cv2.CAP_PROP_POS_FRAMES)/fps, 2)
                    })
                    # Evento para JSONL
                    event = {
    "intersection": INTERSECTION_ID,
    "track_id": int(track_id),
    "gate": str(name),
    "class": str(label),
    "time": float(round(cap.get(cv2.CAP_PROP_POS_FRAMES)/fps, 2))
}
                    events_file.write(json.dumps(event) + "\n")
            # Dibujar BBox minimalista
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 1)


    out_video.write(frame)

cap.release()
out_video.release()
events_file.close()
pd.DataFrame(data_log).to_csv("conteo_puertas_mobility_iq.csv", index=False)
print("Análisis completado. CSV y Video generados.")