<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# <h1 align=center> **PROYECTO FINAL - Grupo N°3** </h1>

# <h1 align=center>**`E-commerce Olist`**</h1>

<p align="center">
<img src="https://play-lh.googleusercontent.com/eqLTXWdyygKUf85JsCXmcLSr1GnoYNLJfFVCmY-N8xGFr2T3PWwNcFdJ2Sx7MwcO6ac"  height=300>
</p>

En este proyecto, se desarrolla un MVP (minimum viable product) para Olist, una compañía brasileña prestadora de servicios e-commerce para PYMES que funciona como un marketplace. El objetivo principal es ayudar a las pequeñas empresas a conectarse con mercados más grandes y mejorar la experiencia del usuario.
Para lograrlo, Olist nos proporciona sus datos de 2016 a 2018, y se espera que el MVP entregado incluya análisis y soluciones innovadoras basadas en estos datos. ***Data Scientist***.


## :small_blue_diamond: **Introducción**

La idea de este proyecto es lograr internalizar los conocimientos requeridos para la elaboración y ejecución de una API.

`Application Programming Interface` es una interfaz que permite que dos aplicaciones se comuniquen entre sí, independientemente de la infraestructura subyacente. Son herramientas muy versátiles y fundamentales para la creación de, por ejemplo, pipelines, ya que permiten mover y brindar acceso simple a los datos que se quieran disponibilizar a través de los diferentes endpoints, o puntos de salida de la API.

Hoy en día contamos con **FastAPI**, un web framework moderno y de alto rendimiento para construir APIs con Python.

<p align=center>
<img src = 'https://i.ibb.co/9t3dD7D/blog-zenvia-imagens-3.png' height=250><p>

## :small_blue_diamond: **Propuesta de trabajo**

El proyecto consiste en realizar una ingesta de datos desde diversas fuentes, posteriormente aplicar las transformaciones que considere pertinentes, y luego disponibilizar los datos limpios para su consulta a través de una API. Esta API será construida en un entorno virtual dockerizado.

Los datos serán obtenidos en archivos de diferentes extensiones, como *csv* o *json*. Se realizará un EDA para cada dataset. Posteriormente, se relacionarán los datasets así pueden acceder a su información por medio de consultas a la API.

Las consultas a realizar son:

+ Máxima duración según tipo de film (película/serie), por plataforma y por año:
    El request debe ser: get_max_duration(año, plataforma, [min o season])

+ Cantidad de películas y series (separado) por plataforma
    El request debe ser: get_count_plataform(plataforma)  
  
+ Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo.
    El request debe ser: get_listedin('genero')  
    Como ejemplo de género pueden usar 'comedy', el cuál deberia devolverles un cunt de 2099 para la plataforma de amazon.

+ Actor que más se repite según plataforma y año.
  El request debe ser: get_actor(plataforma, año)

## :small_blue_diamond: **Pasos del proyecto**

A continuación se detallan los diferentes etapas para la ejecución del proyecto:

+ ***Data engineering:*** Se inició con el EDA, en el cual se buscó  conocer y comprender a los datos sin procesar. Además se investigó respecto de la empresa Olist, para poder definir cuál sería el rumbo que tomaría el proyecto y el producto que se presentaría. Así fue como se decidió que para la etapa correspondiente a la ingeniería del dato se ejecutará una aplicación que se desarrolló enteramente Python y con librerías como pandas, numpy, FastAPI y pymysql, que posteriormente sería automatizada por los servicios que proporciona GCP(Cloud SQL, Cloud Run, Google Scheduler).
La aplicación consiste en la ejecución de las siguientes tareas: 
El proceso de limpieza y transformación de los mismos (ETL) para su posterior análisis. Algunas de las acciones fueron la eliminación de duplicados, cambiar los 
NaN por ‘Sin Dato’  cuando se trataba de datos str, y la transformación de los datos en un formato adecuado para su análisis.
Luego de que los datos  fueron limpiados y transformados, se creó una base de 
datos para almacenarlos y cargarlos.

+ ***Data analyst:*** Con los datos cargados en la base de datos, se utilizó Power BI para analizarlo y crear visualizaciones. Esto permitió una comprensión más profunda de los datos y su relación con otros factores. De esta etapa se obtuvo un dashboard y un reporte con un análisis exhaustivo del mismo.

+ ***Machine Learning:*** Finalmente, se utilizaron técnicas de aprendizaje automático para crear un modelo a partir de los datos. El modelo utilizado fue ForecasterAutorregressor, que permitió predecir la cantidad de ventas en el último trimestre del año 2018.



<p align=center>
<img src = 'https://i.postimg.cc/2SwvnTcw/Sin-t-tulo.png' height = 400></p>


## :small_blue_diamond: **Herramientas utilizadas**

+ Python
<img src = 'https://datascientest.com/es/wp-content/uploads/sites/7/2020/10/power-bi-logo-1.jpg' height = 125>

+ MySQL
<img src = 'https://1000marcas.net/wp-content/uploads/2020/11/MySQL-logo-768x399.png' height = 125>

+ Docker
<img src = 'https://www.techprevue.com/wp-content/uploads/2021/04/docker-image.jpg' height = 125>

+ Google Cloud Platform
<img src = 'https://it.wisc.edu/wp-content/uploads/Google-Cloud-Platform-900x400-1.jpg' height = 125>

+ PowerBI
<img src = 'https://datascientest.com/es/wp-content/uploads/sites/7/2020/10/power-bi-logo-1.jpg' height = 125>

+ FastAPI
<img src = 'https://i.imgur.com/p0Nufjn.jpeg' height = 125>

## :small_blue_diamond: **Deployment en Google Cloud Platform**

Link:

+ https

## :small_blue_diamond: **Video demostrativo**

Link:

+ https

## :small_blue_diamond: **Aclaraciones**

+ La carpeta "notebooks" contiene los archivos ETL y Querys pero con la extension .ipynb utilizados al comienzo del desarrollo del proyecto debido a la comodidad del uso de Jupyter Notebooks.

+ El archivo EDA.py contiene todo el proceso de ingesta de datos y transformacion de los mismos.

+ El archivo Querys.py contiene las funciones necesarias para realizar las solicitudes requeridas.

+ El archivo main.py contiene las instrucciones necesarias para crear la API

+ El archivo Dockerfile contiene el código necesario para crear el entorno Docker
