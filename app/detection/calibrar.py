import cv2

print("Modo calibración de puertas...")

video_path = "Video.mp4"
cap = cv2.VideoCapture(video_path)

w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

ret, frame = cap.read()
if not ret:
    print("No se pudo leer el video")
    exit()

gates = {
    "Puerta_Norte": { 
        "line": [(int(w*0.42), int(h*0.35)), (int(w*0.58), int(h*0.35))],
        "color": (255,165,0)
    },
    "Puerta_Sur": { 
        "line": [(int(w*0.50), int(h*0.85)), (int(w*0.70), int(h*0.85))],
        "color": (0,0,255)
    },
        "Puerta_Izquierda": { 
        "line": [(int(w*0.18), int(h*0.60)), (int(w*0.18), int(h*0.70))],
        "color": (255, 0, 0), "count": 0, "type": "vertical"
    },
    "Puerta_Derecha": { 
    "line": [(int(w*0.94), int(h*0.65)), (int(w*0.94), int(h*0.84))],
    "color": (0, 0, 255), "count": 0, "type": "vertical" 
},


}

for name, g in gates.items():
    cv2.line(frame, g["line"][0], g["line"][1], g["color"], 4)
    cv2.putText(frame, name, (g["line"][0][0], g["line"][0][1]-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, g["color"], 2)

cv2.imwrite("frame_calibracion.jpg", frame)

print("Frame guardado como frame_calibracion.jpg")
cap.release()