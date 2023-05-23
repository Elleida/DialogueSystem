# DialogueSystem
El sistema de diálogo utiliza como sistema de reconocimiento automático del habla el sistema Whisper de Openai.
Tiene que existir un servicio con whisper. Este servicio se indica en la línea 58 del script demovirtualassistant.py

url = 'http://signal4.cps.unizar.es:8000/transcribe'  # Cambiar por la URL correcta

Este servicio está definido en el script app.py que supone que está instalado el sistema whisper.
Este servicio se levanta utilizando flask.

flask run --host 0.0.0.0 --port 8000

Para que el frontend del sistema de diálogo sea accesible desde cualquier máquina es necesario utilizar una conexión segura para que
permita utilizar el micrófono, lo que supone utilizar una versión de streamlit que permita conexiones en https y crear un certificado digital para dicha conexión

La demo se levanta utilizando streamlit

streamlit run demovirtualassistant.py --server.port 8505 --server.sslCertFile=./cert/server.crt --server.sslKeyFile=./cert/server.key

Si no se lanza por https solo se puede utilizar en el ordenador que lanza el servicio.

Si se quiere utilizar los modelos de lenguaje de Openai, hay que indicar la llave del API de Openai.
En la línea 54 se lee dicha llave

openai.api_key = os.getenv("OPENAI_API_KEY")

por lo que tiene que estar definida en la variable de entorno OPENAI_API_KEY.
El modelo vicuna-13b solo se puede utilizar si el frontend se levanta en la subred de la universidad de Zaragoza.

