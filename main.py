from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import pandas as pd
import random
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
#http://127.0.0.1:8000

app = FastAPI(title = "Proyecto_MLOps", description = "proyecto01")

#Creamos un directorio index con mensaje de bienvenida
@app.get("/", response_class=HTMLResponse)
async def index ():
    output = "¡Bienvenido a la interfaz de consultas, usted podrá realizar consulta sobre las peliculas, franquicias, productoras y su inversión! <br>"
    return output

#Carga de base de datos con las transoformaciones ya realizadas (Ver archivo ETL.ipynb)
df_movies_trans = pd.read_csv('datasets/movies_transform.csv')
df_movies = pd.read_csv('datasets/movies_dataset.csv')

df_movies_trans['release_date'] = pd.to_datetime(df_movies_trans['release_date'])

df_movies_trans['moth'] = df_movies_trans['release_date'].dt.strftime('%B')
df_movies_trans['day'] = df_movies_trans['release_date'].dt.strftime('%A')

meses = {
    'January': 'Enero',
    'February': 'Febrero',
    'March': 'Marzo',
    'April': 'Abril',
    'May': 'Mayo',
    'June': 'Junio',
    'July': 'Julio',
    'August': 'Agosto',
    'September': 'Septiembre',
    'October': 'Octubre',
    'November': 'Noviembre',
    'December': 'Diciembre'
}
def convert_mes(mes_ingles):
    mes_espanol = meses.get(mes_ingles)
    return mes_espanol

df_movies_trans['moth'] = df_movies_trans['moth'].apply(convert_mes)

dias = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miércoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}

# Función para convertir el nombre del día de inglés a español
def convert_dia(dia_ingles):
    dia_espanol = dias.get(dia_ingles)
    return dia_espanol

df_movies_trans['day'] = df_movies_trans['day'].apply(convert_dia)

#Se desarrollan las consutlas que fueron solicitadas por el cliente:
# CONSULTA 1
@app.get('/peliculas_mes/{mes}')
def peliculas_mes(mes:str):
    mes = mes.capitalize()
    cantidad = df_movies_trans.loc[df_movies_trans['moth'] == mes, 'title'].count()

    return {'mes':mes, 'cantidad':int (f'{cantidad}')}

# CONSULTA 2
@app.get('/peliculas_dia/{dia}')
async def peliculas_dia(dia:str):
    dia = dia.capitalize()
    cantidad = df_movies_trans.loc[df_movies_trans['day'] == dia, 'title'].count()

    return {'dia':dia, 'cantidad':int (f'{cantidad}')}

# CONSULTA 3
@app.get('/franquicia/{franquicia}')
def franquicia(franquicia: str):
    '''Se ingresa la franquicia, retornando la cantidad de películas, ganancia total y promedio'''
    df_cantidad = df_movies_trans[df_movies_trans['belongs_to_collection'] == franquicia]
    cantidad = len(df_cantidad)
    ganancia_total = df_cantidad['revenue'].sum()
    ganancia_promedio = df_cantidad['revenue'].mean() if cantidad > 0 else 0

    return {'franquicia': franquicia, 'cantidad': cantidad, 'ganancia_total': ganancia_total, 'ganancia_promedio': ganancia_promedio}

# CONSULTA 4
@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais: str):
    '''Ingresas el país, retornando la cantidad de películas producidas en el mismo'''
    df_movies_trans['production_countries']=df_movies_trans['production_countries'].fillna('')
    cantidad = 0
    
    for countries in df_movies_trans['production_countries']:      
        if pais in countries:
                cantidad += 1
    return {'pais':pais, 'cantidad':cantidad}

# CONSULTA 5
@app.get('/productoras/{productora}')
def productoras(productora: str):
    '''Ingresa la productora y retorna la ganancia total y la cantidad de películas que produjeron'''

    df_movies_trans['production_companies'] = df_movies_trans['production_companies'].fillna('')
    productora_df = df_movies_trans[df_movies_trans['production_companies'].apply(lambda x: productora in x)]

    ganancia_total = productora_df['revenue'].sum()
    cantidad = productora_df['revenue'].count()

    return {'productora': productora, 'ganancia_total': ganancia_total, 'cantidad': int (f'{cantidad}')}

# CONSULTA 6
@app.get('/retorno/{pelicula}')
def retorno(pelicula:str):
    '''Ingresas la pelicula, retornando la inversion, la ganancia, el retorno y el año en el que se lanzo'''
    df_retorno=df_movies_trans[df_movies_trans['title'] == pelicula]
    inversion= df_retorno['budget'].sum()
    ganancia= df_retorno['revenue'].sum()
    retorn= df_retorno['return'].sum()
    anio = df_retorno['release_year'].astype(int).item()

  
    return {'pelicula':pelicula, 'inversion':inversion, 'ganacia':ganancia,'retorno':retorn, 'anio':anio}

# ML

# Obtén la cantidad total de filas del DataFrame original
total_filas = len(df_movies)

# Calcula la cantidad de filas para el nuevo DataFrame
filas_nuevo_df = int(total_filas / 5)

# Genera una lista de índices aleatorios sin repetición
indices_aleatorios = random.sample(range(total_filas), filas_nuevo_df)

# Extrae las filas correspondientes a los índices aleatorios en un nuevo DataFrame
df_modelo = df_movies.iloc[indices_aleatorios]

# Reinicia los índices del nuevo DataFrame
df_modelo = df_modelo.reset_index(drop=True)

df_modelo['tagline'] = df_modelo['tagline'].fillna('')
df_modelo['description'] = df_modelo['overview'] + df_modelo['tagline']
df_modelo['description'] = df_modelo['description'].fillna('')

tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(df_modelo['description'])

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

df_modelo = df_modelo.reset_index()
titles = df_modelo['title']
indices = pd.Series(df_modelo.index, index=df_modelo['title'])



@app.get('/recomendacion/{titulo}')
def recommendacion(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    cantidad=titles.iloc[movie_indices].head()
    return  {'lista recomendada': cantidad}