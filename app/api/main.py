from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

EVENT_FILE = "traffic_events.jsonl"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_events():
    try:
        return pd.read_json(EVENT_FILE, lines=True)
    except:
        return pd.DataFrame()


@app.get("/dashboard")
def dashboard():

    df = load_events()

    if df.empty:
        return {
            "kpis": {
                "vehicles_total": 0,
                "vehicles_per_minute": 0,
                "saturation": 0,
                "analysis_time": "00:00:00"
            },
            "gates": {},
            "vehicle_types": {},
            "flow_per_minute": []
        }

    # Vehículos
    vehicles = df[df["class"].isin(["car","bus","truck","motorcycle"])]

    vehicles_total = len(vehicles)

    # Duración análisis
    duration_seconds = df["time"].max()
    minutes = max(duration_seconds / 60, 1)

    vehicles_per_minute = round(vehicles_total / minutes, 2)

    # Saturación estimada (capacidad hipotética 120 veh/min)
    saturation = round((vehicles_per_minute /120) * 100)

    # Gates
    gates = vehicles.groupby("gate").size().to_dict()

    # Tipos de vehículos
    vehicle_types = vehicles.groupby("class").size().to_dict()

    # Flujo por minuto
    df["minute"] = (df["time"] // 60).astype(int)
    flow = df.groupby("minute").size().reset_index(name="count")

    return {
        "kpis": {
            "vehicles_total": int(vehicles_total),
            "vehicles_per_minute": vehicles_per_minute,
            "saturation": saturation,
            "analysis_time": str(pd.to_timedelta(duration_seconds, unit="s"))
        },
        "gates": gates,
        "vehicle_types": vehicle_types,
        "flow_per_minute": flow.to_dict(orient="records")
    }

@app.get("/logs")
def get_logs():
    df = load_events()
    
    if df.empty:
        return []

    # 1. Filtramos solo vehículos válidos
    vehicles = df[df["class"].isin(["car", "bus", "truck", "motorcycle"])]
    
    # 2. Tomamos los últimos 10 eventos y ordenamos por tiempo (lo más nuevo arriba)
    latest_events = vehicles.sort_values(by="time", ascending=False).head(10)
    
    logs = []
    for _, row in latest_events.iterrows():
        # Formateamos el tiempo a HH:MM:SS basado en los segundos del video
        time_str = str(pd.to_timedelta(row["time"], unit="s")).split()[-1]
        
        logs.append({
            "id": int(row.get("track_id", 0)), # Si tienes track_id en tu jsonl
            "vehicle": row["class"],
            "gate": row["gate"].replace("Puerta_", ""),
            "time": time_str
        })
        
    return logs

