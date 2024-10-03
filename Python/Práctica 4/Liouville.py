"""
Autor: Cristian Vázquez Andrino
"""

""""
Práctica 4. Teorema de Liouville
"""
import os
import io
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from alphashape import alphashape
import imageio



os.getcwd()

# Definimos las funciones necesarias para desarrollar la práctica

# La siguiente función calcula (aproxima) la derivada numérica de una serie de valores
def deriv(q, dq0, d):
   dq = (q[1:len(q)] - q[0:(len(q)-1)]) / d
   dq = np.insert(dq, 0, dq0)
   return dq

# Implementamos la ecuación diferencial del oscilador no lineal
def F(q):
    ddq = -2 * q * (q**2 - 1)
    return ddq

# Esta función calcula las posiciones del oscilador en diferentes puntos en el tiempo
def orb(n, q0, dq0, F, d=0.001, args=None):
    q = np.empty([n+1])
    q[0] = q0
    q[1] = q0 + dq0 * d
    for i in np.arange(2, n+1):
        args = q[i-2]
        q[i] = -q[i-2] + d**2 * F(args) + 2 * q[i-1]
    return q

# Definimos la función simplectica, necesaria para representar el espacio fásico
def simplectica(q0, dq0, F, marker, col, d, n):
    q = orb(n, q0, dq0, F, d)
    dq = deriv(q, dq0, d)
    p = dq / 2
    plt.plot(q, p, marker, color=plt.get_cmap("winter")(col))

# Definimos una función para calcular D_t
def D_t(t, a_q0 , a_dq0 , F, d):
    q2 = np.array([])
    p2 = np.array([])
    n = int(t / d)
    for q0 in a_q0:
        for dq0 in a_dq0:
            q = orb(n, q0, dq0, F, d)
            dq = deriv(q, dq0, d)
            p = dq / 2
            q2 = np.append(q2, q[-1])
            p2 = np.append(p2, p[-1])
    X = np.array([q2, p2]).T
    return q2, p2, X

# Definimos una función para calcular el área de D_t
def calcular_area(q2,p2):
    X_aux = np.column_stack((q2, p2))
    vertices = alphashape(X_aux, alpha=2.)
    polygon = Polygon(vertices)
    area = polygon.area
    return area, vertices


# APARTADO 1: Espacio fásico D_(0,\infty) para al menos 20 órbitas con
# condiciones iniciales D_0=[0,1]x[0,1]


fig = plt.figure(figsize=(8, 5))
fig.subplots_adjust(hspace=0.4, wspace=0.2)
ax = fig.add_subplot(1, 1, 1)

# a la hora de usar la función simpléctica, es importante escoger un n
# suficiéntemente grande para que a la hora de representar gráficamente
# el espacio fásico las órbitas aparezcan completas, un n válido será
# el natural m que a continuación calculamos.
Horiz = 12
d = 10**(-3)
m = int(Horiz/d)


seq_q0 = np.linspace(0., 1., num=10)
seq_dq0 = np.linspace(0., 2., num=10)

for i in range(len(seq_q0)):
    for j in range(len(seq_dq0)):
        q0 = seq_q0[i]
        dq0 = seq_dq0[j]
        col = (1+i+j*(len(seq_q0)))/(len(seq_q0)*len(seq_dq0))
        simplectica(q0=q0, dq0=dq0, F=F, marker='-', col=col, d=d, n=m)

ax.set_xlabel("q(t)", fontsize=12)
ax.set_ylabel("p(t)", fontsize=12)

plt.show()

# APARTADO 2: Área de D_t para t=1/3 y cálculo del error

# Definimos las condiciones iniciales
t = 1/3
a_q0 = np.linspace(0., 1., num=25)
a_dq0 = np.linspace(0., 2., num=25)
d = 10**(-3)

# Calculamos área de D_t en el tiempo t=1/3
q2, p2, X= D_t(t, a_q0 , a_dq0 , F, d)
area, vertices = calcular_area(q2,p2)

# Graficar espacio fásico p y q para el tiempo t=1/3
plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], c='blue', alpha=0.5)
plt.xlabel('q(t)')
plt.ylabel('p(t)')
plt.title('Espacio Fásico D_t para t=1/3')

# Obtener las coordenadas x e y de los vértices
x, y = vertices.exterior.xy

# Plot de los vértices
plt.scatter(x, y, color='r', label='Vértices')

# Añadir leyenda
plt.legend()

# Imprimir el área calculada por pantalla
print(f'Área de D en t=1/3: {area:.5f}')

# Mostrar gráfico
plt.show()

# considerando los 25*25=625 puntos de las combinaciones de a_q0 con a_dq0 tenemos:
# para d=10**(-3) el área vale 1.00039
# para d=10**(-4) el área vale 0.99998 (más próximo a 1, mejor estimación)
# el error será error=|1.00039 - 0.99998|/2 = 0.000205 (0.0002 en cifras significativas)
# luego el área, considerando una estimación de su intervalo de error, será 1.0002 +- 0.0002.

# APARTADO 3: Realizar una animación GIF del diagrama de fases D_t para t entre (0,5)

# Configuración de parámetros
timesteps = 30  # Número de pasos de tiempo
t_values = np.linspace(0.01, 5, timesteps)  # Valores de tiempo
a_q0 = np.linspace(0., 1., num=25)
a_dq0 = np.linspace(0., 2., num=25)
d = 0.001  # Paso de tiempo

# Realizar la animación y guardar las imágenes en memoria
images = []
for i, t in enumerate(t_values):
    print(f'Procesando D_t para t={t:.2f} (imagen {i + 1}/{timesteps})...')
    q2, p2, X = D_t(t, a_q0, a_dq0, F, d)

    # Graficar el diagrama de fases
    plt.figure(figsize=(8, 6))
    plt.scatter(X[:, 0], X[:, 1], c='blue', alpha=0.5)
    plt.xlabel('q(t)')
    plt.ylabel('p(t)')
    plt.title(f'Espacios Fásicos D_t para t en (0,5)')
    plt.xlim(-1.7, 1.7)
    plt.ylim(-1.5, 1.5)

    # Guardar la imagen en memoria
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    images.append(imageio.imread(buffer))

    plt.close()

# Guardar el GIF animado en disco
print('Creando y guardando el GIF animado...')
output_gif_path = 'D_t-animacion.gif'
imageio.mimsave(output_gif_path, images, format='gif', duration=0.2)  # Ajusta la duración según sea necesario
print(f'¡Animación completa! GIF guardado en: {output_gif_path}')