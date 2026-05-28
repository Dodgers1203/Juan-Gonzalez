import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Input, Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt
import json
import os

# --- Configuración ---
IMG_SIZE = (224, 224)  # Resolución estándar
BATCH_SIZE = 32  # Batch más grande para velocidad
EPOCHS = 60  # Épocas: 20+40
LEARNING_RATE = 0.0003  # Learning rate más alto para convergencia rápida

BASE_DIR = 'face_data_cropped'
TRAIN_DIR = os.path.join(BASE_DIR, 'train')
VAL_DIR = os.path.join(BASE_DIR, 'validation')

# --- 1. Generadores de Datos ---

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,       # rotación
    width_shift_range=0.3,   # desplazamiento
    height_shift_range=0.3,
    shear_range=0.3,         #  inclinación
    zoom_range=0.3,          #  zoom
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],  # Variación de brillo
    fill_mode='nearest'
)

# En el set de validación solo normalizar.
val_datagen = ImageDataGenerator(rescale=1./255)

# Flujos de datos 
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical' # Para clasificación multiclass
)

validation_generator = val_datagen.flow_from_directory(
    VAL_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

#  2. Guardar las Clases 
class_indices = train_generator.class_indices

labels_map = {v: k for k, v in class_indices.items()}

with open('class_indices.json', 'w') as f:
    json.dump(labels_map, f)

print(f"Clases encontradas: {labels_map}")
NUM_CLASSES = len(labels_map)

# 3. Construir el Modelo de Transfer Learning

# Cargamos MobileNetV2 por que usamos EfficientNetV2 y resulto que mobile era más rápido y eficiente
base_model = MobileNetV2(
    input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
    include_top=False,
    weights='imagenet'
)


base_model.trainable = False


inputs = Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
x = base_model(inputs, training=False)
x = GlobalAveragePooling2D()(x)
x = BatchNormalization()(x)
x = Dropout(0.5)(x)
x = Dense(512, activation='relu')(x)  # Capa más grande
x = BatchNormalization()(x)
x = Dropout(0.4)(x)
x = Dense(256, activation='relu')(x)
x = BatchNormalization()(x)
x = Dropout(0.3)(x)
x = Dense(128, activation='relu')(x)
outputs = Dense(NUM_CLASSES, activation='softmax')(x)

model = Model(inputs, outputs)

model.summary()

# 4. Compilar y Entrenar 

model.compile(
    optimizer=Adam(learning_rate=LEARNING_RATE),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("Iniciando entrenamiento...")

# Callbacks para usar optimización
early_stop = EarlyStopping(monitor='val_accuracy', patience=15, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-7)

# Fase 1: Entrenar solo las capas superiores
history = model.fit(
    train_generator,
    epochs=20,
    validation_data=validation_generator,
    callbacks=[early_stop, reduce_lr],
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    validation_steps=validation_generator.samples // BATCH_SIZE
)

print("\n🔧 Activando Fine-Tuning...")
# Fase 2: Descongelar las últimas capas de MobileNetV2 para fine-tuning
base_model.trainable = True
# Congelar todas menos las últimas 100 capas (más capas para fine-tuning)
for layer in base_model.layers[:-100]:
    layer.trainable = False

# Re-compilar con learning rate reseteado (no heredar reducciones previas)
model.compile(
    optimizer=Adam(learning_rate=0.00003),  # LR fresco para fine-tuning
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("Continuando con fine-tuning (40 épocas más)...")

# Callbacks para fine-tuning (sin EarlyStopping para garantizar épocas completas)
reduce_lr_ft = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=7, min_lr=1e-7)

# Continuar entrenamiento con más épocas
history_fine = model.fit(
    train_generator,
    epochs=60,
    initial_epoch=history.epoch[-1] + 1,
    validation_data=validation_generator,
    callbacks=[reduce_lr_ft],
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    validation_steps=validation_generator.samples // BATCH_SIZE
)

# Combinar historiales
for key in history.history.keys():
    if key in history_fine.history:
        history.history[key].extend(history_fine.history[key])

#5. Evaluar y Guardar

print("Entrenamiento completado.")

# Guardar el modelo en formato H5 (para el convertidor de TF.js)
model.save('face_classifier_model.h5')
print("Modelo guardado como 'face_classifier_model.h5'")
 
# Graficar para precisar y sacar la perdida
acc = history.history.get('accuracy', history.history.get('acc', []))
val_acc = history.history.get('val_accuracy', history.history.get('val_acc', []))
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(len(acc))

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.savefig('training_history.png')
print(" Gráfica guardada como 'training_history.png'")

print(f"Precisión de validación final: {val_acc[-1]*100:.2f}%")
if val_acc[-1] > 0.80:
    print(" Superaste el 80% de precisión.")
else:
    print("El modelo está por debajo del 80%. ")