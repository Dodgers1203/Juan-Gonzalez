"""
Clasificación con SVM (kernel Radial/RBF)

Este script genera un conjunto de datos no lineal (círculos),
entrena un clasificador SVM con kernel RBF, evalúa su desempeño
e ilustra la frontera de decisión. También realiza una pequeña
búsqueda en malla (GridSearchCV) para encontrar buenos hiperparámetros.

Salidas:
- rbf_svm_decision_boundary.png: gráfica de frontera de decisión
- confusion_matrix.png: matriz de confusión

Ejecutar:
	python SVM.py
"""

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Usar backend no interactivo para guardar figuras sin abrir ventanas
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay, confusion_matrix


def generate_data(n_samples: int = 400, noise: float = 0.1, factor: float = 0.4, random_state: int = 42):
	"""Genera datos en forma de círculos concéntricos (no linealmente separables)."""
	X, y = make_circles(n_samples=n_samples, noise=noise, factor=factor, random_state=random_state)
	return X, y


def build_pipeline(C: float = 1.0, gamma="scale") -> Pipeline:
	"""Crea un pipeline: estandarización + SVM RBF.

	- StandardScaler: esencial para SVM con RBF (escala las características)
	- SVC(kernel='rbf'): clasificador con kernel radial
	"""
	return Pipeline([
		("scaler", StandardScaler()),
		("svc", SVC(kernel="rbf", C=C, gamma=gamma, probability=False))
	])


def fit_and_evaluate(model: Pipeline, X_train, y_train, X_test, y_test):
	model.fit(X_train, y_train)
	y_pred = model.predict(X_test)
	acc = accuracy_score(y_test, y_pred)
	report = classification_report(y_test, y_pred, digits=4)
	cm = confusion_matrix(y_test, y_pred)
	return acc, report, cm, y_pred


def plot_decision_boundary(model: Pipeline, X: np.ndarray, y: np.ndarray, fname: str = "rbf_svm_decision_boundary.png"):
	"""Grafica la frontera de decisión del clasificador en 2D y guarda a archivo."""
	# Malla densa en el espacio de características
	x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
	y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
	xx, yy = np.meshgrid(
		np.linspace(x_min, x_max, 400),
		np.linspace(y_min, y_max, 400),
	)
	grid = np.c_[xx.ravel(), yy.ravel()]

	# Pipeline maneja el escalado internamente; decision_function da márgenes
	Z = model.decision_function(grid)
	Z = Z.reshape(xx.shape)

	plt.figure(figsize=(7, 6))
	# Mapa de calor suave de márgenes
	contour = plt.contourf(xx, yy, Z, levels=50, cmap="RdBu", alpha=0.7)
	plt.colorbar(contour, label="margen (decision_function)")

	# Contorno de la frontera (margen = 0)
	plt.contour(xx, yy, Z, levels=[0], colors="k", linestyles=["--"], linewidths=1.5)

	# Puntos de datos
	scatter = plt.scatter(X[:, 0], X[:, 1], c=y, cmap="bwr", edgecolor="k", s=30, alpha=0.9)
	plt.xlabel("x1")
	plt.ylabel("x2")
	plt.title("SVM con kernel RBF - Frontera de decisión")
	plt.tight_layout()
	plt.savefig(fname, dpi=130)
	plt.close()


def plot_confusion_matrix(cm: np.ndarray, fname: str = "confusion_matrix.png"):
	disp = ConfusionMatrixDisplay(confusion_matrix=cm)
	disp.plot(cmap="Blues")
	plt.title("Matriz de confusión")
	plt.tight_layout()
	plt.savefig(fname, dpi=130)
	plt.close()


def small_grid_search(X_train, y_train):
	"""Pequeño GridSearchCV para ajustar C y gamma.

	Mantiene la búsqueda pequeña para ser rápida pero ilustrativa.
	"""
	base = build_pipeline()
	param_grid = {
		"svc__C": [0.1, 1, 10],
		"svc__gamma": ["scale", 0.1, 1, 10],
	}
	gs = GridSearchCV(base, param_grid=param_grid, cv=5, n_jobs=-1)
	gs.fit(X_train, y_train)
	return gs


def main():
	# 1) Datos
	X, y = generate_data(n_samples=500, noise=0.15, factor=0.4, random_state=42)
	X_train, X_test, y_train, y_test = train_test_split(
		X, y, test_size=0.25, random_state=42, stratify=y
	)

	# 2) Modelo base (valores razonables por defecto)
	model = build_pipeline(C=1.0, gamma="scale")
	acc, report, cm, _ = fit_and_evaluate(model, X_train, y_train, X_test, y_test)

	print("Modelo base SVM RBF")
	print(f"Accuracy (test): {acc:.4f}")
	print("\nReporte de clasificación (test):\n", report)

	# 3) Búsqueda en malla pequeña para mejorar (opcional)
	print("Buscando hiperparámetros (GridSearchCV pequeño)...")
	gs = small_grid_search(X_train, y_train)
	print("Mejores hiperparámetros:", gs.best_params_)

	# Reentrenar con los mejores hiperparámetros y evaluar
	best_model: Pipeline = gs.best_estimator_
	best_acc, best_report, best_cm, _ = fit_and_evaluate(best_model, X_train, y_train, X_test, y_test)
	print("\nMejor modelo SVM RBF tras GridSearchCV")
	print(f"Accuracy (test): {best_acc:.4f}")
	print("\nReporte de clasificación (test):\n", best_report)

	# 4) Gráficas
	# Frontera de decisión usando TODOS los datos para visualizar mejor el espacio
	plot_decision_boundary(best_model, X, y, fname="rbf_svm_decision_boundary.png")
	plot_confusion_matrix(best_cm, fname="confusion_matrix.png")

	print("\nSe guardaron las figuras:")
	print(" - rbf_svm_decision_boundary.png")
	print(" - confusion_matrix.png")


if __name__ == "__main__":
	main()

