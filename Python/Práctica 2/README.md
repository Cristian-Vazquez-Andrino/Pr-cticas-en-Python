# Clustering y Diagrama de Voronoi

## Autor
Cristian Vázquez Andrino

## Descripción

El objetivo principal de esta práctica es explorar y aplicar técnicas de **clasificación** a un conjunto de datos de la población ficticia 'Villa Laminera'. En este proyecto se implementarán y usarán los algoritmos de clasificación **KMeans** y **DBSCAN**, además de otras técnicas estadísticas y de visualización.

La práctica incluye las siguientes tareas principales:

- **Cálculo del coeficiente de Silhouette**: Se utilizará para determinar el número óptimo de vecindades o clusters en el conjunto de datos.
  
- **Representación del Diagrama de Voronoi**: Utilizando KMeans con métrica euclidiana.
  
- **Predicción de la "franja de edad"**: Se predecirá la franja de edad a la que deben pertenecer dos personas basándonos en los valores de sus dos estados.

Para la implementación de los algoritmos **KMeans** y **DBSCAN** se han utilizado las librerías disponibles en Python, específicamente **scikit-learn**. Para la representación del **Diagrama de Voronoi** se utilizó la librería **scipy**.

## Archivos de la práctica
  - La práctica se resuelve en el script **`Clustering.py`**.
  - El archivo **`Personas_de_villa_laminera.txt`** es un archivo auxiliar que contiene los datos que se usan para la clasificación y el clustering.
  
  Para más detalles sobre la implementación, consulta el enunciado de la práctica y los comentarios incluidos en el script.

## Método de Uso

El script `Clustering.py` proporciona todas las funcionalidades necesarias para realizar el análisis de clasificación y clustering sobre el conjunto de datos. Para utilizar el script:

1. Asegúrate de tener instaladas las librerías **scikit-learn** y **scipy** en tu entorno de Python.
2. Asegúrate de tener el archivo `Personas_de_villa_laminera.txt` en el mismo directorio que `Clustering.py`.
3. Las gráficas resultantes se generarán automáticamente y pueden ser visualizadas para comparar los resultados de los diferentes métodos aplicados.

## Notas Finales

- La práctica tiene como propósito no solo la aplicación de técnicas de clasificación y clustering, sino también la **visualización** de los resultados, lo cual es clave para entender mejor la agrupación y las relaciones entre los datos.
