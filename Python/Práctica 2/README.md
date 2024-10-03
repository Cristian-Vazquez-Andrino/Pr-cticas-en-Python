# Clasificación y Clustering en 'Villa Laminera'

## Objetivo de la Práctica

El objetivo principal de esta práctica es explorar y aplicar técnicas de **clasificación** a un conjunto de datos de la población ficticia 'Villa Laminera'. En este proyecto se implementarán y usarán los algoritmos de clasificación **KMeans** y **DBSCAN**, además de otras técnicas estadísticas y de visualización.

## Descripción

La práctica incluye las siguientes tareas principales:

- **Cálculo del coeficiente de Silhouette**: Se utilizará para determinar el número óptimo de vecindades o clusters en el conjunto de datos.
  
- **Representación del Diagrama de Voronoi**: Utilizando KMeans con métrica euclidiana.
  
- **Predicción de la "franja de edad"**: Se predecirá la franja de edad a la que deben pertenecer dos personas basándonos en los valores de sus dos estados.

Para la implementación de los algoritmos **KMeans** y **DBSCAN** se han utilizado las librerías disponibles en Python, específicamente **scikit-learn**. Para la representación del **Diagrama de Voronoi** se utilizó la librería **scipy**.

## Resumen de Contenido

A continuación, se describen brevemente los elementos principales que se encuentran en el proyecto:

- **Clasificación y Clustering con KMeans y DBSCAN**: 
  - Se implementan y se aplican los algoritmos de clasificación **KMeans** y **DBSCAN** al conjunto de datos 'Villa Laminera'.
  - Se utiliza el **coeficiente de Silhouette** para evaluar la calidad de los clusters y determinar el número óptimo de vecindades en el conjunto de datos.

- **Representación Gráfica**:
  - Se representa el diagrama de **Voronoi** utilizando el algoritmo KMeans con **métrica euclidiana**.
  - Se graficará el **coeficiente de Silhouette** en función del número de vecindades, utilizando el algoritmo KMeans.
  - Posteriormente, se repetirá con el algoritmo **DBSCAN** para las métricas **manhattan** y **euclidiana**.

- **Archivos del Proyecto**:
  - La práctica se resuelve en el script **`Clustering.py`**.
  - El archivo **`Personas_de_villa_laminera.txt`** es un archivo auxiliar que contiene los datos que se usan para la clasificación y el clustering.
  
  Para más detalles sobre la implementación, consulta el enunciado de la práctica y los comentarios incluidos en el script.

## Método de Uso

El script `Clustering.py` proporciona todas las funcionalidades necesarias para realizar el análisis de clasificación y clustering sobre el conjunto de datos. Para utilizar el script:

1. Asegúrate de tener instaladas las librerías **scikit-learn** y **scipy** en tu entorno de Python.
2. Ejecuta el script `Clustering.py` para realizar las siguientes tareas:
   - Calcular el **coeficiente de Silhouette** y determinar el número óptimo de vecindades.
   - Representar el **diagrama de Voronoi** utilizando **KMeans** con métrica **euclidiana**.
   - Graficar el **coeficiente de Silhouette** para KMeans y DBSCAN, usando las métricas **manhattan** y **euclidiana**.

3. Las gráficas resultantes se generarán automáticamente y pueden ser visualizadas para comparar los resultados de los diferentes métodos aplicados.

## Notas Finales

- La práctica tiene como propósito no solo la aplicación de técnicas de clasificación y clustering, sino también la **visualización** de los resultados, lo cual es clave para entender mejor la agrupación y las relaciones entre los datos.

- Recomendamos experimentar con los parámetros de los algoritmos **KMeans** y **DBSCAN** (como el número de clusters o la distancia máxima entre vecinos) para observar cómo estos afectan a la calidad y estructura de los clusters obtenidos.

- Asegúrate de revisar el script `Clustering.py` y los comentarios incluidos para un entendimiento detallado del proceso implementado.
