# -*- coding: utf-8 -*-
"""
Autor: Cristian Vázquez Andrino
"""

"""
Práctica 1. Código de Huffmann y Teorema de Shannon.
"""

import os
import math
import numpy as np
import pandas as pd
from collections import Counter

en='pract1_auxiliar_eng.txt'
es='pract1_auxiliar_esp.txt'

# A partir de una muestra dada la siguiente función crea el DataFrame 
# que presenta los caracteres que aparecen en la muestra y la probabilidad
# asociada a cada uno de ellos.
def tabla(muestra):
    os.getcwd()
    with open(muestra, 'r',encoding="utf8") as file:
          m = file.read()
    # Contamos cuantos caracteres hay en la muestra
    dict_m = Counter(m)
    # Transformamos en formato array de los carácteres y su frecuencia
    # Finalmente realizamos un DataFrame con Pandas y ordenamos con 'sort'
    chars_m = np.array(list(dict_m))
    frecuencias_m = np.array(list(dict_m.values()))
    probs_m = frecuencias_m/float(np.sum(frecuencias_m))
    tabla_m = pd.DataFrame({'caracteres': chars_m, 'probabilidades': probs_m})
    # Ordenamos en función de la probabilidad:
    tabla_m = tabla_m.sort_values(by='probabilidades', ascending=True)
    tabla_m.index=np.arange(0,len(chars_m)) # Reordenamos los índices
    return tabla_m

# Dada una tabla apropiada, aplica el algoritmo de Huffman concatenando los dos
# primeros elementos de la tabla (aquellos con menos frecuencia) y reordenando
# la nueva tabla resultante. 
def huffman_branch(t):
    chars = np.array(t['caracteres'])
    probs = np.array(t['probabilidades'])
    char_n = np.array([''.join(chars[[0,1]])])
    prob_n = np.array([np.sum(probs[[0,1]])])
    # El código es un array con un diccionario que asigna un 0 al elemento con
    # menos probabilidad y un 1 al restante
    codigo = np.array([{chars[0]: '0', chars[1]: '1'}])
    # Concatenamos el nuevo elemento con la lista sin los dos primeros 
    # elementos:
    chars =  np.concatenate((chars[np.arange(2,len(chars))], char_n), axis=0)
    # Hacemos lo mismo con la probabilidad:
    probs =  np.concatenate((probs[np.arange(2,len(probs))], prob_n), axis=0)
    # A continuación creamos una nueva tabla de datos a partir de esta nueva
    # colección, y la ordenamos en función de la probabilidad:
    t = pd.DataFrame({'caracteres': chars, 'probabilidades': probs})
    t = t.sort_values(by='probabilidades', ascending=True)
    t.index=np.arange(0,len(chars))
    # Por último creamos un diccionario compuesto por la nueva tabla de datos
    # y el código
    branch = {'tabla':t, 'código':codigo}
    return(branch) 

# Dada una tabla apropiada, te devuelve el arbol asociado por el algoritmo de
# Huffman.
def huffman_tree(t):
    tree = np.array([])
    while len(t) > 1:
        branch = huffman_branch(t)
        t = branch['tabla']
        code = np.array([branch['código']])
        tree = np.concatenate((tree, code), axis=None)
    return(tree)

# Dado un arbol apropiado, te devuelve la codificación de Huffman de los 
# caracteres implicados.
def huffman_code(tree):
    code={}
    l=len(list(tree))
    for k in range (0,l-1):
        for j in range (1,-1,-1):
            a=list(tree[k].items())[j][0]
            if len(a)==1:
                c=list(tree[k].items())[j][1] 
                for i in range (k+1,l):
                    if a in list(tree[i].items())[1][0]:
                        b= list(tree[i].items())[1][1]
                        c=b+c
                    elif a in list(tree[i].items())[0][0]:
                        b= list(tree[i].items())[0][1]
                        c=b+c
                code[a]=c
    return code

# Combina todas las funciones anteriores, aplicando el algoritmo de Huffman  
# completo y proporcionando la codificación de Huffman.
def huffman(muestra):
    t=tabla(muestra)
    tree=huffman_tree(t)
    code=huffman_code(tree)
    return code

# Dados una codificación de Huffman y una palabra o texto apropiados para 
# dicha codificación, los codifica.
def codificar(code,txt):
    txt_c=""
    for i in txt:
        txt_c += code[i]
    return txt_c

# Calculamos el número total de estados (caracteres) de una muestra dada.
def obtener_N(muestra):
    os.getcwd()
    with open(muestra, 'r',encoding="utf8") as file:
          m = file.read()
    n=len(m)
    return n

# Dada una muestra, a partir del sistema que genera, calcula H (la entropía 
# total del sistema).
def obtener_H(muestra):
    t=tabla(muestra)
    probs=list(t['probabilidades'])
    for i in range (0,len(probs)):
        probs[i] = probs[i]*math.log(probs[i],2)
    h = -1 * sum(probs)
    return h

# Dada una muestra, calculamos ΔH.
def error_H(muestra):
    t=tabla(muestra)
    probs=list(t['probabilidades'])
    n= obtener_N(muestra)
    for i in range (0,len(probs)):
        probs[i] = (math.log(probs[i],2)+1/(math.log(2,math.e)))**2
    e = 1/n * math.sqrt(sum(probs))
    return e

# Dada una muestra, calcula L (del algoritmo de Huffman).
def obtener_L(muestra):
    t=tabla(muestra)
    probs=list(t['probabilidades'])
    cs = list(huffman(muestra).values())
    w= sum(probs)
    s = 0
    for i in range (0,len(cs)):
        s += len(cs[i])*probs[i]
    l = s/w
    return l

# Dada una muestra, calculamos ΔL.
def error_L(muestra):
    cs = list(huffman(muestra).values())
    n= obtener_N(muestra)
    s = 0
    for i in range (0,len(cs)):
        s += len(cs[i])**2
    e = 1/n * math.sqrt(s)
    return e



# EJERCICIO 1:

# Códigos Huffman binarios de S_Eng y S_Esp, respectivamente:
code_en=huffman(en)
code_es=huffman(es)

# A continuación vamos a ver que se satisface el Primer Teorema de Shannon.
# Para ello calculamos H(C) y L(C) a partir de las muestras en y es, 
# respectivamente. Después comprobamos que en ambos casos H(C) <= L(C) < H(C)+1:

# Primero calculamos una primera aproximación a H y L de ambas muestras sin  
# tener en cuenta el error ni las cifras significativas:

en_H=obtener_H(en) # en_H = 4.2827303843795885 
es_H=obtener_H(es) # es_H = 4.27846906600711

en_L=obtener_L(en) # en_L = 4.303754266211605
es_L=obtener_L(es) # es_L = 4.304285714285715

# A continuación calculamos ΔH y ΔL:

error_en_H=error_H(en) # error_en_H = 0.055803658127588085
error_es_H=error_H(es) # error_es_H = 0.05185850846005321


error_en_L=error_L(en) # error_en_L = 0.06887520843211797
error_es_L=error_L(es) # error_es_L = 0.0662401321106836

# Por tanto, tenemos que para la muestra en inglés:
# H ± ΔH = 4,28 ± 0.05 < L ± ΔL = 4,30 ± 0.06 < H ± ΔH + 1 = 5,28 ± 0.05

# Y para la muestra en español:
# H ± ΔH = 4,27 ± 0.05 < L ± ΔL = 4,30 ± 0.06 < H ± ΔH + 1 = 5,27 ± 0.05

# Luego, se cumple el Teorema de Shannon.



# EJERCICIO 2:
    
# Palabra "Lorentz" codificada según los códigos anteriores (primero en inglés
# y luego en español):
en_Lorentz = codificar(code_en,"Lorentz")
# en_Lorentz = '01000110100001010011011101011111001'
es_Lorentz = codificar(code_es,"Lorentz")
# es_Lorentz = '11111000100101100101000111011101101'

# La palabra "Lorentz" en código binario usual es:
bin_Lorentz = '01001100 01101111 01110010 01100101 01101110 01110100 01111010'

# len(bin_Lorentz) = 62 (56 sin contar espacios), mientras que len(en_Lorentz)
# = len(es_Lorentz) = 35. Notable diferencia a favor de las codificaciones de
# Huffman.



# EJERCICIO 3:        

# Dados una codificación de Huffman y una palabra o texto codificados según
# dicha codificación, los decodifica.
def decodificar(code,txt_c):
    txt = ""
    l=list(code)
    l_v=list(code.values())
    b = ""
    for i in txt_c:
        b += i
        if b in l_v:
            indice=l_v.index(b)
            c=l[indice]
            txt += c
            b=""
    return txt

prueba_en = decodificar(code_en,codificar(code_en,"Lorentz"))
prueba_es = decodificar(code_es,codificar(code_es,"Lorentz"))
# Se tiene que prueba_en = prueba_es = "Lorentz".










