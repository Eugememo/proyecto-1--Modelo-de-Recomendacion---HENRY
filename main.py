from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import pandas as pd
from unidecode import unidecode
import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import gc


app = FastAPI()

app.title = "Aplicación de consulta de películas - María Eugenia Memolli"

@app.get("/", tags =['Home'])
def Home():
    return "Bienvenidos a la APP de consultas de películas. Para continuar a la API de consulta agregar /docs al final de la url."

df_movies = pd.read_parquet('datasets/movies_limpio.parquet')
df_tags = pd.read_parquet('datasets/tags_ML.parquet')


meses = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12
}

#Función para ver la cantidad de películas que se estrenaron en un mes indicado. 
@app.get("/cantidad_filmaciones_mes/{mes}", tags=['Funciones'])
def cantidad_filmaciones_mes(mes:str):
    """
    Obtiene la cantidad de peliculas que estrenaron en el mes ingresaro. <br>
    :param df: Dataframe con las películas disponibles en la plataforma con fecha de estreno<br>
    :param mes: mes para el cual se quiere obtener la cantidad de películas estrenadas. <br>
    :return: respuesta con la cantidad de películas estrenadas ese mes. 
    """

    mes = mes.lower()  


    df_movies['release_date']= pd.to_datetime(df_movies['release_date'],format=('%Y-%m-%d'))

    if mes not in meses:
        raise ValueError("Mes ingresado no es válido. Por favor, ingrese un mes en español.")
    
    mes_numero = meses[mes]
    
    df_sin_duplicados = df_movies.drop_duplicates(subset='title')
    
    peliculas_en_mes = df_sin_duplicados[df_sin_duplicados['release_date'].dt.month == mes_numero]
    
    cantidad_peliculas = len(peliculas_en_mes)
    
    resultado = f"La cantidad de películas estrenadas en {mes} es: {cantidad_peliculas}"

    return resultado



dias_map = {
    "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
    "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
    "once": 11, "doce": 12, "trece": 13, "catorce": 14, "quince": 15,
    "dieciséis": 16, "diecisiete": 17, "dieciocho": 18, "diecinueve": 19, "veinte": 20,
    "veintiuno": 21, "veintidos": 22, "veintitres": 23, "veinticuatro": 24, "veinticinco": 25,
    "veintiséis": 26, "veintisiete": 27, "veintiocho": 28, "veintinueve": 29, "treinta": 30, "treinta y uno": 31
}

@app.get("/cantidad_filmaciones_dia/{dia}",  tags=['Funciones'])
def cantidad_filmaciones_dia(dia:str):
    """
    Obtiene la cantidad de peliculas que estrenaron en el día ingresaro. 
    :param df: Dataframe con las películas disponibles en la plataforma con fecha de estreno
    :param mes: mes para el cual se quiere obtener la cantidad de películas estrenadas. 
    :return: respuesta con la cantidad de películas estrenadas ese mes. 
    """
    
    df_movies['release_date'] = pd.to_datetime(df_movies['release_date'], errors='coerce')
    
    df_movies['day'] = df_movies['release_date'].dt.day
    
    dia_numero = dias_map.get(dia.lower())
    if dia_numero is None:
        return "Día no válido."
    
    df_filtered = df_movies[df_movies['day'] == dia_numero]
    
    df_unique_titles = df_filtered.drop_duplicates(subset=['title'])
    
    cantidad_peliculas = len(df_unique_titles)

    resultado = f"La cantidad de películas estrenadas en {dia} es: {cantidad_peliculas}"
    
    return resultado


@app.get("/score_titulo/{titulo_de_la_filmacion}",  tags=['Funciones'])
def score_titulo(titulo_de_la_filmacion: str):
    """
    La función score_titulo toma el título de una película como entrada y devuelve el título, año de lanzamiento y puntaje de popularidad. 
    Primero, normaliza el título ingresado y los títulos en el DataFrame df_movies. Luego, filtra el DataFrame para encontrar coincidencias. 
    Si no se encuentra ninguna película, devuelve un mensaje de error. Si se encuentra una, devuelve la información de la primera coincidencia.
    """

    titulo_normalizado = unidecode(titulo_de_la_filmacion).lower()
    df_movies['title_normalized'] = df_movies['title'].apply(lambda x: unidecode(x).lower())
    peliculas_filtradas = df_movies[df_movies['title_normalized'].str.contains(titulo_normalizado, case=False, na=False)]
    
    if peliculas_filtradas.empty:
        return {"mensaje": f'No se encontró ninguna película con el título "{titulo_de_la_filmacion}"'}
    
    pelicula = peliculas_filtradas.iloc[0]
    titulo = pelicula['title']
    release_year = pelicula['release_year']
    popularidad_score = pelicula['popularity']
    
    resultado = f'La película "{titulo}" fue estrenada en el año {release_year}. Su score de popularidad es {popularidad_score:.2f}'
    
    return resultado



@app.get("/votos_titulos/{titulo_de_la_filmacion}",  tags=['Funciones'])
def votos_titulos(titulo_de_la_filmacion:str):

    """
    La función votos_titulos toma el título de una película y devuelve información sobre sus votos. P
    rimero, normaliza el título ingresado y los títulos en el DataFrame df_movies. 
    Luego, filtra para encontrar la película. Si no se encuentra, devuelve un mensaje de error. 
    Si se encuentra, obtiene el número de votos, el promedio de votos y el año de lanzamiento. 
    Si la película tiene menos de 2000 votos, devuelve un mensaje indicando que no cumple con el requisito mínimo de votos. 
    Si cumple, devuelve una cadena con el título, el año de lanzamiento, el total de votos y el promedio de votos.
    """

    titulo_normalizado = unidecode(titulo_de_la_filmacion).lower()  # Convertir y normalizar a minúsculas
    filtro = df_movies['title'].str.lower().apply(unidecode) == titulo_normalizado
    peliculas_filtradas = df_movies[filtro]

    if len(peliculas_filtradas) == 0:
            return f'No se encontró ninguna película con el título "{titulo_de_la_filmacion}".'
    else:
        votos = peliculas_filtradas['vote_count'].values[0]
        if votos < 2000:
            return f'La película "{titulo_de_la_filmacion}" no cumple con la condición de tener al menos 2000 votos.'
        else:
            titulo = peliculas_filtradas['title'].values[0]
            promedio_votos = peliculas_filtradas['vote_average'].values[0]
            año = peliculas_filtradas['release_year'].values[0]  
            return f"La película  {titulo} fue es trenada en el año {año}. La misma cuenta con un total de {votos} valoraciones, con un promedio de {promedio_votos}"
        


@app.get("/get_actor/{nombre_actor}",  tags=['Funciones']) 
def get_actor(nombre_actor: str):

    """
    La función get_actor recibe el nombre de un actor y devuelve información sobre su rendimiento en términos de retorno. 
    Primero, normaliza el nombre del actor y lo busca en el DataFrame df_credit_cast. 
    Si encuentra al actor, combina estos datos con el DataFrame df_movies para acceder a información adicional sobre las películas en las que ha participado. 
    Calcula el número total de películas únicas en las que ha actuado, suma el retorno total obtenido de estas películas y calcula el retorno promedio por película. 
    Finalmente, retorna una cadena formateada con el nombre del actor, el número de películas en las que ha participado, el retorno total acumulado y el retorno promedio por película.
    """
    df_credit_cast = pd.read_parquet('datasets/credit_cast_limpio.parquet')
    
    actor_normalizado = unidecode(nombre_actor).lower()  # Convertir y normalizar a minúsculas
    filtro_actor = df_credit_cast['cast_name'].str.lower().apply(unidecode) == actor_normalizado
    actor_movies = df_credit_cast[filtro_actor]
        
    if actor_movies.empty:
        return f"El actor {nombre_actor} no se encuentra en el dataset."
        
    actor_movies = actor_movies.merge(df_movies, on='id', how='left')
        
    cantidad_peliculas = actor_movies['id'].nunique()
    retorno_total = actor_movies['return'].sum()
    promedio_retorno = retorno_total / cantidad_peliculas if cantidad_peliculas > 0 else 0

    del df_credit_cast
    gc.collect()

    return f"El actor {nombre_actor} ha participado de {cantidad_peliculas} cantidad de filmaciones, el mismo ha conseguido un retorno de {retorno_total:.2f} con un promedio sw {promedio_retorno:.2f} por pelicula"



@app.get("/get_director/{nombre_director}",  tags=['Funciones'])
def get_director(nombre_director: str):

    """
    La función get_director acepta el nombre de un director como entrada y evalúa su éxito basado en el retorno financiero de las películas que ha dirigido. 
    Primero, obtiene los IDs de las películas asociadas al director desde el DataFrame df_credit_crew, luego filtra el DataFrame df_movies para obtener detalles 
    específicos de cada película dirigida por ese director. Calcula el retorno total sumando los retornos individuales de cada película y almacena los detalles de cada película en una lista. 
    Posteriormente, imprime los detalles de cada película desde esta lista y devuelve el retorno total acumulado de todas las películas dirigidas por el director. P
    ara mejorar, sería ideal manejar casos donde no se encuentre el nombre del director en el DataFrame df_credit_crew o si no hay películas asociadas con el director, 
    además de optimizar la impresión de detalles de películas evitando bucles anidados.
    """
    df_credit_crew = pd.read_parquet('datasets/credit_crew_limpio.parquet')

    director_pelicula = df_credit_crew[df_credit_crew['crew_name'] == nombre_director]['id']
    
    director_pelicula_detalles = df_movies[df_movies['id'].isin(director_pelicula)]
    
    exito = director_pelicula_detalles.drop_duplicates(subset='title')['return'].sum()
    
    movies_info = []
    for index, row in director_pelicula_detalles.drop_duplicates(subset='title').iterrows():
        Titulo = row['title']
        Año_lanzamiento = row['release_year']
        Valor_retorno = row['return']
        Ganancia = row['revenue']
        Presupuesto = row['budget']
        
        movie_details = {
            "Titulo": Titulo,
            "Año lanzamiento": Año_lanzamiento,
            "Retorno": Valor_retorno,
            "Ganancia": Ganancia,
            "Presupuesto": Presupuesto
        }
        
        movies_info.append(movie_details)

    for info in movies_info:
        print(f"Titulo: {info['Titulo']}")
        print(f"Año lanzamiento: {info['Año lanzamiento']}")
        print(f"Retorno: {info['Retorno']}")
        print(f"Ganancia: {info['Ganancia']}")
        print(f"Presupuesto: {info['Presupuesto']}")
        print()

    return {
        "exito_total": exito,
        "peliculas_detalle": movies_info
    }
    

@app.get("/recomendacion/{titulo}",  tags=['Modelo de Recomendación'])
def recomendacion(titulo:str):

    stop_words = 'english'
    cv = CountVectorizer(stop_words=stop_words)
    vector = cv.fit_transform(df_tags['etiquetas']).toarray()
    similitud_coseno = cosine_similarity(vector)
    
    try:
        indice = df_tags[df_tags['title'] == titulo].index[0]
        distancia = sorted(list(enumerate(similitud_coseno[indice])), reverse = True, key = lambda x: x[1])
        recomendadas = [df_tags.iloc[i[0]].title for i in distancia[1:6]]
        
        return {
                "message": f"Porque viste '{titulo}', tal vez te guste:",
                "peliculas_recomendadas": recomendadas
            }
    except IndexError:
        raise HTTPException(status_code=404, detail=f"No se encontró la película '{titulo}' en la base de datos.")
