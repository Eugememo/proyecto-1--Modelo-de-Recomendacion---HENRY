
<h1> Modelo de Recomencación de Películas 🎬 </h1>

## Introducción:
El proyecto trata del análisis y recomendación para películas, diseñada para ayudar a los usuarios a explorar y descubrir películas 
basadas en sus preferencias personales. Utiliza técnicas avanzadas de análisis de datos para proporcionar recomendaciones precisas y personalizadas, 
basadas en el género, el director y otros criterios relevante.

Tabla de Contenidos: 
1. [Introducción](#introducción)
2. [Conjunto de datos](#conjunto-de-datos)
3. [Etapas del Proyecto](#etapas-del-proyecto)
4. Creación de funciones

## Conjunto de datos
Para el proyecto HENRY nos proporcionó 2 archivos CSV para desarollar el análisis y el Modelo de recomendación posterior. 
* `movies_dataset.csv` es un conjunto de datos que contiene información detallada sobre las películas disponibles en la plataforma. Incluye datos sobre los votos proporcionados por los usuarios, ofreciendo una visión de la recepción y popularidad de cada película. Además, proporciona detalles sobre el presupuesto invertido en la producción de cada filme y las ganancias generadas, permitiendo un análisis completo del rendimiento económico de las películas en la plataforma.
* `credits.csv` es un conjunto de datos que proporciona información detallada sobre el equipo de producción involucrado en cada película, incluyendo roles como directores, guionistas y productores. Además, incluye datos sobre los actores que participaron en cada filme, ofreciendo un panorama completo del equipo creativo y técnico detrás de las producciones cinematográficas.

## Etapas del Proyecto
### 1. Ingeniería de Datos (ETL)
En esta etapa inicial de la ingeniería de datos, comenzamos por comprender los archivos proporcionados, identificando los tipos de datos que contienen para obtener una visión clara del dataset completo. Al revisar y analizar el repositorio de películas, nos encontramos con que los DataFrames contienen datos anidados, lo cual requiere un enfoque específico para su comprensión y manipulación adecuada.

### 2. Creación de funciones
Se empleó FastAPI para desarrollar una aplicación que incluye las funciones solicitadas por el cliente, las cuales devuelven la información requerida en cada caso. Las funciones se encuentran documentadas en el archivo dentro de la carpeta Notebook.
+ def **cantidad_filmaciones_mes( *`Mes`* )**: Se ingresa un mes en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en el mes consultado en la totalidad del dataset.
+  def **cantidad_filmaciones_dia( *`Dia`* )**: Se ingresa un día en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en día consultado en la totalidad del dataset.
+  def **score_titulo( *`titulo_de_la_filmación`* )**: Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.
+  def **votos_titulo( *`titulo_de_la_filmación`* )**: Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. La misma variable deberá de contar con al menos 2000 valoraciones, caso contrario, debemos contar con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.
+  def **get_actor( *`nombre_actor`* )**: Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, la cantidad de películas que en las que ha participado y el promedio de retorno. 
+ def **get_director( *`nombre_director`* )**: Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.

### 3. Análisis Exploratorio de Datos (EDA)
Se realizó un análisis comprensivo de los datos para entender la estructura y las características del conjunto con el que estamos trabajando. Esto implica examinar la distribución de variables, detectar valores atípicos y explorar las relaciones entre las variables, entre otros aspectos clave. Este análisis es fundamental para identificar patrones o tendencias en los datos, lo que permite formular hipótesis sólidas y diseñar modelos más precisos.

### 4. Modelo de recomendación
En el archivo "Modelo de recomendación" se encuentra la guía detallada de cómo se diseñó y desarrolló el modelo de recomendación. Este documento incluye una descripción de los pasos seguidos, desde la recopilación y preparación de datos hasta la implementación del algoritmo de recomendación. Además, se documentan los criterios y métricas utilizados para evaluar la efectividad del modelo, proporcionando una visión integral del proceso de creación del sistema de recomendación.

Link a la aplicación: https://proyecto-1-modelo-de-recomendacion-henry-tg0c.onrender.com

