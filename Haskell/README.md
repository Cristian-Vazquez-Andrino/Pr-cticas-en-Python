# Problema de la Mochila Entera: Algoritmo Genético

## Autor
**Cristian Vázquez Andrino**

---

## Introducción
La práctica trata de resolver el problema de la mochila entera aplicando un **algoritmo genético**. Cada uno de los elementos está implementado y comentado en el archivo `practica.hs`. En este documento haremos un breve resumen del contenido del archivo principal y explicaremos su método de uso.

## Resumen del Contenido del Archivo Principal
El archivo `practica.hs` comienza explicando el problema de la mochila entera, qué es un algoritmo genético y cuáles son las ventajas de su uso en problemas como el de la mochila entera. 

A continuación, se definen (o renombran) los **tipos** con los que vamos a trabajar y se implementan algunas **operaciones básicas** asociadas a ellos. Luego, se implementa el **algoritmo genético** completo. A continuación se describen las funciones clave:

- **`generarIndividuo`**: Genera una mochila-solución, es decir, una mochila que sea una solución factible al problema para unos objetos y un peso máximo dados.

- **`generarPoblacion`**: Con ayuda de `generarIndividuo`, genera `N` mochilas-solución para un `N` dado.

- **`aptitud`**: Calcula la suma de los valores de los objetos en una mochila-solución dada.

- **`seleccion`**: Selecciona los individuos de la población que se reproducirán. Dadas una población, un número máximo de individuos para reproducirse, una probabilidad base y una influencia (valor mayor a 0, generalmente menor a 100), calcula una probabilidad de selección en función de la aptitud del individuo y la influencia establecida.

- **`cruzamiento`**: Cruza las mochilas-solución entre sí usando una porción (`valor entre 0 y 1`) que indica cómo combinar las mochilas padres. Usa la función `ajustarPeso` para asegurarse de que la mochila resultante no exceda el peso máximo.

- **`mutacion`**: Evalúa cada objeto de cada mochila de la población y, con una probabilidad de mutación, cambia ese objeto por otro que mantenga la solución factible.

- **`reemplazo`**: Toma los `N` mejores individuos para formar la nueva población, asegurando que el tamaño se mantenga.

- **`evolucionarPoblacion`**: Evoluciona la población una vez aplicando los procesos de selección, cruzamiento, mutación y reemplazo.

- **`evolucionarPoblacionS`**: Evoluciona la población `N` veces.

- **`algoritmoGenetico`**: Genera una población inicial y la evoluciona `N` veces, devolviendo una población final evolucionada.

Para el correcto funcionamiento de estas funciones, se utilizan varias funciones auxiliares, como la mencionada `ajustarPeso`. Todas estas funciones están descritas con detalle dentro del archivo `practica.hs`.

## Método de Uso
La aplicación del algoritmo genético al problema de la mochila que se quiera resolver se realiza a través de la función `main`. A continuación, se detalla su funcionamiento:

- **`main`**: Dado un archivo de entrada con la misma estructura que `ejemplo_entrada.txt` y un archivo de salida:
  
  1. Aplica el algoritmo genético con los valores introducidos en el archivo de entrada.
  2. Elimina las mochilas-solución repetidas en la población evolucionada, escribiendo en el archivo de salida la población reducida.
  3. Escribe en el archivo de salida la mejor mochila de la población evolucionada (la que tiene mayor valor).
  4. Escribe en el archivo de salida el peso llevado por la mejor mochila de la población evolucionada.

## Notas Finales

- El programa es más rápido generando **poblaciones pequeñas** (20-50 individuos) y evolucionándolas muchas veces (100-200) que generando poblaciones más grandes y evolucionándolas menos veces. En cualquier caso, la calidad de las soluciones es similar.
  
- **Recomendaciones de parámetros**:
  - Probabilidad de mutación: **5% a 15%**.
  - Influencia: **100**.
  - Probabilidad base de selección: **20%**.
  - Número de individuos seleccionados para cruzarse: no más del **20%** de la población total.
  
- Cambiar la **semilla** en cada prueba puede ser más útil que modificar los demás parámetros.
