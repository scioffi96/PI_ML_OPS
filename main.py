# http://127.0.0.1:8000

# Importamos las librerías
import pandas as pd 
import numpy as np
from fastapi import FastAPI
import sklearn
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.neighbors import NearestNeighbors

#Lectura de los df necesarios para las funciones
df=pd.read_csv('movies_endpoints.csv')
df_recom = pd.read_csv('movies_recommend.csv') 

# Indicamos título y descripción de la API
app = FastAPI(title='Proyecto individual n° 1')

@app.get('/')
async def read_root():
    return {'Hola! Para usar la API de peliculas dirigite a /docs '}

# FUNCIONES:

# Función de películas por mes
@app.get('/peliculas_mes/({mes})')
def peliculas_mes(mes:str):
    '''Ingresas el mes y la funcion retorna la cantidad de peliculas que se estrenaron ese mes.''' 
    mes = mes.lower()
    meses = {
    'enero': 1,
    'febrero': 2,
    'marzo': 3,
    'abril': 4,
    'mayo': 5,
    'junio': 6,
    'julio': 7,
    'agosto': 8,
    'septiembre': 9,
    'octubre': 10,
    'noviembre': 11,
    'diciembre': 12}
    mes_numero = meses[mes]
    # Convertir la columna "fecha" a un objeto de tipo fecha
    df['release_date'] = pd.to_datetime(df['release_date'])
    # Tratamos la excepciòn
    try:
        month_filtered = df[df['release_date'].dt.month == mes_numero]
    except (ValueError, KeyError, TypeError):
        return None
    # Filtramos valores duplicados del dataframe y calculamos
    month_unique = month_filtered.drop_duplicates(subset='id')
    respuesta = month_unique.shape[0]
    return {'mes':mes, 'cantidad':respuesta}

# Función de películas por día
@app.get('/peliculas_dia/({dia})')
def peliculas_dia(dia:str):
    '''Ingresas el dia de la semana y la funcion retorna la cantidad de peliculas que se estrenaron ese dia (por ejemplo, lunes) historicamente.'''
    # Creamos diccionario para normalizar
    days = {
    'lunes': 'Monday',
    'martes': 'Tuesday',
    'miercoles': 'Wednesday',
    'jueves': 'Thursday',
    'viernes': 'Friday',
    'sabado': 'Saturday',
    'domingo': 'Sunday'}
    day = days[dia.lower()]
    # Filtramos los duplicados del dataframe y calculamos
    lista_peliculas_day = df[df['release_date'].dt.day_name() == day].drop_duplicates(subset='id')
    respuesta = lista_peliculas_day.shape[0]
    return {'dia': dia, 'cantidad': respuesta}

# Función de métricas por franquicia
@app.get('/franquicia/({franquicia})')
def franquicia(franquicia:str):
    '''Ingresas la franquicia y la funcion retorna: la cantidad de peliculas, ganancia total y promedio promedio por pelicula.''' 
    # Filtramos el dataframe
    lista_peliculas_franquicia = df[(df['collection'] == franquicia)].drop_duplicates(subset='id')
    # Calculamos
    cantidad_peliculas_franq = (lista_peliculas_franquicia).shape[0]
    revenue_franq = lista_peliculas_franquicia['revenue'].sum()
    promedio_franq = revenue_franq/cantidad_peliculas_franq
    return {'franquicia':franquicia, 'cantidad':cantidad_peliculas_franq, 'ganancia_total':revenue_franq, 'ganancia_promedio':promedio_franq}

# Función películas por país
@app.get('/peliculas_pais/({pais})')
def peliculas_pais(pais:str):
    '''Ingresas el pais y la funcion retorna la cantidad de peliculas producidas en el mismo.'''
    # Filtramos el dataframe y contamos filas
    movies_filtered = df[(df['country'] == pais)]
    movies_unique = movies_filtered.drop_duplicates(subset='id')    
    respuesta = movies_unique.shape[0]
    return {'pais':pais, 'cantidad':respuesta}

# Función métricas por productora
@app.get('/productoras/({productora})')
def productoras(productora:str):
    '''Ingresas la productora y la funcion retorna la ganancia total y la cantidad de peliculas que produjeron.''' 
    if productora not in df['company'].values:
        return 'La productora no se encuentra en el conjunto de la base de datos.'
    else:
        # Filtramos el dataframe
        lista_peliculas_productoras = df[(df['company'] == productora)].drop_duplicates(subset='id')
        # Calculamos
        cantidad_peliculas_prod = (lista_peliculas_productoras).shape[0]
        revenue_prod = lista_peliculas_productoras['revenue'].sum()
        return {'productora':productora, 'ganancia_total':revenue_prod, 'cantidad':cantidad_peliculas_prod}

# Función métricas por película
@app.get('/retorno/({pelicula})')
def retorno(pelicula):
    '''Ingresas la pelicula y la funcion retorna la inversion, la ganancia, el retorno y el año en el que se lanzo'''
    if pelicula not in df['title'].values:
        return 'La pelicula no se encuentra en el conjunto de la base de datos.'
    else:
        
        info_pelicula = df[(df['title'] == pelicula)].drop_duplicates(subset='title')
        pelicula_nombre = info_pelicula['title'].iloc[0]
        inversion_pelicula = str(info_pelicula['budget'].iloc[0])
        ganancia_pelicula = str(info_pelicula['revenue'].iloc[0])
        retorno_pelicula = str(info_pelicula['return'].iloc[0])
        year_pelicula = str(info_pelicula['release_year'].iloc[0])
        return {'pelicula':pelicula_nombre, 'inversion':inversion_pelicula, 'ganacia':ganancia_pelicula,'retorno':retorno_pelicula, 'anio':year_pelicula}

# Función de recomendación
cv = CountVectorizer(stop_words='english', max_features=5000)
count_matrix = cv.fit_transform(df_recom['combined_features'])
nn = NearestNeighbors(metric='cosine', algorithm='brute')
nn.fit(count_matrix)
indices = pd.Series(df_recom.index, index=df_recom['title']).drop_duplicates()

@app.get("/recomendacion/{titulo}")
def recomendacion(title):
    '''Ingresas un nombre de pelicula y la funcion te recomienda cinco peliculas similares.''' 
    # Verifica si el titulo ingresado se encuentra en el df
    if title not in df_recom['title'].values:
        return 'La pelicula no se encuentra en el conjunto de la base de datos.'
    else:
        # Si el título esta en el df, encuentra su indice
        index = indices[title]
        # Obtiene las puntuaciones de similitud de las 5 peliculas más cercanas
        distances, indices_knn = nn.kneighbors(count_matrix[index], n_neighbors=6)  # indica que queremos encontrar las 6 peliculas más similares, incluyendo la pelicula dada
        # Obtenemos los indices de las peliculas
        movie_indices = indices_knn[0][1:]  
        # Devolvemos las 5 peliculas mas similares
        return {'lista recomendada': df_recom['title'].iloc[movie_indices].tolist()}