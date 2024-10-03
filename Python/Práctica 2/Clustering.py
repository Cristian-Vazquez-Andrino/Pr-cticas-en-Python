"""
Autor: Cristian Vázquez Andrino / Grupo 2
"""

"""
Diagrama de Voronoi y Clustering
"""

import os
import numpy as np

from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from scipy.spatial import Voronoi, voronoi_plot_2d

import matplotlib.pyplot as plt

# Obtiene la ruta absoluta del directorio en el que se encuentra el script actualmente
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define 'a2' como la ruta del archivo dentro del mismo directorio
a2 = os.path.join(script_dir, "Personas_de_villa_laminera.txt")

# Definimos los dos sistemas asociados a dichos archivos:

# El sistema principal X consta de 1500 elementos, con dos estados
# cada uno. Cada elemento representa a una persona y los estados
# son el nivel de estrés y la afición a dulces
X = np.loadtxt(a2, skiprows=1)

# Dado sistema X de elementos con dos estados, la siguiente función
# imprime el plano representando en él los elementos del sistema.
def representar(sistema):
    plt.plot(sistema[:,0], sistema[:,1], 'bo', markersize=3)
    plt.show()



# Dados dos enteros n1 y n2, y un sistema X, la siguiente función
# aplica el algoritmo KMeans con la métrica euclidiana y muestra
# en una gráfica los puntos (i,s_i) donde i es un entero entre n1
# y n2 y s_i es el coeficiente de Silhouette para i vecindades. A
# su vez, devuelve par (k,s_k) para el que el coeficiente de
# Silhouette alcanza el valor más alto.
def silhouette_KMeans(n1, n2, sistema):
    l = []
    for i in range(n1, n2+1):
        kmeans = KMeans(n_clusters=i, random_state=0).fit(sistema)
        labels = kmeans.labels_
        s = metrics.silhouette_score(sistema, labels)
        l.append([i,s])
    Z = np.array(l)
    plt.title("Coeficientes de Silhouette en función del número de vecindades, \n" +
              "calculados con KMeans con métrica euclidiana")
    representar(Z)
    cs = list(Z[:,1])
    s = max(cs)
    k = cs.index(s)+n1
    print("el coeficiente de Silhouette es %0.3f" % s + f", y se alcanza con {k} vecindades")




# Dado un sistema X y un entero n, la siguiente función imprime
# en una gráfica el diagrama de Voronoi de k vecindades asociado
# al sistema X aplicando el algoritmo KMeans con métrica euclidiana.
def diagrama_Voronoi(sistema, n):

    # Aplicando el algoritmo KMeans (con métrica euclidiana), obtenemos
    # los centros de las vecindades y a partir de ellos dibujamos el
    # diagrama de Voronoi
    kmeans = KMeans(n_clusters=n, random_state=0).fit(sistema)
    centros = np.array(kmeans.cluster_centers_)
    v = Voronoi(centros)
    # Por el momento no pintamos los centros, lo haremos después
    voronoi_plot_2d(v, show_points=False, show_vertices=False,line_width=1.5, line_alpha=1)

    # Pintamos los elementos de cada vecindad con colores distintos
    # (uno por cada vecindad)
    labels = kmeans.labels_
    unique_labels = set(labels)
    scatter_handles=[]
    for k in unique_labels:
        class_member_mask = (labels == k)
        puntos = list(map(list, list(X[class_member_mask])))
        x, y = zip(*puntos)
        scatter_handle = plt.scatter(x, y, s=10)
        scatter_handles.append(scatter_handle)

    # Por último, pintamos los centros de cada vecindad como puntos
    # negros de mayor grosor que el resto
    c = list(map(list, list(centros)))
    x, y = zip(*c)
    plt.scatter(x, y, s=30, c="k")

    # Establecemos los límites del gráfico para tener esquinas diagonales
    #plt.xlim(-3, 3.7)
    #plt.ylim(-3.7, 3.7)

    # Añadimos una leyenda donde se declara el color de cada franja (esto
    # será importante para función predecir)
    F = []
    for i in range(0, n):
        F.append('Franja ' + str(i))
    plt.legend(scatter_handles, F, loc='lower right')

    # Añadimos un título descriptivo a la gráfica
    plt.title(f"Diagrama de Voronói con {n} vecindades por KMeans con métricla euclidiana")



# Dados un sistema X, un entero n y una lista de puntos lp, la siguiente
# función indica a que vecindad del diagrama de Voronoi generado por la
# función anterior pertenece cada punto de lp.
def predecir(sistema, n, lp):
    kmeans = KMeans(n_clusters=n, random_state=0).fit(sistema)
    puntos=np.array(lp)
    clases_pred = kmeans.predict(puntos)
    for i in range(0,len(clases_pred)):
        print(f"la persona {i+1} pertenece a la franja {clases_pred[i]}")



# Dados un sistema X, un par de números reales a y b, un entero n y una
# métrica, representa en una gráfica los coeficientes de Silhouette
# obtenidos usando DBSCAN en función de distintos valores del umbral de
# distancia (a,b), elegidos tomando del intervalo [a,b] en n elementos
# consecutivamente equidistantes. Devuelve el coeficiente de Silhouette mas
# alto obtenido.
def silhouette_DBSCAN(a, b, n, sistema, metrica):
    Z = []
    vecindades = []
    epsilons = np.linspace(a, b, n).tolist()
    for epsilon in epsilons:
        db = DBSCAN(eps=epsilon, min_samples=10, metric=metrica).fit(sistema)
        labels = db.labels_
        s = metrics.silhouette_score(sistema, labels)
        v = len(set(labels)) - (1 if -1 in labels else 0)
        vecindades.append(v)
        Z.append([epsilon, s])
    Z = np.array(Z)
    plt.title("Coeficientes de Silhouette en función del número de vecindades, \n " +
              f"calculados con DBSCAN con métrica {metrica}")
    representar(Z)
    cs = list(Z[:, 1])
    s = max(cs)
    k = cs.index(s)
    v = vecindades[k]
    epsilon = list(Z[:, 0])[k]
    print("el coeficiente de Silhouette mas alto encontrado es %0.3f" % s +
          f" para métrica {metrica}, y se alcanza con epsilon = {epsilon}" +
          f" que estima {v} vecindades")


# Dados un sistema X, un par de números reales a y b, un entero n
# representa en una gráfica en función del número de vecindades
# los coeficientes de Silhouette que produce KMeans frente a los
# que produce DBSCAN.
def comparar(sistema, a, b, n):
    z1 = []
    vecindades = []
    cs = []
    scatter_handles = []
    epsilons = np.linspace(a, b, n).tolist()
    for epsilon in epsilons:
        db = DBSCAN(eps=epsilon, min_samples=10, metric='euclidean').fit(sistema)
        labels = db.labels_
        s = metrics.silhouette_score(sistema, labels)
        v = len(set(labels)) - (1 if -1 in labels else 0)
        if v in vecindades:
            i = vecindades.index(v)
            if cs[i] < s:
                z1[i][1] = s
        else:
            vecindades.append(v)
            cs.append(s)
            z1.append([v, s])
    z1 = np.array(z1)
    scatter_handle = plt.scatter(z1[:,0], z1[:,1], s=7, color='b')
    scatter_handles.append(scatter_handle)
    n1 = min(vecindades)
    n2 = max(vecindades)
    z2 = []
    for i in range(n1, n2+1):
        kmeans = KMeans(n_clusters=i, random_state=0).fit(sistema)
        labels = kmeans.labels_
        s = metrics.silhouette_score(sistema, labels)
        z2.append([i, s])
    z2 = np.array(z2)
    scatter_handle = plt.scatter(z2[:, 0], z2[:, 1], s=7, color='r')
    scatter_handles.append(scatter_handle)
    plt.legend(scatter_handles, ['KMeans', 'DBSCAN'], loc='lower right')
    plt.xlim(0, 15.5)
    plt.ylim(-0.5, 0.7)
    plt.title(" Coeficientes de Silhouette en función del número de vecindades, \n " +
              "calculados por KMeans y DBSCAN (métrica euclidiana)")
    plt.show()

#diagrama_Voronoi(X,4)

diagrama_Voronoi(X,3)

silhouette_KMeans(2,7,X)



# runfile('D:/python/GC/p2/GCP2.py', wdir='D:/python/GC/p2')

