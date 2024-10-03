# Huffman Coding Practice

## Autor
Cristian Vázquez Andrino

## Descripción
El objetivo principal de esta práctica es hallar el código Huffman binario de los alfabetos del inglés y del español, denominados `S_Eng` y `S_Esp`, respectivamente. 

Una vez obtenidos ambos códigos, se comprobará que satisfacen el Primer Teorema de Shannon.

## Funcionalidades
1. **Codificación de la palabra "Lorentz"**: 
   - Codificación utilizando los códigos `S_Eng` y `S_Esp`.
   - Codificación en binario usual para comparar la eficiencia de longitud de los códigos Huffman frente al método binario estándar.

2. **Decodificación de Palabras o Textos**: 
   - Desarrollo de un programa para decodificar cualquier palabra o texto codificado con alguno de los códigos Huffman obtenidos.

## Archivos del Proyecto
- **`Codigo_de_Huffman.py`**: Contiene la implementación del código de Huffman, así como las funciones necesarias para las tareas de codificación y decodificación.
- **`pract1_auxiliar_eng.txt`**: Muestra de texto en inglés utilizada para generar el código Huffman `S_Eng`.
- **`pract1_auxiliar_esp.txt`**: Muestra de texto en español utilizada para generar el código Huffman `S_Esp`.

Revisa el enunciado de la práctica y los comentarios dentro del script para más información detallada sobre el proceso y los resultados.

## Uso
Para ejecutar el script, simplemente ejecuta el archivo `Codigo_de_Huffman.py`. Asegúrate de tener los archivos `pract1_auxiliar_eng.txt` y `pract1_auxiliar_esp.txt` en el mismo directorio.

```sh
python Codigo_de_Huffman.py
