# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

<p align="center">
<img src="https://user-images.githubusercontent.com/67664604/217914153-1eb00e25-ac08-4dfa-aaf8-53c09038f082.png"  height=300>
</p>

## **Desarrollado por Jesús Arteaga Vela**
<hr>

### **Resumen:**
Realizar un sistema de recomendaciones en una start-up que provee servicios de agregación de plataformas de streaming.

Para el cual tienes datos con 0 tratamiento ([movies_dataset.csv](https://github.com/jarteaga97/PI_ML_OPS_LAB01/tree/main/datasets)), datos anidados, sin transformar, etc.

Por lo que es necesario realizar para este proyecto, ETL, API, EDA, deployment y un sistema de recomendaciones.
<hr>

### </h1>**Rol del desarrollador:**
**`Data Scientis`**
<hr>

### **Proceso:**

#### Proceso de "ETL" (Extract, transform, load) en VisualStudioCode - Python:

+ Desanidar los campos que poseen diccionarios o lista de los mismos.
+ Rellenar con el número **`0`** los valores nulos de los campos **`revenue`**, **`budget`**.
+ De haber fechas, deberán tener el formato.**`AAAA-mm-dd`**
+ Crear la columna **`release_year`** donde extraerán el año de la fecha de estreno.
+ Crear la columna llamada **`return`**, dividiendo los campos.**`revenue / budget`**, cuando no hay datos disponibles para calcularlo, deberá tomar el valor **`0`**.
+ Eliminar las columnas que no serán utilizadas, **`video`**,**`imdb_id`**,**`adult`**,**`original_title`**,**`vote_count`**,**`poster_path`** y **`homepage`**.
+ Exportar CSV final con todas las transformaciones.

#### *Nota: La extracción de datos así como las respectivas transformaciones pueden verse desarrolladas en el archivo ([ETL.ipynb](https://github.com/jarteaga97/PI_ML_OPS_LAB01/blob/main/ETL.ipynb))*
<hr>

#### Desarrollo de las consultas solicitadas (API):

+ Ingresar el mes y la funcion retorna la cantidad de peliculas que se estrenaron ese mes historicamente.
+ Ingresar el dia y la funcion retorna la cantidad de peliculas que se estrebaron ese dia historicamente.
+ Ingresar la franquicia, retornando la cantidad de peliculas, ganancia total y promedio.
+ Ingresar el pais, retornando la cantidad de peliculas producidas en el mismo.
+ Ingresar la productora, retornando la ganancia toal y la cantidad de peliculas que produjeron.
+ Ingresar la pelicula, retornando la inversion, la ganancia, el retorno y el año en el que se lanzo.

**ML**
+ Ingresas un nombre de pelicula y te recomienda las similares en una lista.




