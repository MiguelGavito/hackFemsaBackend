from ultralytics import YOLO
import cv2
import os
from collections import defaultdict

def extract_detections(results):
    names = results.names
    dets = []
    for box, cls_id, conf in zip(results.boxes.xyxy.tolist(), results.boxes.cls.tolist(), results.boxes.conf.tolist()):
        dets.append({
            "name": names[int(cls_id)],
            "x1": float(box[0]),
            "x2": float(box[2]),
            "y1": float(box[1]),
            "y2": float(box[3]),
            "x": (box[0] + box[2]) / 2,
            "y": (box[1] + box[3]) / 2,
            "conf": float(conf)
        })
    return dets

def deduplicate_by_overlap(detections, iou_threshold=0.5):
    def compute_iou(boxA, boxB):
        xA = max(boxA["x1"], boxB["x1"])
        xB = min(boxA["x2"], boxB["x2"])
        yA = max(boxA["y1"], boxB["y1"])
        yB = min(boxA["y2"], boxB["y2"])
        inter = max(0, xB - xA) * max(0, yB - yA)
        areaA = (boxA["x2"] - boxA["x1"]) * (boxA["y2"] - boxA["y1"])
        areaB = (boxB["x2"] - boxB["x1"]) * (boxB["y2"] - boxB["y1"])
        union = areaA + areaB - inter
        return inter / union if union > 0 else 0

    deduped = []
    for det in sorted(detections, key=lambda d: d["conf"], reverse=True):
        if any(compute_iou(det, d) > iou_threshold and det["name"] == d["name"] for d in deduped):
            continue
        deduped.append(det)
    return deduped

def compare_detections(reference, current, tolerance_px=50):
    correctos = []
    mal_posicionados = []
    faltantes = []
    extras = [d["name"] for d in current]

    for ref_det in reference:
        name = ref_det["name"]
        expected_x = ref_det["x"]
        candidates = [s for s in current if s["name"] == name]
        if not candidates:
            faltantes.append(name)
            continue
        closest = min(candidates, key=lambda c: abs(c["x"] - expected_x))
        if abs(closest["x"] - expected_x) <= tolerance_px:
            correctos.append(name)
        else:
            mal_posicionados.append(name)
        if name in extras:
            extras.remove(name)

    return {
        "correctos": sorted(set(correctos)),
        "mal_posicionados": sorted(set(mal_posicionados)),
        "faltantes": sorted(set(faltantes)),
        "extras": sorted(set(extras))
    }

def segment_image(image_path):
    """Divide la imagen en 4 segmentos horizontales."""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("No se pudo cargar la imagen")
    
    h = img.shape[0]
    segments = [img[i*h//4:(i+1)*h//4, :] for i in range(4)]
    
    # Guardar segmentos temporalmente
    temp_paths = []
    for i, segment in enumerate(segments):
        temp_path = f"_tmp_seg{i}.jpg"
        cv2.imwrite(temp_path, segment)
        temp_paths.append(temp_path)
    
    return temp_paths

def process_segment(model, segment_path, conf_threshold=0.1):
    """Procesa un segmento de imagen y retorna las detecciones."""
    results = model.predict(segment_path, conf=conf_threshold)[0]
    detections = deduplicate_by_overlap(extract_detections(results))
    return detections

def cleanup_temp_files(temp_paths):
    """Elimina archivos temporales."""
    for path in temp_paths:
        if os.path.exists(path):
            os.remove(path) 