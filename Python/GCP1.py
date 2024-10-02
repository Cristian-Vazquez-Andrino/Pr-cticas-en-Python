# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 13:27:30 2024

@author: usu458
"""

"""
Práctica 1. Código de Huffmann y Teorema de Shannon
"""

import os
import numpy as np
import pandas as pd

#### Vamos al directorio de trabajo
os.getcwd()
#os.chdir(ruta)
#files = os.listdir(ruta)

with open('GCOM2024_pract1_auxiliar_eng.txt', 'r',encoding="utf8") as file:
      en = file.read()
     
with open('GCOM2024_pract1_auxiliar_esp.txt', 'r',encoding="utf8") as file:
      es = file.read()


#### Contamos cuantos caracteres hay en cada texto
from collections import Counter
tab_en = Counter(en)
tab_es = Counter(es)


#### Transformamos en formato array de los carácteres (states) y su frecuencia
#### Finalmente realizamos un DataFrame con Pandas y ordenamos con 'sort'
tab_en_states = np.array(list(tab_en))
tab_en_weights = np.array(list(tab_en.values()))
tab_en_probab = tab_en_weights/float(np.sum(tab_en_weights))
distr_en = pd.DataFrame({'states': tab_en_states, 'probab': tab_en_probab})
# Ordenamos en función de la probabilidad:
distr_en = distr_en.sort_values(by='probab', ascending=True)
distr_en.index=np.arange(0,len(tab_en_states)) # Reordenamos los índices

tab_es_states = np.array(list(tab_es))
tab_es_weights = np.array(list(tab_es.values()))
tab_es_probab = tab_es_weights/float(np.sum(tab_es_weights))
distr_es = pd.DataFrame({'states': tab_es_states, 'probab': tab_es_probab })
distr_es = distr_es.sort_values(by='probab', ascending=True) 
distr_es.index=np.arange(0,len(tab_es_states)) 

##### Para obtener una rama, fusionamos los dos states con menor frecuencia
def huffman_branch(distr):
    states = np.array(distr['states'])
    probab = np.array(distr['probab'])
    state_new = np.array([''.join(states[[0,1]])])
    probab_new = np.array([np.sum(probab[[0,1]])])
    # El código es un array con un diccionario que asigna un 0 al elemento con
    # menos probabilidad y un 1 al restante
    codigo = np.array([{states[0]: 0, states[1]: 1}])
    # Concatenamos el nuevo elemento con la lista sin los dos primeros 
    # elementos:
    states =  np.concatenate((states[np.arange(2,len(states))], state_new), axis=0)
    # Hacemos lo mismo con la probabilidad:
    probab =  np.concatenate((probab[np.arange(2,len(probab))], probab_new), axis=0)
    # A continuación creamos una nueva tabla de datos a partir de esta nueva
    # colección, y la ordenamos en función de la probabilidad:
    distr = pd.DataFrame({'states': states, 'probab': probab})
    distr = distr.sort_values(by='probab', ascending=True)
    distr.index=np.arange(0,len(states))
    # Por último creamos un diccionario compuesto por la nueva tabla de datos
    # y el código
    branch = {'distr':distr, 'codigo':codigo}
    return(branch) 

def huffman_tree(distr):
    tree = np.array([])
    while len(distr) > 1:
        branch = huffman_branch(distr)
        distr = branch['distr']
        code = np.array([branch['codigo']])
        tree = np.concatenate((tree, code), axis=None)
    return(tree)
 
distr = distr_en 
tree = huffman_tree(distr)
tree[0].items()
tree[0].values()

def huffman_code(tree):
    
    return

def anadir0(n):
    return n*10

def anadir1(n):
    return n*10+1

#Buscar cada estado dentro de cada uno de los dos items
list(tree[0].items())[0][1] ## Esto proporciona un '0'
list(tree[0].items())[1][1] ## Esto proporciona un '1'