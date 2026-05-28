"""
Sistema de Reconocimiento Facial en Tiempo Real
Usa el modelo entrenado para clasificar rostros en vivo desde la webcam
"""

import cv2
import numpy as np
from tensorflow.keras.models import load_model
import json

# Configuración
MODEL_PATH = 'face_classifier_model.h5'
CLASSES_PATH = 'class_indices.json'
IMG_SIZE = 224

# Cargar modelo y clases
print("Cargando modelo...")
model = load_model(MODEL_PATH)
print("✅ Modelo cargado")

with open(CLASSES_PATH, 'r', encoding='utf-8') as f:
    class_labels = json.load(f)

print(f"✅ {len(class_labels)} clases cargadas\n")

# Inicializar cámara
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Error: No se pudo acceder a la cámara")
    exit()

# Cargar detector de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

print("🎥 Sistema de Reconocimiento Facial Iniciado")
print("Presiona 'q' para salir\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Detectar rostros
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        # Extraer región del rostro
        face_roi = frame[y:y+h, x:x+w]
        
        # Preprocesar para el modelo
        face_resized = cv2.resize(face_roi, (IMG_SIZE, IMG_SIZE))
        face_array = np.array(face_resized, dtype=np.float32)
        face_array = face_array / 255.0  # Normalizar
        face_array = np.expand_dims(face_array, axis=0)  # Añadir batch dimension
        
        # Predecir
        predictions = model.predict(face_array, verbose=0)
        predicted_class = np.argmax(predictions[0])
        confidence = predictions[0][predicted_class]
        
        # Obtener nombre y top 3 predicciones
        person_name = class_labels[str(predicted_class)].replace('_', ' ')
        
        # Obtener top 3 predicciones para análisis
        top3_indices = np.argsort(predictions[0])[-3:][::-1]
        
        # Umbral ajustado a la realidad del modelo (56% accuracy)
        if confidence > 0.30:  # Ajustado para modelo con 56% accuracy
            color = (0, 255, 0)  # Verde
            text = f"{person_name}: {confidence*100:.1f}%"
        else:
            color = (0, 165, 255)  # Naranja
            text = f"Desconocido: {confidence*100:.1f}%"
        
        # Mostrar top 3 en consola
        print(f"\nTop 3 predicciones:")
        for idx in top3_indices:
            name = class_labels[str(idx)].replace('_', ' ')
            conf = predictions[0][idx] * 100
            print(f"  {name}: {conf:.1f}%")
        
        # Dibujar rectángulo y texto
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        
        # Fondo para el texto
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(frame, (x, y-30), (x+text_width, y), color, -1)
        
        # Texto
        cv2.putText(frame, text, (x, y-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Mostrar instrucciones
    cv2.putText(frame, "Presiona 'q' para salir", (10, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Mostrar frame
    cv2.imshow('Reconocimiento Facial en Tiempo Real - Proyecto IA', frame)
    
    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Limpiar
cap.release()
cv2.destroyAllWindows()
print("\n✅ Sistema cerrado correctamente")
