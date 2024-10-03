AUTOR: Cristian Vázquez Andrino


INTRODUCCIÓN


La práctica trata de resolver el problema de la mochila entera aplicando un algoritmo genético. Cada una de ellas 
está implementada y comentada en el archivo "practica.hs", por tanto, en este documento haremos un breve resumen
del contenido del archivo principal y explicaremos su método de uso.


RESUMEN DEL CONTENIDO DEL ARCHIVO PRINCIPAL


El archivo "practica.hs" comienza explicando el problema de la mochila entera, qué es un algoritmo genético y 
cuales son las ventajas de su uso en problemas como el de la mochila entera. A continuación se definen (o 
renombran) los tipos con los que vamos a trabajar y se definen unas operaciones básicas asociadas a ellos.
Posteriormente se implementa todo el algoritmo genético. Las funciones claves para ello son:

- generarIndividuo: genera una mochila-solución, es decir, una mochila que sea solución factible al problema de 
la mochila para unos objetos y un peso máximo dados.

- generarPoblacion: apoyándonos en la función generarIndividuos, genera N mochilas-solución, para N dado.

- aptitud: calcula la suma de los valores de los objetos que lleva una mochila-solución dada.

- seleccion: dadas una población, el número máximo de individuos seleccionados para reproducirse entre sí, una 
probabilidad base y una influencia (un valor mayor que 0, mi recomendación es que sea menor de 100), selecciona 
los individuos que se reproducirán conforme a la probabilidad de selección, está será la probabilidad base más 
una probabilidad extra constituida por la aptitud del individuo y la influencia que le hayamos dado a esta (0
equivale a 0%, pero 100 NO equivale entorno al 100%, depende del individuo, el funcionamiento de este parámetro 
está detallado con rigor en el archivo principal).

- cruzamiento: dados unos individuos seleccionados y una porción (valor entre 0 y 1), cruza las mochilas-solución
entre sí seccionandolas por la porción dada, por ejemplo, si la porción es 0.25, para una mochila padre y una 
mochila madre, la mochila-solución hijo será el primer 25% de la mochila padre y el 75% último de la mochila madre 
(pasada por una función filtro llamada "ajustarPeso", que para una mochila dada asegura que la mochila resultante 
no lleva más peso del que la mochila es capaz de llevar, eliminando elementos aleatorios de la mochila introducida 
hasta que esto se cumpla).

- mutacion: dada una probabilidad de mutación y una población, la función evalua cada objeto de cada mochila de la
población y en dicha evalución tiene una probabilidad (la propia probabilidad de mutación), de cambiar ese objeto 
por otro que no haga que la mochila-solución deje de ser una solución factible (es decir, que no exceda el peso 
máximo de la mochila).

- reemplazo: dada la población no mutada, los nuevos individuos y la población mutada, toma los N mejores 
individuos, siendo N el número de individuos que había en la población inicial, antes del cruzamiento.

- evolucionarPoblacion: para una población dada aplica los procesos de selección, cruzamiento, mutación y 
reemplazo, evolucionando una vez la población.

- evolucionarPoblacionS: para una población y un valor N dados, evoluciona N veces dicha población.

- algoritmoGenetico: genera una población inicial y la evoluciona N veces con la función anterior. Devolviendo una
población que ha sido evolucionanda N veces.

Sin embargo, para el correcto funcionamiento de estas funciones hay una gran cantidad de funciones auxiliares (como
la ya explicada "ajustarPeso"), todas ellas descritas con detalle dentro del propio archivo "practica.hs".


MÉTODO DE USO


La forma de aplicar el algoritmo genético al problema de la mochila en cuestión que queramos resolver es a través de
la función "main". A continuación, se detalla su funcionamiento:

- main: dados un archivo de entrada con la misma estructura de "ejemplo_entrada.txt" y un archivo de salida:

 1. Aplica el algoritmo genético en función de los valores introducidos en el archivo de entrada.

 2. Elimina las mochilas-solución repetidas en la población evolucionada producida por el algoritmo genético,
    escribiendo en el archivo de salida dicha población reducida. 

 3. Escribe en el archivo de salida la mejor mochila de la población evolucionada (la que más valor lleva).

 4. Por último, escribe en el archivo de salida el peso llevado por la mejor mochila de la población evolucionada.

Notas finales: 

- El programa es más rápido generando poblaciones de pocos individuos (20-50) y evolucionándolas muchas veces 
(100-200) que generando poblaciones más grandes y evolucionándolas menos veces. Aunque en cualquier caso devuelve
soluciones parecidas.

- Recomiendo que la probabilidad de mutación oscile entre el 5% y el 15%.

- Recomiendo que la influencia tome el valor 100 y que la probabilidad base de selección sea del 20%.

- Recomiendo que no se seleccionen una cantidad de individuos superior al 20% de la población  total para 
cruzarse entre sí.

- Recomiendo cambiar la semilla en cada prueba, en vez de cambiar solamente el resto de parámetros.

