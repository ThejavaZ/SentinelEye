import cv2
import os
import time
from datetime import datetime
from ultralytics import YOLO

class SecurityVideoProcessor:
    def __init__(self, model_path: str = "modules/inference/model.pt", snapshot_dir: str = "static/snapshots"):
        self.model_path = model_path
        self.snapshot_dir = snapshot_dir
        
        # Asegurar que el directorio de snapshots exista
        os.makedirs(self.snapshot_dir, exist_ok=True)
        
        # Cargar el modelo YOLO
        try:
            self.model = YOLO(self.model_path)
            print(f"[AI Processor] Modelo YOLO cargado exitosamente desde: {self.model_path}")
        except Exception as e:
            print(f"[AI Processor Error] No se pudo cargar el modelo YOLO: {e}")
            self.model = None

    def process_frame(self, frame, camera_id: int, confidence_threshold: float = 0.5):
        """
        Procesa un único frame con YOLO, detecta infracciones y guarda evidencia si aplica.
        Retorna una lista de incidentes detectados en este frame.
        """
        if self.model is None:
            return []

        # Ejecutar inferencia
        results = self.model(frame, verbose=False)
        detected_incidents = []

        for r in results:
            boxes = r.boxes
            for box in boxes:
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]

                # Filtro de confianza mínima
                if confidence < confidence_threshold:
                    continue

                # EJEMPLO DE LÓGICA DE INFRACCIÓN:
                # Supongamos que tu modelo detecta clases como 'no_helmet', 'no_vest', etc.
                # O si detectas personas y validas su equipo. Aquí atrapamos clases de infracción directa:
                violation_classes = ["no_helmet", "no_vest", "unauthorized_person"]
                
                # Si el nombre de la clase detectada está en nuestras infracciones objetivo:
                if class_name.lower() in violation_classes:
                    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    snapshot_filename = f"cam_{camera_id}_{class_name}_{timestamp_str}.jpg"
                    snapshot_path = os.path.join(self.snapshot_dir, snapshot_filename)

                    # Guardar la captura del frame con OpenCV
                    cv2.imwrite(snapshot_path, frame)

                    incident_data = {
                        "camera_id": camera_id,
                        "violation_type": class_name.upper(),
                        "snapshot_path": f"/static/snapshots/{snapshot_filename}",
                        "confidence_score": round(confidence, 2),
                        "detected_at": datetime.now().isoformat()
                    }
                    detected_incidents.append(incident_data)

        return detected_incidents

    def start_stream_simulation(self, camera_id: int, source=0, fps_limit: int = 1):
        """
        Simula o procesa un stream en bucle (ideal para pruebas locales con webcam o archivo de video).
        Procesa por lotes limitados por fps_limit para no saturar la CPU/GPU.
        """
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            print(f"[Stream Error] No se pudo abrir la fuente de video para la cámara {camera_id}")
            return

        print(f"[Stream] Iniciando procesamiento de video para la cámara {camera_id}...")
        
        prev_time = 0
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("[Stream] Fin del video o pérdida de señal.")
                    break

                # Controlar los FPS de procesamiento (ej. 1 frame por segundo para IA)
                current_time = time.time()
                if current_time - prev_time >= (1.0 / fps_limit):
                    prev_time = current_time
                    
                    incidents = self.process_frame(frame, camera_id)
                    if incidents:
                        for inc in incidents:
                            print(f"[¡INFRACCIÓN DETECTADA!]: {inc}")
                            # Aquí luego despacharemos el evento vía WebSocket

                # Opcional: si quieres visualizar la cámara de escritorio en local descomenta la siguiente línea:
                # cv2.imshow(f"SentinelEye - Camera {camera_id}", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        except KeyboardInterrupt:
            print("[Stream] Detenido manualmente por el usuario.")
        finally:
            cap.release()
            cv2.destroyAllWindows()