from fastapi import FastAPI
import pandas as pd

app = FastAPI()

#Carga de dataset df_movies
df_movies = pd.read_csv("./Dataset/df_movies.csv")
df_movies['release_date'] = pd.to_datetime(df_movies['release_date'])

@app.get("/")
def read_root():
    """_Bienvenida_

    Returns:
        _type_: _Bienvenida al Proyecto_
    """
    return f'Bienvenido al Proyecto Integrador Numero 1'

# Ruta para la función cantidad_filmaciones_mes
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str)->str:
    """_Cantidad de filmaciones por mes_

    Args:
        mes (str): _Mes de Busqueda de Filmaciones_

    Raises:
        ValueError: _Descripcion del error_

    Returns:
        String: _Cantidad de películas que fueron estrenadas en el mes_
    """
    meses_en_espanol = {
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
    'diciembre': 12
    }

    # Convertir el mes a minusculas
    mes = mes.lower() 

    # Convertir el mes de español a número
    if mes not in meses_en_espanol:
        raise ValueError("Nombre de mes inválido")

    mes_numero = meses_en_espanol[mes]

    # Convertir la columna 'release_date' a tipo datetime
    #df_movies['release_date'] = pd.to_datetime(df_movies['release_date'])

    # Filtrar por el mes deseado
    peliculas_mes = df_movies[df_movies['release_date'].dt.month == mes_numero]

    # Contar la cantidad de películas
    cantidadmes = peliculas_mes.shape[0]
    
    return f'{cantidadmes} cantidad de películas fueron estrenadas en el mes de {mes.capitalize()}'

# Ruta para la función cantidad_filmaciones_dia    
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str)->str:
    """_Cantidad de filmaciones por dia_

    Args:
        dia (str): _Dia de Busqueda de Filmaciones_

    Raises:
        ValueError: _Descripcion del error_

    Returns:
        str: _Cantidad de películas que fueron estrenadas en el dia_
    """
    dias_en_espanol = {
    'lunes': 0,
    'martes': 1,
    'miercoles': 2,
    'jueves': 3,
    'viernes': 4,
    'sabado': 5,
    'domingo': 6
    }

    # Convertir el mes a minusculas
    dia = dia.lower()

    # Convertir el mes de español a número
    if dia not in dias_en_espanol:
        raise ValueError("Nombre de dia inválido")
    
    dia_numero = dias_en_espanol[dia]

    # Convertir la columna 'release_date' a tipo datetime
    #df_movies['release_date'] = pd.to_datetime(df_movies['release_date'])

    # Filtrar por el dia deseado
    peliculas_dia = df_movies[df_movies['release_date'].dt.weekday == dia_numero]

    # Contar la cantidad de películas
    cantidaddia = peliculas_dia.shape[0]
    
    return f'{cantidaddia} cantidad de películas fueron estrenadas en los días {dia.capitalize()}'

# Ruta para la función score_titulo
@app.get("/score_titulo/{titulo_de_la_filmacion}")
def score_titulo(titulo_de_la_filmacion: str)->str:
    """_Año de Estreno y Score_

    Args:
        titulo_de_la_filmacion (str): _Titulo de la Filmacion_

    Returns:
        str: _Año de estreno y score_
    """
    # Buscar la película por título en el dataframe
    pelicula = df_movies[df_movies['title'] == titulo_de_la_filmacion]
    
    # Verificar si se encontró la película
    if pelicula.empty: # El método empty devuelve True si el DataFrame está vacío.
        return "Película no encontrada"
    
    # Obtener los valores de título, año de estreno y score
    titulo = pelicula['title'].iloc[0] # iloc[0] sirve para acceder al primer registro
    año_estreno = str(pelicula['release_year'].iloc[0])
    score = str(pelicula['popularity'].iloc[0])
    
    return f"La película {titulo} fue estrenada en el año {año_estreno} con un score de {score}"

# Ruta para la función votos_titulo
@app.get("/votos_titulo/{titulo_de_la_pelicula}")
def votos_titulo(titulo_de_la_pelicula: str)->str:
    """_Año de estreno de la pelicula y votos_

    Args:
        titulo_de_la_pelicula (str): _Titulo de la Pelicula_

    Returns:
        str: _Año de Estreno y Votos_
    """
    # Buscar la película por título en el dataframe
    pelicula = df_movies[df_movies['title'] == titulo_de_la_pelicula]
    
    # Verificar si la película existe en el dataframe
    if pelicula.empty:
        return "La película no existe en el dataset."
    
    # Obtener los valores de título, cantidad de votos y valor promedio de las votaciones
    titulo = pelicula['title'].iloc[0]
    votos = pelicula['vote_count'].iloc[0]
    promedio_votos = pelicula['vote_average'].iloc[0]
    año_estreno = str(pelicula['release_year'].iloc[0])

    # Verificar si la película cumple con la condición de tener más de 2000 votos
    if votos < 2000:
        return f"La película {titulo} no cumple con la condición de tener más de 2000 votos. La misma cuenta con {int(votos)} votos"
    else:
        return f"La película {titulo} fue estrenada en el año {año_estreno}. La misma cuenta con un total de {int(votos)} valoraciones, con un promedio de {promedio_votos}"

# Ruta para la función get_actor
@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str)->str:
    """_Cantidad de Peliculas, Retorno y Retorno Promedio de Actor_

    Args:
        nombre_actor (str): _Nombre del Actor_

    Returns:
        str: _Cantidad de Peliculas Retorno y Retorno Promedio_
    """

    #Carga de dataset df_movies_cast
    df_movies_cast = pd.read_csv("./Dataset/df_movies_cast.csv")

    # Filtrar las filas que contienen al actor consultado
    peliculas_actor = df_movies_cast[df_movies_cast['cast_name'].apply(lambda x: nombre_actor in x)]
    
    # Verificar si el actor existe en el dataset
    if peliculas_actor.empty:
        return {"message": f"No se encontraron películas para el actor: {nombre_actor}"}
    
    # Obtener la cantidad de películas y el promedio de retorno del actor
    cantidad_peliculas = len(peliculas_actor)
    promedio_retorno = peliculas_actor['return'].mean()
    retorno = sum(peliculas_actor['return'])
    return f"El actor {nombre_actor} ha participado de {cantidad_peliculas} cantidad de filmaciones, el mismo ha conseguido un retorno de {retorno} con un promedio de {promedio_retorno} por filmación"
    
@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):
    """_Retorno Total, Peliculas (Nombre,Fecha de lanzamiento,Retorno,Ganancia y Costo)_

    Args:
        nombre_director (str): _Nombre del director_

    Returns:
        str: _Retorno Total, Peliculas (Nombre,Fecha de lanzamiento,Retorno,Ganancia y Costo)_
    """
    #Carga de dataset df_movies_crew
    df_movies_crew = pd.read_csv("./Dataset/df_movies_crew.csv")

    # Filtrar las filas que contienen al director consultado
    peliculas_director = df_movies_crew[df_movies_crew['crew_name'] == nombre_director]
    
    # Verificar si el director existe en el dataset
    if peliculas_director.empty:
        return {"message": f"No se encontraron películas para el director: {nombre_director}"}
    
    # Calcular la suma del retorno de inversión total
    retorno_total = peliculas_director['return'].sum()
    
    # Crear una lista para almacenar la información de cada película
    peliculas_info = []
    
    # Recorrer cada película del director
    for _, pelicula in peliculas_director.iterrows(): # iterrows() se utiliza para iterar sobre un DataFrame de Pandas fila por fila, cada iteración devuelve una tupla que contiene el índice de la fila y la serie de datos correspondiente a esa fila.
        titulo = pelicula['title']
        año_lanzamiento = pelicula['release_year']
        retorno_individual = pelicula['return']
        costo = pelicula['budget']
        ganancia = pelicula['revenue']
        
        # Crear un diccionario con la información de la película
        pelicula_info = {
            'titulo': titulo,
            'año_lanzamiento': año_lanzamiento,
            'retorno_pelicula': retorno_individual,
            'budget_pelicula': costo,
            'revenue_pelicula': ganancia
        }
        
        # Agregar el diccionario a la lista de películas
        peliculas_info.append(pelicula_info)
    
    # Crear el diccionario de respuesta con la suma del retorno total y la lista de películas
    respuesta = {
        'director': nombre_director,
        'retorno_total': retorno_total,
        'peliculas': peliculas_info
    }
    
    return respuesta
