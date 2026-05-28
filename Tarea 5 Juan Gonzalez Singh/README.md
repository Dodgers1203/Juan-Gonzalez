# Clasificación con SVM (kernel Radial / RBF)

Este proyecto contiene un ejemplo completo de clasificación no lineal usando **SVM con kernel RBF** en un conjunto de datos sintético de círculos concéntricos.

## ¿Qué hace el script?
- Genera datos `make_circles` (no linealmente separables)
- Crea un `Pipeline` con `StandardScaler` + `SVC(kernel='rbf')`
- Entrena y evalúa el modelo (accuracy, reporte de clasificación y matriz de confusión)
- Realiza una pequeña búsqueda en malla (`GridSearchCV`) para encontrar mejores hiperparámetros `C` y `gamma`
- Guarda dos figuras:
  - `rbf_svm_decision_boundary.png`: frontera de decisión
  - `confusion_matrix.png`: matriz de confusión

## Requisitos
Instala dependencias (usa el mismo intérprete de Python que ejecutes):

```powershell
# Desde esta carpeta
C:/Users/macac/AppData/Local/Microsoft/WindowsApps/python3.11.exe -m pip install -r requirements.txt
```

> Nota: el script ya usa un backend no interactivo de matplotlib, por lo que generará archivos `.png` sin abrir ventanas.

## Ejecutar

```powershell
C:/Users/macac/AppData/Local/Microsoft/WindowsApps/python3.11.exe SVM.py
```

## Explicación breve
- `StandardScaler`: SVM con RBF es sensible a la escala; estandarizamos características (media 0, varianza 1).
- `C`: controla el equilibrio entre margen ancho y penalización de errores de clasificación (regularización). Valores grandes de `C` intentan clasificar mejor el entrenamiento pero pueden sobreajustar.
- `gamma`: controla el alcance (la "anchura") de la función radial. `gamma` grande hace fronteras más complejas/locales; `gamma` pequeño hace fronteras más suaves.
- `GridSearchCV`: valida combinaciones de `C` y `gamma` con validación cruzada para elegir la que funciona mejor.
