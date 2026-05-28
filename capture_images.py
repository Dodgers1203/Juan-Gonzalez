import cv2
import os
import time

def capturar_imagenes():
    """
    Script para capturar imágenes de rostros usando la webcam.
    Útil para crear tu dataset personalizado.
    """
    
    # Solicitar información al usuario
    print("\n=== CAPTURA DE IMÁGENES PARA DATASET ===\n")
    nombre = input("Ingresa el nombre de la persona (sin espacios, usa guion_bajo): ").strip()
    
    tipo = input("¿Es para train o validation? (train/val): ").strip().lower()
    if tipo == "val":
        tipo = "validation"
    elif tipo != "train" and tipo != "validation":
        print("Opción inválida. Usando 'train' por defecto.")
        tipo = "train"
    
    # Crear carpeta si no existe
    carpeta = f"face_data/{tipo}/{nombre}"
    os.makedirs(carpeta, exist_ok=True)
    
    # Contar imágenes existentes para continuar numeración
    existentes = len([f for f in os.listdir(carpeta) if f.endswith(('.jpg', '.png'))])
    contador = existentes
    
    print(f"\n📁 Guardando en: {carpeta}")
    print(f"📸 Imágenes existentes: {existentes}")
    print("\n--- INSTRUCCIONES ---")
    print("• Presiona ESPACIO para iniciar captura automática")
    print("• Se capturarán 500 fotos en 21 segundos")
    print("• Mueve tu cabeza y varía expresiones durante la captura")
    print("• Presiona ESC para cancelar\n")
    
    # Inicializar webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print(" Error: No se pudo acceder a la cámara")
        return
    
    print(" Cámara iniciada correctamente\n")
    
    # Cargar detector de rostros (opcional, para dibujar rectángulo)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    capturando = False
    total_fotos = 500 if tipo == "train" else 100  # 500 para train, 100 para validation
    duracion_segundos = 21
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print(" Error al leer frame de la cámara")
            break
        
        # Mostrar estado
        if not capturando:
            cv2.putText(frame, f"Capturas: {contador}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.putText(frame, "ESPACIO: Capturar | ESC: Salir", (10, frame.shape[0] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Mostrar frame
        cv2.imshow('Capturar Rostros - Proyecto IA', frame)
        
        tecla = cv2.waitKey(1) & 0xFF
        
        if tecla == 27:  # ESC
            print("\n Captura finalizada")
            break
        elif tecla == 32 and not capturando:  # ESPACIO
            capturando = True
            print(f"\n📸 Iniciando captura de {total_fotos} fotos en {duracion_segundos} segundos...")
            print("💡 Mueve tu cabeza y varía expresiones!")
            
            inicio = time.time()
            intervalo = duracion_segundos / total_fotos
            fotos_capturadas = 0
            
            while fotos_capturadas < total_fotos:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Mostrar progreso
                progreso = int((fotos_capturadas / total_fotos) * 100)
                cv2.putText(frame, f"CAPTURANDO: {fotos_capturadas}/{total_fotos} ({progreso}%)", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, "Mueve tu cabeza y varia expresiones", (10, frame.shape[0] - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                
                cv2.imshow('Capturar Rostros - Proyecto IA', frame)
                cv2.waitKey(1)
                
                # Guardar imagen
                nombre_archivo = f"{carpeta}/img_{contador:04d}.jpg"
                cv2.imwrite(nombre_archivo, frame)
                contador += 1
                fotos_capturadas += 1
                
                # Esperar el intervalo
                time.sleep(intervalo)
            
            tiempo_total = time.time() - inicio
            print(f"✅ ¡Captura completada! {fotos_capturadas} fotos en {tiempo_total:.2f} segundos")
            capturando = False
    
    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n Total de imágenes capturadas en esta sesión: {contador - existentes}")
    print(f" Total de imágenes en {carpeta}: {contador}")
    print("\n Consejos:")
    if tipo == "train" and contador < 30:
        print("     Para mejor precisión, captura al menos 30-50 imágenes para training")
    if tipo == "validation" and contador < 10:
        print("   ⚠️ Para validación, se recomiendan al menos 10-15 imágenes")

if __name__ == "__main__":
    try:
        capturar_imagenes()
    except KeyboardInterrupt:
        print("\n\n  Captura interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
