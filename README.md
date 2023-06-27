# PROYECTO INDIVIDUAL Nº1: Machine Learning Operations

## Introducción
Al finalizar el bootcamp de Data Science de Henry, se asignan dos proyectos individuales y un proyecto grupal, con el objetivo de integrar los conocimientos adquiridos en la etapa de bootcamp.

Para el primer proyecto individual, Machine Learning Operations, se creó un modelo de ML que recomienda peliculas. En [este repositorio](https://github.com/HX-PRomero/PI_ML_OPS) se encuentran las consignas y en [este link](https://github.com/scioffi96/PI_ML_OPS/blob/main/movies_dataset.csv) se encuentra el dataset.

Al final de este archivo se encuentra el link a la API.

## Transformaciones y endpoints

En primera instancia, se realizaron las transformaciones a los datos que fueron sugeridas en las consignas. Estas recomendaciones abarcan:
- Desanidar campos del dataset que se encuentraban anidados en formato de diccionario o lista como valores en cada fila.
- Rellenar con 0 o eliminar valores nulos, según el campo.
- Crear o editar campos nuevos.
- Eliminar campos que no se utilizarán.

Luego, se crearon 6 funciones para los endpoints que se consumirán en la API:
- peliculas_mes: se ingresa el mes y la función retorna la cantidad de peliculas que se estrenaron ese mes.
- peliculas_dia: se ingresa el dia y la funcion retorna la cantidad de peliculas que se estrenaron ese dia.
- franquicia: se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio.
- peliculas_pais: se ingresas el pais, retornando la cantidad de peliculas producidas en el mismo.
- productoras: se ingresas la productora, retornando la ganancia total y la cantidad de peliculas que produjeron.
- retorno: se ingresas la pelicula, retornando la inversion, la ganancia, el retorno y el año en el que se lanzo.

*El notebook donde se realizaron las transformacioens y los endpoints se encuentra en [este link](https://github.com/scioffi96/PI_ML_OPS/blob/main/proyecto1_endpoints.ipynb).*

## Desarollo y deploy de la API

Para el desarrollo de la API se utilizó el framework recomendado: FastAPI.
Se probaron los endpoints en la API de forma local, en un entorno virtual, y una vez que todo funcionó correctamente se realizó el deployment.
Para el deployment se utilizó el servicio de web de rendezidado [Render](https://render.com/docs/free#free-web-services), por lo que primero se tuvo que armar el repositorio del proyecto en GitHub.

## EDA y Sistema de recomendación

Finalmente se realizó un análisis exploratorio de los datos (EDA) y el sistema de recomendación.
En el EDA se analizaron:
- los géneros de las películas, donde se eliminaron los géneros que sólo aparecían una vez; 
- la duración de las películas, donde se decidió no eliminar películas por su duración:
- los años de lanzamiento de las películas, que se analizaron con un gráfico de caja y bigote, las películas de años anteriores a 1930 salían como outliers. Si bien se entendió que no son valores erróneos, se decidió eliminarlos porque son una menor cantidad respecto a los años posteriores.

Luego, para el sistema de recomendación con HashingVectorizer se creó una nueva columna con palabras de los campos *descripción*, *géneros* y *compañía de producción*.
Además, se ordenaron los campos según su *puntuación*, y se limitó el dataset a los primeros 10000 valores, luego, a esos datos ordenados se los volvió a ordenar pero ahora según el *promedio de votos* y se limitó el dataset a los mejores 5000 puntuados.
De esta forma nos quedamos con las 5000 películas más populares y mejor puntuadas.

*El notebook donde se realizaró el EDA y el sistema de recomendación se encuentra en [este link](https://github.com/scioffi96/PI_ML_OPS/blob/main/proyecto1_recommend.ipynb).*

Finalmente, se editó el archivo [main.py](https://github.com/scioffi96/PI_ML_OPS/blob/main/main.py) que se utiliza para la API y se hizo un último deploy en Render con la función de recomendació ya activa.

Para usar la API haga [click aquí](https://santiagocioffi-pi1.onrender.com/docs).             
*(Si la API no ha sido utilizada en los últimos 15 minutos se deberá esperar a que se inicie)*.
