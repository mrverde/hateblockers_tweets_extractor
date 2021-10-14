# Hateblockers
## Proyecto: Medidor de odio

En este proyecto realizado en Python 3.8 para [Hateblockers](https://hateblockers.es/) se aborda la creación de un dashboard que busca medir el odio dentro de la red social twitter en función de los tweets de los usuarios.

## Extractor de tweets
La extracción de tweets se realiza con el script **hateblockers_tweets_extractor.py**. Para ejecutarlo es necesario en primer lugar crear un virtual environment con las dependencias del archivo **requirements.txt**.

Puede accederse a la documentación para crear un virtual environment desde [aquí](https://docs.python.org/3/library/venv.html).

Para ejecutar el script hay que invocar desde consola el comando:

```{bash}
python hateblockers_tweets_extractor.py
```

El script automáticamente buscará los términos existentes en el archivo **terms_to_search.txt**. Habrá de declararse un término por línea.

Es necesario configurar el archivo **.env** con las siguientes variables:

* API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET - [Credenciales de twitter](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api)
  
* EXPORT_LOG - Bool. Sirve para definir si queremos que se cree un log del proceso de extracción
  
* LOG_FILE - String. Nombre del archivo donde se volcarán los datos del log.
  
* OUTPUT_FILE - String. Nombre del archivo de salida donde se volcarán los tweets extraídos.

* EXCLUDE_RETWEETS - Bool. Sirve para excluir los retweets de la extracción.