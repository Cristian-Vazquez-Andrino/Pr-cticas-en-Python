# Código de Huffman y Teorema de Shanon

## Autor
Cristian Vázquez Andrino

## Descripción
El objetivo principal de la práctica es hallar el código Huffman binario de los alfabetos del
inglés y el español, que denominaremos `S_Eng` y `S_Esp`, respectivamente. Una vez los hayamos
obtenido, comprobaremos que ambos códigos satisfacen el Primer Teorema de Shannon.

Seguidamente, codificaremos la palabra Lorentz en ambos códigos y también en binario
usual, con la motivación de poner de manifiesto la eficiencia de longitud de los dos primeros
códigos frente al último.

Por último, desarrollaremos un programa para decodificar cualquier palabra o texto
codificado en alguno de los dos códigos Huffman obtenidos (o en cualquier otro). A su vez,
probaremos que funciona con el resultado del apartado anterior.

## Archivos del Proyecto
- **`Codigo_de_Huffman.py`**: Contiene la implementación del código de Huffman, así como las funciones necesarias para las tareas de codificación y decodificación.
- **`pract1_auxiliar_eng.txt`**: Muestra de texto en inglés utilizada para generar el código Huffman `S_Eng`.
- **`pract1_auxiliar_esp.txt`**: Muestra de texto en español utilizada para generar el código Huffman `S_Esp`.

Revisa el enunciado de la práctica y los comentarios dentro del script para más información detallada sobre el proceso y los resultados.

## Uso
Para ejecutar el script, simplemente ejecuta el archivo `Codigo_de_Huffman.py`. Asegúrate de tener los archivos `pract1_auxiliar_eng.txt` y `pract1_auxiliar_esp.txt` en el mismo directorio.
