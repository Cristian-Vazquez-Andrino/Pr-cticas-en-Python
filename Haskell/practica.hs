-- AUTOR: Cristian Vázquez Andrino

{- 
El problema de la mochila entera se trata de un problema de optimización en el que tenemos una 
mochila con capacidad limitada y unos objetos (que no se pueden fraccionar). Cada objeto tiene un 
peso y un valor determinados y el objetivo es conseguir llevar el mayor valor posible sin exceder
la capacidad máxima de peso de la mochila.

El problema de la mochila entera es un problema NP-completo, si queremos resolverlo para n objetos
existen 2^n grupos de objetos entre los que escoger el mejor en relación valor-peso, lo cuál hace
que el problema sea inabordable para n grande. Por ello, para encarar este problema se emplean 
métodos que sacrifican la garantía de obtener la solución óptima a cambio de obtener una solución
decente en un tiempo razonable. Un ejemplo de ello son los algoritmos genéticos. 

Los algoritmos genéticos son métodos de optimización inspirados en la evolución biológica. La idea 
de este tipo de algoritmos es la siguiente:

- Inicialización: tomar una "población inicial" de posibles soluciones al problema que se quiere  
abordar, esa población inicial está formada por "individuos" elegidos al azar, cada individuo se
identifica por sus "genes", que es con lo que verdaderamente trabajamos. Sin embargo, como nos 
referimos a cada individuo por sus genes constantemente llamaremos "individuo" a sus genes, que 
precisamente representan soluciones factibles del problema de optimización a tratar.

- Evaluación: el algoritmo procede a evaluar a cada individuo mediante una función de "aptitud" que 
indica como de "bien adaptado" se encuentra el individuo en cuestión (es decir, como de buena es 
dicha solución para el problema). 

Posteriormente comienzan a generar nuevas "generaciones" de individuos, se trata deuna busqueda 
recursiva de mejores soluciones  del problema mediante esta población inicial, que terminará cuando
o bien se haya alcanzado un número máximo de iteraciones, o bien deje de haber cambios en la 
población. El método para producir nuevas generaciones consta de los siguientes 4 pasos:

- Selección: se escogen individuos de la población vigente para "reproducirlos". Esta selección no 
se hace al azar, puesto que los individuos con mejor aptitud tendrán mayor probabilidad de ser 
escogidos. 

- Cruzamiento: los individuos se reproducen, dando lugar a nuevos individuos, es decir, de cierta 
forma las soluciones se van mezclando entre sí produciendo nuevos candidatos a mejores soluciones del 
problema.

- Mutación: algunos individuos sufren una mutación genética, se trata de una modificación azarosa de
parte de sus genes. El objetivo de esto es abrir nuevos caminos en la búsqueda de una mejor solución
que pudieran no estar aún presentes en la población vigente. 

- Reemplazo: finalmente, se seleccionan a los mejores individuos que reemplazarán la anterior generación.

El objetivo de esta práctica es resolver el problema de la mochila entera mediante un algoritmo genético.
-}
{- 
Lo primero que vamos a hacer es importar "System.Random", lo necesitaremos para generar valores 
aleatorios. Las funciones mkStdGen, randomRs, randoms y randomR son las únicas que usaremos del paquete 
Random en toda la práctica, por ello me parece apropiado explicar brevemente que hace cada una de ellas. 
La función mkStdGen :: Int -> StdGen recibe un entero, devuelve un generador de valores pseudoaleatorios 
(cuyo tipo es StdGen) asociado a dicho entero. La función randomRs :: Random a => (a, a) -> StdGen -> [a] 
toma un rango de valores (cuyo tipo es randomizable), toma un generador de valores psudoaleatorios y 
produce una lista infinita de valores pseudoaleatorios, todos ellos dentro del rango introducido. La 
función randoms :: (RandomGen g, Random a) => g -> [a] toma un generador de números pseudoaleatorios, un 
valor de tipo randomizable y devuelve una lista infinita de valores (de dicho tipo randomizable). Por 
último, la función randomR :: Random a => (a, a) -> StdGen -> (a, StdGen) dado un rango (de valores de 
tipo randomizable) y un generador de valores pseudoaleatorios devuelve un único valor aleatorio (dentro 
del rango introducido) y el estado del generador en una misma tupla.

Detallemos un poco más las 2 clases que han aparecido en los tipos de estas funciones: Random es una clase de 
tipos que aceptan una representación aleatoria (es decir, tipos randomizables) y RandomGen es la clase de tipos 
de generadores de valores pseudoleatorios (como el tipo StdGen, el único con la que trabajaremos).
-}

import System.Random

-- Comenzamos definiendo los tipos con los que vamos a trabajar: objetos y mochilas:

-- Cada objeto será definido por dos enteros: el primero será su peso, el segundo su valor
data Objeto = Objeto Int Int
    deriving (Eq, Read, Show)



-- Renombraremos el tipo "[Objeto]" como "Mochila", por ser esta una lista de objetos.
type Mochila = [Objeto]



-- En lo venidero usaremos las siguientes dos funciones básicas: 

-- La siguiente función, dado un objeto te devuelve su peso.
pesoObj:: Objeto -> Int
pesoObj (Objeto p v) = p



-- La siguiente función, dada una mochila te devuelve la suma del peso de los objetos que contiene.
sumPeso :: Mochila -> Int
sumPeso mochila = sum (map pesoObj mochila)



-- La siguiente función, dado un objeto te devuelve su valor.
valorObj::Objeto -> Int
valorObj (Objeto p v) = v



{- La siguiente función, dada una mochila y un objeto te devuelve un booleano 
que indica si el objeto está en la mochila. -}
pertenece:: Mochila -> Objeto -> Bool
pertenece [] objeto = False
pertenece (objeto':mochila) objeto
    | objeto'==objeto = True
    | otherwise = pertenece mochila objeto



-- La siguiente función elimina las mochilas repetidas en una lista de mochilas.
eliminarRepeticiones::[Mochila]-> [Mochila]
eliminarRepeticiones []=[]
eliminarRepeticiones [x]=[x]
eliminarRepeticiones (x:xs) = x:eliminarRepeticiones(eliminarMochila x xs)



-- La siguiente función elimina una mochila de una lista de mochilas.
eliminarMochila:: Mochila -> [Mochila] -> [Mochila]
eliminarMochila _ [] = []
eliminarMochila x (y:xs)
    | iguales x y = eliminarMochila x xs
    | otherwise = y: eliminarMochila x xs



-- La siguiente función determina si dos mochilas dadas tienen los mismos elementos.
iguales:: Mochila -> Mochila -> Bool
iguales [] [] = True
iguales [] _ = False
iguales _ [] = False
iguales (x:xs) ys = elem x ys && iguales xs (eliminarObjeto x ys)



-- La siguiente función elimina un objeto de una mochila
eliminarObjeto:: Objeto -> Mochila -> Mochila 
eliminarObjeto _ [] = []
eliminarObjeto x (y:xs)
    | x==y = eliminarObjeto x xs
    | otherwise = y: eliminarObjeto x xs



{- 
Tratando el problema de la mochila con un algoritmo genético, un individuo (una posible solución del 
problema) es un subconjunto del conjunto de objetos de los que disponemos tales que la suma de sus 
pesos es menor al peso máximo que la mochila puede almacenar, es lo que llamaremos "mochila-solución".
Cada individuo es una "mochila-solución" porque es una solución factible del problema de la mochila. 
Cuando en el tipo de una función aparece el tipo "Mochila", nos referimos a una "mochila-solución", 
cuando aparece [Objetos] nos referimos a una "lista de objetos" que no tiene porque ser una mochila 
solución, y cuando aparace el tipo "[Mochila]" nos referiremos a la población de individuos vigente.
Como hemos comentado al principio, un algoritmo genético tratará de generar al individuo mejor 
adaptado; traducido a este problema: la mochila-solución que mas valor es capaz de almacenar. 

A continuación, introducimos una función para generar una población, dicha población se obtendrá 
de manera aleatoria, usando las funciones mkStdGen y randomRs obtenidas alimportar "System.Random". 
La función aceptará el tamaño que queremos que tenga la población (número de posibles soluciones 
generadas), la lista de objetos de la que disponemos, el peso máximo que la mochila puede almacenar y 
la semilla para el generador de valores pseaudoaleatorios, en ese orden. Lo que devolverá será una 
lista de posibles mochilas óptimas (formadas todas ellas por elementos de la misma lista inicial dada).
-}
generarPoblacion:: Int -> [Objeto] -> Int -> Int -> [Mochila]
generarPoblacion tamPoblacion objetos pesomax semilla =
    take tamPoblacion ( map (generarIndividuo objetos pesomax) (randomRs (0, semillaux) (mkStdGen semilla)))
    where semillaux = sum [tamPoblacion, length objetos, pesomax, semilla]
{- en ocasiones usaremos una variable como "semillaux", que funciona como una "semilla auxiliar", 
cambiando según los valores de entrada de la función en cuestión -}



{- En la función anterior vemos la llamada a la función generarIndividuo. Esta función genera una 
mochila-solución a partir de la lista de objetos que disponemos y del peso máximo. -}
generarIndividuo:: [Objeto] -> Int -> Int -> Mochila
generarIndividuo objetos pesomax semilla =
    ajustarPeso (map snd ( filter fst (zip bools objetos) )) pesomax semilla
    where bools = take (length objetos) (randoms (mkStdGen semilla) :: [Bool])



-- La siguiente función saca aleatoriamente elementos de la mochila hasta que esta no exceda su peso máximo.
ajustarPeso:: Mochila -> Int -> Int -> Mochila
ajustarPeso mochila pesomax semilla
    | sumPeso mochila <= pesomax = mochila
    | otherwise = ajustarPeso (reducir mochila (semilla + 1)) pesomax (semilla + 2)
{- en ocasiones se toma "semilla+n" como una semilla en una llamada recursiva o a otra
función, se hace para cambiar de semilla constantemente y aumentar la "aleatoriedad"
ligada a la semilla inicial -}



-- La siguiente función elimina un elemento aleatorio de la mochila.
reducir:: Mochila -> Int -> Mochila
reducir mochila semilla = take indiceAleatorio mochila ++ drop (indiceAleatorio + 1) mochila
    where indiceAleatorio = fst (randomR (0, length mochila - 1) (mkStdGen (semilla + 3)))



{- Nótese que las funciones ajustarPeso, sumPeso y reducir se han diseñado para asegurarnos
de que la mochila generada sea una mochila-solución, es decir, un individuo válido para
nuestra población, ya que sin estas funciones se podrían generar mochilas no válidas, pues
podrían exceder el peso total permitido. -}

{-Como hemos explicado al principio, en un algoritmo genético la función aptitud determina 
como de bien adaptado está un invididuo, en este problema determina como de buena solución
es una mochila-solución dada sumando el valor de los objetos que contiene. -}
aptitud :: Mochila -> Int
aptitud mochila = sum (map valorObj mochila)



{- La siguiente función realizará el paso de selección: dada una población, una cierta cantidad
maxima de individuos que se reproducirán, una probabilidad base de selección y un valor que 
determina la influencia en la probabilidad de ser escogidos en función de la aptitud del 
individuo, devuelve los individuos seleccionados para el cruzamiento. -}
seleccion:: [Objeto] -> [Mochila] -> Int -> Int -> Int -> Int -> [Mochila]
seleccion objetos mochilas' numMaxIndividuos probBase influencia semilla
    | null mochilas' = []
    | numMaxIndividuos == 0 = []
    | fst (randomR (0, 100) (mkStdGen semillaux)) <= probSeleccion = mochila:seleccion objetos mochilas (numMaxIndividuos-1) probBase influencia (semilla+1)
    | otherwise = seleccion objetos mochilas numMaxIndividuos probBase influencia (semilla+1)
    where semillaux = sum [numMaxIndividuos, probBase, influencia, semilla]
          (mochila:mochilas) = mochilas'
          probSeleccion = probBase + probExtra objetos mochila influencia c
          c=cota objetos




{- La idea de la siguiente función es devolver una cota superior del máximo valor que puede cargar la 
mochila en función de la mejor relación valor-peso que se puede encontrar entre los objetos de los que 
disponemos. -}
cota:: [Objeto] -> Float
cota objetos = fromIntegral (length objetos) * maximum (map (\obj-> fromIntegral (valorObj obj) / fromIntegral (pesoObj obj)) objetos)



{- La siguiente función, dada la lista de objetos de los que disponemos, una mochila-solución y un valor 
que determina la influencia de la aptitud del individuo y te devuelve la probabilidad (sobre dicho valor) 
de escoger una mochila en el proceso de selección en función de la aptitud de la mochila-solución. -}
probExtra:: [Objeto] -> Mochila -> Int -> Float -> Int
probExtra objetos mochila influencia c = round (fromIntegral influencia * 2 *(fromIntegral (aptitud mochila) / fromIntegral (sumPeso mochila)) / c)



{- La siguiente función realiza el paso de cruzamiento entre las mochilas-solución seleccionadas. Para 
ello llama a la función cruzarMochilas.-}
cruzamiento:: [Mochila] -> Float -> Int -> Int -> [Mochila]
cruzamiento mochilas porcion pesomax semilla = [cruzarMochilas padre madre porcion pesomax semilla | padre <- mochilas, madre <- mochilas]



{- La siguiente función produce un cruce entre dos individuos y produce un individuo válido 
(una solución factible del problema), en este caso toma dos mochilas solución y dada una porción
secciona las listas de objetos de las mochilas según dicha porción mezclándolas (por ejemplo, si 
la porción es 0.3, mezcla el primer 30% de la primera mochila (mochila-solución padre) con el 70% 
de la segunda mochila (mochila-solución madre)) y produciendo una mochila-solución. La función 
tomará las dos mochilas, el índice pero también el peso máximo de la mochila y una semilla para 
poder aplicar la función ajustarPeso. -}
cruzarMochilas :: Mochila -> Mochila -> Float -> Int -> Int -> Mochila
cruzarMochilas padre madre porcion = ajustarPeso (take indicePadre padre ++ drop indiceMadre madre')
    where madre' = filter (`notElem` padre) madre
          indicePadre = round (fromIntegral (length padre)*porcion)-1
          indiceMadre = round (fromIntegral (length madre)*(1-porcion))-1




{- La siguiente función genera cambios aleatorios en los genes de una población. En este problema 
se traduce como realizar cambios en el interior de una mochila-solución. La función mutación se 
aplica sobre toda una población y llama a la función mutarMochila, que evalua la mutación de cada
individuo-}
mutacion :: [Objeto] -> Int -> Int -> Int -> [Mochila] -> [Mochila]
mutacion objetos probMutacion pesomax semilla [] = []
mutacion objetos probMutacion pesomax semilla (mochila:mochilas) = mochila':mochilas'
    where mochila' = mutarMochila objetos probMutacion pesomax semilla mochila mochila
          mochilas' = mutacion objetos probMutacion pesomax (5*semilla+1) mochilas



{- La siguiente función muta una mochila-solución produciendo otra mochila-solución tras evaluar 
la mutación de cada uno de los objetos iniciales mediante "mutarObjeto". -}
mutarMochila:: [Objeto] -> Int -> Int -> Int -> Mochila -> Mochila -> Mochila 
mutarMochila objetos probMutacion pesomax semilla [] mochilaFinal = mochilaFinal
mutarMochila objetos probMutacion pesomax semilla (objeto:mochila) mochilaFinal
    | fst (randomR (0, 100) (mkStdGen semillaux)) < probMutacion = mochila'
    | otherwise = mutarMochila objetos probMutacion pesomax (2*semilla+3) mochila mochilaFinal
    where semillaux = sum [semilla, probMutacion, valorObj objeto, pesoObj objeto, length mochila]
          mochila' = mutarMochila objetos probMutacion pesomax (5*semilla+1) mochila (aleatorio:mochilaFinal')
          mochilaFinal' = eliminarObjeto objeto mochilaFinal
          aleatorio = mutarObjeto objetos mochilaFinal' probMutacion pesomax semilla
          

{- La siguiente función, dada una lista de objetos, una mochila en la que se encuentra el objeto 
que se va a mutar, una probabilidad (entre 0 y 100), una semilla y el propio objeto sobre el que 
se evaluará la mutación, de devuelve, en función de la probabilidad, o bien el propio objeto inicial, 
o bien otro que se encuentre en la lista de objetos pero no en la mochila de entrada. -}
mutarObjeto :: [Objeto] -> Mochila -> Int -> Int -> Int -> Objeto
mutarObjeto objetos mochilaFinal probMutacion pesomax semilla = aleatorio
    where otros = [obj | obj <- objetos, sumPeso (obj:mochilaFinal)<=pesomax && not (pertenece mochilaFinal obj)]
          aleatorio = otros !! fst (randomR (0, length otros -1) (mkStdGen (semilla + 5)))
-- otros = Lista de objetos que no están ya en la mochila y que pueden producir una mochila-solución.



{- La siguiente función, dado un tamaño n y una población, se queda con los n mejores
individuos de la población. -}
reemplazo::[Mochila] -> Int -> [Mochila]
reemplazo mochilas tamPoblacion = take tamPoblacion (ordenarMochilas mochilas)



{- La siguiente función usa el quicksort para ordenar la población mochilas en función 
de su aptitud. -}
ordenarMochilas::[Mochila] -> [Mochila]
ordenarMochilas [] = []
ordenarMochilas (mochila:mochilas) = ordenarMochilas mochilasMejores ++ [mochila] ++ ordenarMochilas mochilasPeores
    where mochilasPeores =  [mochilaPeor | mochilaPeor <- mochilas, aptitud mochilaPeor < aptitud mochila]
          mochilasMejores = [mochilaMejor | mochilaMejor <- mochilas, aptitud mochilaMejor >= aptitud mochila]



{- 
Por último, implementaremos la función "algoritmoGenetico", la cuál toma como parámetros de entrada
la lista de objetos de los que disponemos, el tamaño de la población, el número de generaciones que 
queremos producir, el peso máximo del que dispone la mochila, la número máximo de individuos que 
queremos reproducir, la probabilidad base de ser seleccionado para el cruzamiento, la influencia de 
la aptitud de cada individuo en la probabilidad de ser seleccionado para el cruzamiento, la porción
con la que se seccionan los genes de los individuos a la hora de cruzarse, la probabilidad de mutación 
y una semilla y devuelve una lista de mochilas-solución no repetidas de tamaño menor o igual al tamaño 
de la población introducido. 

La función aplica el método del algoritmo genético tal como se explica al inicio de la práctica, usando 
todas las funciones ya introducidas hasta el momento recogidas en una función auxiliar llamada
"evolucionarPoblacion", que dada una población y todos los parámetros anteriores (salvo numGeneraciones)
aplica los 4 pasos del algoritmo genético (selección, cruzamiento, mutación y reemplazo) produciendo una
nueva población.
-}
algoritmoGenetico:: Int -> [Objeto] -> Int -> Int -> Int -> Int -> Int -> Float -> Int -> Int -> [Mochila]
algoritmoGenetico numGeneraciones objetos tamPoblacion pesomax numMaxIndividuos probBase influencia porcion probMutacion semilla = poblacionFinal
    where poblacionInicial = generarPoblacion tamPoblacion objetos pesomax semilla
          poblacionFinal = evolucionarPoblacionS numGeneraciones objetos tamPoblacion pesomax numMaxIndividuos probBase influencia porcion probMutacion semilla poblacionInicial


-- Como ya se ha explicado, evolucionarPoblación evoluciona una población dada una vez.
evolucionarPoblacion:: [Objeto] -> Int -> Int -> Int -> Int -> Int -> Float -> Int -> Int -> [Mochila] -> [Mochila]
evolucionarPoblacion objetos tamPoblacion pesomax numMaxIndividuos probBase influencia porcion probMutacion semilla poblacion = poblacionNueva
    where poblacionSeleccionada = seleccion objetos poblacion numMaxIndividuos probBase influencia (2*semilla+1)
          nuevosIndividuos = cruzamiento poblacionSeleccionada porcion pesomax (3*semilla+2)
          poblacionMutada = mutacion objetos probMutacion pesomax (5*semilla+3) poblacion
          poblacionNueva = reemplazo (poblacion ++ poblacionMutada ++ nuevosIndividuos) tamPoblacion



-- evolucionarPoblacionS aplica evolucionarPoblacion n veces (es decir, hace evolucionar n veces una población).
evolucionarPoblacionS:: Int -> [Objeto] -> Int -> Int -> Int -> Int -> Int -> Float -> Int -> Int -> [Mochila] -> [Mochila]
evolucionarPoblacionS numGeneraciones objetos tamPoblacion pesomax numMaxIndividuos probBase influencia porcion probMutacion semilla poblacion
    | numGeneraciones > 1 = evolucionarPoblacionS (numGeneraciones-1) objetos tamPoblacion pesomax numMaxIndividuos probBase influencia porcion probMutacion (2*semilla+1) poblacionEvolucionada
    | numGeneraciones == 1 = poblacion 
    where poblacionEvolucionada = evolucionarPoblacion objetos tamPoblacion pesomax numMaxIndividuos probBase influencia porcion probMutacion semilla poblacion



-- A continuación introducimos un ejemplo del uso del algoritmo.
ejemplo:: Int -> Int -> ([Mochila],Mochila, Int)
ejemplo n s = (mochilas, mejor, aptitud mejor)
    where objetos = [Objeto 2 5,Objeto 3 8,Objeto 5 13,Objeto 7 21,Objeto 1 2,Objeto 2 6,Objeto 3 11,Objeto 4 12,Objeto 5 14,Objeto 3 12,Objeto 8 15,Objeto 13 30,Objeto 9 23,Objeto 1 5]
          mochilas = eliminarRepeticiones (algoritmoGenetico n objetos 30 25 10 20 200 0.5 10 s) 
          mejor = head (ordenarMochilas mochilas)
{- Nótese que en la salida se eliminan las mochilas-solución repetidas, en la función entrada-salida 
procederemos de la misma forma, adem´s devolveremos la mejor mochila obtenida y el valor que lleva. -}



{- Ahora introducimos entrada/salida por pantalla y a fichero. La función solicita el nombre de un 
fichero que disponga de los parámetros apropiados para la aplicación del algoritmo genético y devuelve
las mochilas-solución (sin repeticiones) generadas para esos parámetros mediante el algoritmo genético, 
la mejor de ellas y el valor que carga. -}
main :: IO ()
main = do putStr "Introduzca el nombre del fichero de entrada. Este debe proporcionar en lineas consecutivas y en \n el siguiente orden, los siguientes parámetros: \n el número de generaciones que queremos producir, la lista de objetos de los que disponemos, el \n tamaño de la población, el peso máximo del que dispone la mochila, la número máximo de individuos \n que se seleccionarán para reproducirse, la probabilidad base de ser seleccionado para el cruzamiento,\n la influencia de la aptitud de cada individuo en la probabilidad de ser seleccionado para el cruzamiento \n (recomendación: escoger un valor entre 0 y 100), la porción con la que se seccionan los genes de los \n  individuos a la hora de cruzarse (escoger un valor real entre 0 y 1), la probabilidad de mutación y una \n semilla (para generar valores aleatorios). \n"
          inNombre <- getLine
          contenido <- readFile inNombre
          putStr "Introduzca el nombre del fichero de salida. \n"
          outNombre <- getLine
          let salida =  algoritmoGeneticoS contenido  -- llamada a la función que modifica el contenido del fichero
          writeFile outNombre salida



algoritmoGeneticoS:: String -> String
algoritmoGeneticoS txt = lineas mochilas ++ "\n Mejor mochila:" ++ show mejor ++ "\n \n Valor:" ++ show valor
    where p = lines txt
          numGeneraciones = read (head p)::Int
          objetos = read (p!!1)::[Objeto]
          tamPoblacion = read (p!!2):: Int
          pesomax = read (p!!3)::Int 
          numMaxIndividuos = read (p!!4)::Int
          probBase = read (p!!5)::Int
          influencia = read (p!!6)::Int
          porcion = read (p!!7)::Float
          probMutacion = read (p!!8)::Int
          semilla = read (p!!9)::Int
          mochilas = eliminarRepeticiones (algoritmoGenetico numGeneraciones objetos tamPoblacion pesomax numMaxIndividuos probBase influencia porcion probMutacion semilla)
          mejor = head (ordenarMochilas mochilas)
          valor = aptitud mejor



lineas:: [Mochila] -> String
lineas [] = ""
lineas (mochila:mochilas) = show mochila ++ "\n" ++ lineas mochilas

{-

:l D:\HASKELL\practica.hs 

-}