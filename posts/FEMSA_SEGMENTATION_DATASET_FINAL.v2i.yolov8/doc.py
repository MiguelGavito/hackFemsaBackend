from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

# Cargar modelo
model = YOLO("runs/detect/train3/weights/best.pt")

# Realizar predicción con umbral bajo para forzar detecciones
results = model.predict("IMG_9859.JPG", conf=0.1)[0]

# Dibujar las detecciones
img_with_boxes = results.plot()  # Esto devuelve una imagen con boxes y etiquetas

# Mostrar en pantalla
plt.figure(figsize=(12, 8))
plt.imshow(cv2.cvtColor(img_with_boxes, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.title("Detecciones con nombres de clase")
plt.show()
print(results.names)
print(results.boxes.cls)
print(results.boxes.conf)


