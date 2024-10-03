"""
Autor: Cristian Vázquez Andrino
"""

""""
Práctica 3. Transformación isométrica afín
"""

import numpy as np
import matplotlib.pyplot as plt
import imageio
import io
from matplotlib import cm
from skimage import io as sio
from scipy.spatial import ConvexHull
from scipy.spatial.distance import pdist, squareform


# APARTADO 1

# GENERACIÓN DE LA SUPERFICIE 3D S

X = np.arange(-5, 5, 0.1)
Y = np.arange(-5, 5, 0.1)
X, Y = np.meshgrid(X, Y)
R = -np.sqrt(X ** 2 / 2 + Y ** 2 / 4)
Z = np.sin(R)

# Definimos una función para calcular el diámetro mayor y el centroide:
def diametro_mayor(X,Y,Z):
    # Obtener los puntos de la superficie
    puntos = np.column_stack([X.flatten(), Y.flatten(), Z.flatten()])
    # Calcular la envolvente convexa de los puntos
    hull = ConvexHull(puntos)
    # Obtener las distancias entre todos los pares de puntos en la envolvente convexa
    distancias = squareform(pdist(puntos[hull.vertices]))
    # Encontrar la distancia máxima entre los puntos de la envolvente convexa
    diametro = np.amax(distancias)
    print("Diámetro mayor de la superficie:", diametro)
    return diametro

# Definimos una función que ayuda a seleccionar los límites de los ejes de las gráficas:
def lims(C,C_trans):
    ct_max = np.max(C_trans)
    cn_max = np.max(C)
    c_max = max(ct_max, cn_max)
    ct_min = np.min(C_trans)
    cn_min = np.min(C)
    c_min = min(ct_min, cn_min)
    return c_min, c_max

# Definimos las funciones para graficar y transformar una superficie
def transformacion_afin(X, Y, Z, theta, v, t):
    theta_t=t*theta
    v_t=t*v
    # Calcular el centroide de la superficie S
    centroid_x = np.mean(X)
    centroid_y = np.mean(Y)
    centroid_z = np.mean(Z)
    print(f"el centroide se situa en ({centroid_x},{centroid_y},{centroid_z})")
    # Trasladar los puntos al origen (centroide)
    X_centered = X - centroid_x
    Y_centered = Y - centroid_y
    Z_centered = Z - centroid_z
    # Definir la matriz de rotación R_theta_xy
    cos_theta = np.cos(theta_t)
    sin_theta = np.sin(theta_t)
    R_theta = np.array([[cos_theta, -sin_theta, 0],[sin_theta, cos_theta, 0],[0, 0, 1]])
    # Aplicar la rotación alrededor del origen
    X_rotated = X_centered * cos_theta - Y_centered * sin_theta
    Y_rotated = X_centered * sin_theta + Y_centered * cos_theta
    Z_rotated = Z_centered
    # Trasladar de vuelta al centroide con la traslación v
    X_transformed = X_rotated + centroid_x + v_t[0]
    Y_transformed = Y_rotated + centroid_y + v_t[1]
    Z_transformed = Z_rotated + centroid_z + v_t[2]
    return X_transformed, Y_transformed, Z_transformed

# CREACIÓN DEL GIF

# Definimos la función para generar cada frame de la animación
def generate_frame(t):
    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    # Aplicar la transformación afín
    X_trans, Y_trans, Z_trans = transformacion_afin(X, Y, Z, theta, v, t)
    # Graficar la superficie transformada
    surf = ax.plot_surface(X_trans, Y_trans, Z_trans, rstride=1, cstride=1, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    z_min = np.min(Z_trans)
    z_max = np.max(Z_trans)
    ax.set_zlim(z_min, z_max)
    fig.colorbar(surf, shrink=0.5, aspect=10)
    # Guardar la figura en un buffer de memoria y convertirla a una imagen
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image = imageio.imread(buffer)
    plt.close(fig)  # Cerrar la figura para liberar memoria
    return image

# Ángulo de rotación
theta = 3 * np.pi
# Vector de traslación v
d = diametro_mayor(X,Y,Z)  # Diámetro mayor de S
v = np.array([0, 0, d])



duration = 1.0  # Duración total de la animación en segundos
fps = 20  # Fotogramas por segundo

# Calcular el número de fotogramas (timesteps) y los valores de tiempo (t_values)
timesteps = int(duration * fps)  # Número de pasos de tiempo basado en la duración y fps
t_values = np.linspace(0, 1, timesteps)  # Valores de tiempo entre 0 y 1 para la animación

# Lista para almacenar las imágenes de cada frame
images = []

# Generar cada frame de la animación para cada paso de tiempo
for i, t in enumerate(t_values):
    print(f'Generando frame para t={t:.2f} (frame {i + 1}/{timesteps})...')
    frame_image = generate_frame(t)
    images.append(frame_image)

# Guardar la animación como un archivo GIF
output_gif_path = 'p4a2.gif'
imageio.mimsave(output_gif_path, images, format='gif', duration=1 / fps)  # Ajustar la duración según fps
print(f'¡Animación completa! GIF guardado en: {output_gif_path}')

# APARTADO 2

img = sio.imread('C:/Users/niket/OneDrive/Escritorio/Geometría Computacional/p4/hurricane-isabel.png')
dimensions = img.data.shape
print(dimensions)
sio.show()

xyz = img.shape
x = np.arange(0, xyz[0], 1)
y = np.arange(0, xyz[1], 1)
xx, yy = np.meshgrid(x, y)
xx = np.asarray(xx).reshape(-1)
yy = np.asarray(yy).reshape(-1)
z = img[:,:,2]
z = np.transpose(z)
zz = np.asarray(z).reshape(-1)

x0 = xx[zz > 100]
y0 = yy[zz > 100]
z0 = zz[zz > 100] / zz.max()

# Función para generar cada frame de la animación
def generate_frame_2(t,x_max,y_max):
    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    # Aplicar la transformación afín
    XYZ= transformacion_afin(x0, y0, z0, theta, v, t)
    # Crear una figura y graficar los puntos transformados
    fig, ax = plt.subplots(figsize=(6, 6))
    col = plt.get_cmap("viridis")(XYZ[2])
    ax.scatter(XYZ[0], XYZ[1], c=col, s=0.1)
    ax.set_xlim(0, x_max)
    ax.set_ylim(0, y_max)
    # Guardar la figura en un buffer de memoria y convertirla a una imagen
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image = imageio.imread(buffer)
    plt.close(fig)  # Cerrar la figura para liberar memoria
    return image

# Ángulo de rotación
theta = 6 * np.pi
# Vector de traslación v
d = diametro_mayor(x0, y0, z0)
v = np.array([d, d, 0])
# Límites de la gráfica de la animación
XYZ = transformacion_afin(x0, y0, z0, theta, v, 1)
x_min, x_max = lims(x0, XYZ[0])
y_min, y_max = lims(y0, XYZ[1])

# Definir los parámetros de la animación
duration = 3.0  # Duración total de la animación en segundos
fps = 30  # Fotogramas por segundo

# Calcular el número de fotogramas (timesteps) y los valores de tiempo (t_values)
timesteps = int(duration * fps)  # Número de pasos de tiempo basado en la duración y fps
t_values = np.linspace(0, 1, timesteps)  # Valores de tiempo entre 0 y 1 para la animación

# Lista para almacenar las imágenes de cada frame
images = []

# Generar cada frame de la animación para cada paso de tiempo
for i, t in enumerate(t_values):
    print(f'Generando frame para t={t:.2f} (frame {i + 1}/{timesteps})...')
    frame_image = generate_frame_2(t,x_max,y_max)
    images.append(frame_image)

# Guardar la animación como un archivo GIF
output_gif_path = 'p4b2.gif'
imageio.mimsave(output_gif_path, images, format='gif', duration=1 / fps)  # Ajustar la duración según fps
print(f'¡Animación completa! GIF guardado en: {output_gif_path}')