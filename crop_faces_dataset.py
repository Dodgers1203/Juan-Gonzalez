import cv2
import os
from pathlib import Path
from tqdm import tqdm

# Configuración
SOURCE_DIR = 'face_data'
OUTPUT_DIR = 'face_data_cropped'
IMG_SIZE = 224  # Tamaño final de la imagen recortada

# Cargar clasificador Haar Cascade para detección de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def crop_face(image_path, output_path, margin=0.3):
    """
    Detecta y recorta la cara de una imagen con margen adicional.
    
    Args:
        image_path: Ruta de la imagen original
        output_path: Ruta donde guardar la imagen recortada
        margin: Margen adicional alrededor de la cara (0.3 = 30% más grande)
    
    Returns:
        True si se detectó y recortó correctamente, False si no
    """
    # Leer imagen
    img = cv2.imread(image_path)
    if img is None:
        return False
    
    # Convertir a escala de grises para detección
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detectar rostros
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
    # Si no se detecta cara, guardar imagen original redimensionada
    if len(faces) == 0:
        resized = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        cv2.imwrite(output_path, resized)
        return False
    
    # Tomar la cara más grande (en caso de múltiples detecciones)
    x, y, w, h = max(faces, key=lambda face: face[2] * face[3])
    
    # Calcular margen adicional
    margin_x = int(w * margin)
    margin_y = int(h * margin)
    
    # Coordenadas con margen (sin salirse de la imagen)
    x1 = max(0, x - margin_x)
    y1 = max(0, y - margin_y)
    x2 = min(img.shape[1], x + w + margin_x)
    y2 = min(img.shape[0], y + h + margin_y)
    
    # Recortar cara con margen
    face_crop = img[y1:y2, x1:x2]
    
    # Redimensionar a tamaño estándar
    face_resized = cv2.resize(face_crop, (IMG_SIZE, IMG_SIZE))
    
    # Guardar imagen recortada
    cv2.imwrite(output_path, face_resized)
    
    return True

def process_dataset():
    """
    Procesa todo el dataset recortando caras.
    """
    stats = {
        'total': 0,
        'cropped': 0,
        'no_face': 0,
        'error': 0
    }
    
    # Procesar train y validation
    for split in ['train', 'validation']:
        source_split_dir = os.path.join(SOURCE_DIR, split)
        output_split_dir = os.path.join(OUTPUT_DIR, split)
        
        if not os.path.exists(source_split_dir):
            print(f"⚠️  Directorio {source_split_dir} no encontrado, saltando...")
            continue
        
        # Crear directorio de salida
        os.makedirs(output_split_dir, exist_ok=True)
        
        # Obtener todas las clases (carpetas de personas)
        classes = [d for d in os.listdir(source_split_dir) 
                  if os.path.isdir(os.path.join(source_split_dir, d))]
        
        print(f"\n📁 Procesando {split.upper()} - {len(classes)} clases")
        
        # Procesar cada clase
        for class_name in tqdm(classes, desc=f"Clases en {split}"):
            source_class_dir = os.path.join(source_split_dir, class_name)
            output_class_dir = os.path.join(output_split_dir, class_name)
            
            # Crear directorio de clase
            os.makedirs(output_class_dir, exist_ok=True)
            
            # Obtener todas las imágenes
            images = [f for f in os.listdir(source_class_dir) 
                     if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            # Procesar cada imagen
            for img_name in images:
                stats['total'] += 1
                source_path = os.path.join(source_class_dir, img_name)
                output_path = os.path.join(output_class_dir, img_name)
                
                try:
                    face_detected = crop_face(source_path, output_path)
                    if face_detected:
                        stats['cropped'] += 1
                    else:
                        stats['no_face'] += 1
                except Exception as e:
                    stats['error'] += 1
                    print(f"\n❌ Error procesando {source_path}: {e}")
    
    return stats

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 RECORTE AUTOMÁTICO DE CARAS - DATASET COMPLETO")
    print("=" * 60)
    print(f"\n📂 Origen: {SOURCE_DIR}")
    print(f"📂 Destino: {OUTPUT_DIR}")
    print(f"📏 Tamaño de salida: {IMG_SIZE}x{IMG_SIZE} píxeles")
    print(f"🎯 Margen adicional: 30% alrededor de la cara")
    print("\nIniciando procesamiento...\n")
    
    # Procesar dataset
    stats = process_dataset()
    
    # Mostrar estadísticas
    print("\n" + "=" * 60)
    print("📊 ESTADÍSTICAS DEL PROCESAMIENTO")
    print("=" * 60)
    print(f"✅ Total de imágenes procesadas: {stats['total']}")
    print(f"👤 Caras detectadas y recortadas: {stats['cropped']} ({stats['cropped']/stats['total']*100:.1f}%)")
    print(f"⚠️  Sin cara detectada (imagen completa): {stats['no_face']} ({stats['no_face']/stats['total']*100:.1f}%)")
    print(f"❌ Errores: {stats['error']}")
    print("\n✨ Procesamiento completado!")
    print(f"📁 Dataset recortado guardado en: {OUTPUT_DIR}")
    print("\n💡 Próximo paso: Cambiar BASE_DIR en train_model.py a 'face_data_cropped'")
