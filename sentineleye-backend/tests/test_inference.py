import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.inference.processor import SecurityVideoProcessor

# Inicializar procesador con un modelo válido
processor = SecurityVideoProcessor(model_path="yolov8n.pt")

# Pasar la ruta de un video local en lugar de 0 (webcam)
processor.start_stream_simulation(camera_id=1, source="tests/sample_safety.mp4", fps_limit=1)