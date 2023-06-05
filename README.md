# DialogueSystem
The dialogue system uses Openai's Whisper system as an automatic speech recognition system. There has to be a service with whisper. This service is indicated in line 58 of the demovirtualassistant.py script

url = 'http://signal4.cps.unizar.es:8000/transcribe' # Change to the correct URL

This service is defined in the app.py script which assumes system whisper is installed. This service is built using flask.

flask run --host 0.0.0.0 --port 8000

In order for the frontend of the dialog system to be accessible from any machine, it is necessary to use a secure connection to allow the use of the microphone, which means using a version of streamlit that allows https connections and creating a digital certificate for the connection.

The demo is launch using streamlit

streamlit run demovirtualassistant.py --server.port 8505 --server.sslCertFile=./cert/server.crt --server.sslKeyFile=./cert/server.key

If it is not launched via https, it can only be used on the computer that launches the service.

If you want to use the Openai language models, you must indicate the Openai API key. The key is read in line 54

openai.api_key = os.getenv("OPENAI_API_KEY")

so it has to be defined in the OPENAI_API_KEY environment variable. The vicuna-13b model can only be used if the frontend is set up in the subnet of the University of Zaragoza.

