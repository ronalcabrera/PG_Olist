<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# <h1 align=center> **PROYECTO FINAL - Grupo N°3** </h1>

# <h1 align=center>**`E-commerce Olist`**</h1>

<p align="center">
<img src="https://epiprodux.com/blog/wp-content/uploads/2022/02/Ecommerce-managers-Role.jpg"  height=500>
</p>



## :small_blue_diamond: **Introducción**

En este proyecto, se desarrolla un MVP (minimum viable product) para Olist, una compañía brasileña prestadora de servicios e-commerce para PYMES que funciona como un marketplace. El objetivo principal es ayudar a las pequeñas empresas a conectarse con mercados más grandes y mejorar la experiencia del usuario.
Para lograrlo, Olist nos proporciona sus datos de 2016 a 2018, y se espera que el MVP entregado incluya análisis y soluciones innovadoras basadas en estos datos.



## :small_blue_diamond: **Propuesta de trabajo**

A continuación se detallan los diferentes etapas para la ejecución del proyecto:

+ *Data Engineering:* Se inició con el EDA, en el cual se buscó  conocer y comprender a los datos sin procesar. Además se investigó respecto de la empresa Olist, para poder definir cuál sería el rumbo que tomaría el proyecto y el producto que se presentaría. Así fue como se decidió que para la etapa correspondiente a la ingeniería del dato se ejecutará una aplicación que se desarrolló enteramente Python y con librerías como pandas, numpy, FastAPI y pymysql, que posteriormente sería automatizada por los servicios que proporciona GCP(Cloud SQL, Cloud Run, Google Scheduler).
La aplicación consiste en la ejecución de las siguientes tareas: 
El proceso de limpieza y transformación de los mismos (ETL) para su posterior análisis. Algunas de las acciones fueron la eliminación de duplicados, cambiar los 
NaN por ‘Sin Dato’  cuando se trataba de datos str, y la transformación de los datos en un formato adecuado para su análisis.
Luego de que los datos  fueron limpiados y transformados, se creó una base de 
datos para almacenarlos y cargarlos.

+ *Data Analytics:* Con los datos cargados en la base de datos, se utilizó Power BI para analizarlo y crear visualizaciones. Esto permitió una comprensión más profunda de los datos y su relación con otros factores. De esta etapa se obtuvo un dashboard y un reporte con un análisis exhaustivo del mismo.

+ *Machine Learning:* Finalmente, se utilizaron técnicas de aprendizaje automático para crear un modelo a partir de los datos. El modelo utilizado fue ForecasterAutoregressor, que permitió predecir la cantidad de ventas en el último trimestre del año 2018.



## :small_blue_diamond: **Video demostrativo**

Link:

+ https 



## :small_blue_diamond: **Disclaimer**

+ Este proyecto pretende simular un entorno laboral, en el cual se trabajan diversas temáticas ajustadas a la realidad. No reflejan necesariamente la filosofía y valores de la organización de Olist. Es por ello que la información expuesta y los resultados obtenidos no deben ser tomados en cuenta para la toma real de decisiones.
