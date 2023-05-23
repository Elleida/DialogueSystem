
import openai
from gtts import gTTS
from io import BytesIO
import os
import requests
import streamlit as st
import base64
from audio_recorder_streamlit import audio_recorder
from PIL import Image
import time
from langdetect import detect
import pandas as pd
import json

def autoplay_audio(audio_bytes):
    audio_base64 = base64.b64encode(audio_bytes).decode()
    audio_tag = f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}"></audio>'
    st.markdown(audio_tag, unsafe_allow_html=True)

def enwelcomemessage():
    language = 'en'
    mensaje_inicial = "Hello, I'm your virtual assisstant powered by Openai. How can I help you?"
    tts = gTTS(text=mensaje_inicial, lang=language,slow=False)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    autoplay_audio(mp3_fp.getvalue())

def engoodbyemessage():
    language = 'en'
    mensaje_inicial = "See you soon! It has been a pleasure helping you."
    tts = gTTS(text=mensaje_inicial, lang=language,slow=False)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    autoplay_audio(mp3_fp.getvalue())

def welcomemessage():
    language = 'es'
    mensaje_inicial = "Hola, soy tu asistente virtual. ¿En qué puedo ayudarte?"
    tts = gTTS(text=mensaje_inicial, lang=language,slow=False)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    autoplay_audio(mp3_fp.getvalue())

def goodbyemessage():
    language = 'es'
    mensaje_inicial = "¡Hasta pronto! Ha sido un placer ayudarte."
    tts = gTTS(text=mensaje_inicial, lang=language,slow=False)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    autoplay_audio(mp3_fp.getvalue())

# Set up OpenAI API credentials
openai.api_key = os.getenv("OPENAI_API_KEY")
fid=open('chatbot.txt','a')
lenguas={'español':'es','inglés':'en'}
df=pd.DataFrame(lenguas,columns=['Lenguaje','Idioma'])
url = 'http://signal4.cps.unizar.es:8000/transcribe'  # Cambiar por la URL correcta
archivo_audio = 'audio.wav'  # Cambiar por la ruta correcta del archivo de audio
idioma='**Selecciona el idioma/Choose the language**'
parametros = {
   'language': 'spanish',
    'model_size': 'medium'
}
# Establecer los headers de la llamada POST
headers = {
    'Content-Type': 'audio/mp3'  # Cambiar por el tipo de archivo correcto
}
current_dir= os.getcwd()
with st.sidebar:
    lang=st.radio(idioma, ('español', 'inglés'))   
    llm=st.radio('Selecciona el modelo de lenguage',('gpt-3.5-turbo','vicuna-13b'))
    streamchat=st.checkbox('Respuesta en streaming')
    if llm=='vicuna-13b':
        openai.api_key = "EMPTY" # Not support yet
        openai.api_base = "http://voz12.intra.unizar.es:8000/v1"
        model="vicuna-13b"
    if llm=='gpt-3.5-turbo':
        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_base = "https://api.openai.com/v1"
        model="gpt-3.5-turbo"
    language=lenguas[lang]
    if language=='es':
        st.title('¿Cómo funciona?')
        st.markdown('''- Pulsa el botón **Iniciar conversación** para comenzar una conversación con el asistente.
- Pulsa el botón **Pulsa para hablar** para iniciar la grabación de tu voz (el icono cambiará a color rojo).
- Vuelve a pulsar el botón **Pulsa para hablar** para detener la grabación.
- Pulsa el botón **Terminar conversación** cuando quieras finalizar la conversación.
''')
        titulo='Asistente virtual con un LLM'
        pulsahablar='Pulsa para hablar'
        iniciarconversacion='Iniciar conversación'
        terminarconversacion='Terminar conversación'
        despedida='**M:** Hasta pronto'
        parametros['language']='spanish'
        notranscripcion="No se ha podido transcribir el audio, vuelve a intentarlo"
    if language=='en':
        st.title('How does it work?')
        st.markdown('''- Press the **Start conversation** button to start a conversation with the assistant.
- Press the **Press to talk** button to start recording your voice (the icon will change to red).
- Press the **Press to talk** button again to stop recording.
- Press the **End conversation** button when you want to end the conversation.
''')
        titulo='Virtual assistant with a LLM'
        pulsahablar='Press to talk'
        iniciarconversacion='Start conversation'
        terminarconversacion='End conversation'
        despedida='**M:** See you soon'
        parametros['language']='english'
        notranscripcion="The audio could not be transcribed, please try again"
           
st.title(titulo)
col1, col2 = st.columns(2)
if 'audio_bytes' not in st.session_state:
    st.session_state.audio_bytes = None

mensajerole=[{"role":"system","content":"Eres un asistente útil y amable."}]
mensaje=mensajerole
if 'mensaje' not in st.session_state:
    st.session_state["mensaje"]=mensaje
else:
    mensaje=st.session_state["mensaje"]
sample_rate = 16000
tts_language=language
total_tokens = 0
image = Image.open('susurro.png')
with col1:
    if st.button(iniciarconversacion):
        if language=='es':
            welcomemessage()
        if language=='en':
            enwelcomemessage()
        st.session_state["mensaje"]=mensajerole
# Inicializar el stream de audio
    audio_bytes = audio_recorder(text=pulsahablar,energy_threshold=(1,1),pause_threshold=2.0, sample_rate=sample_rate, key="audio_recorder")
    if st.button(terminarconversacion):
        placeholder = st.empty()
        placeholder.markdown(despedida)
        if language=='es':
            goodbyemessage()
        if language=='en':
            engoodbyemessage()
        st.session_state["mensaje"]=mensajerole
        time.sleep(3)
        placeholder.empty()
with col2:
    st.image(image, width=200)
# Save audio to WAV file
st.markdown("""---""")
if audio_bytes and audio_bytes != st.session_state.audio_bytes:
    st.session_state.audio_bytes = audio_bytes
    with open('audio.wav', mode='bw') as f:
        f.write(audio_bytes)
    files = {'audio_data': open(archivo_audio, 'rb')}
# Realizar la llamada POST con requests
#headers = {'Content-Type': 'application/json'}

#    st.audio(audio_bytes, format="audio/wav")
    placeholder = st.empty()
    placeholder.markdown('**:red[Transcribiendo...]** :memo:')
    respuesta = requests.post(url, files=files, data=parametros)
    placeholder.empty()
# Transcribe audio using Whisper
    if  len(respuesta.text)>0:
        transcription = respuesta.text.strip()
        st.write('**U:**',transcription)
# Create a moderation request
        if llm=='gpt-3.5-turbo':
            response = openai.Moderation.create(
                input=transcription
            )
            output = response["results"][0]
            print(output)
        if llm=='gpt-3.5-turbo' and output["flagged"]:
            st.write("El mensaje contiene contenido inapropiado./The message contains inappropriate content.")
            st.write("Discurso de odio (Hate speech): ", output['categories']["hate"], "score = ", output["category_scores"]["hate"])
            st.write("Odio/Amenaza (Hate/Threatening): ", output['categories']["hate/threatening"], "score = ", output["category_scores"]["hate/threatening"])
            st.write("Autolesiones (Self Harm): ", output['categories']["self-harm"], "score = ", output["category_scores"]["self-harm"])
            st.write("Sexual: ", output['categories']["sexual"], "score = ", output["category_scores"]["sexual"])
            st.write("Sexuales/menores (Sexual/minors): ", output['categories']["sexual/minors"], "score = ", output["category_scores"]["sexual/minors"])
            st.write("Violence: ", output['categories']["violence"], "score = ", output["category_scores"]["violence"])
            st.write("violence/graphic: ", output['categories']["violence/graphic"], "score = ", output["category_scores"]["violence/graphic"])
            placeholder = st.empty()
            placeholder.markdown(despedida)
            goodbyemessage()
            st.session_state["mensaje"]=mensajerole
            time.sleep(3)
            placeholder.empty()
        else:
# Get the response from OpenAI API
            mensaje.append({"role":"user","content":transcription})
            print(model,mensaje)
            response=openai.ChatCompletion.create(
                model=model,
                messages=mensaje,
                max_tokens=200,
                stream=streamchat
                )

    # Get the response from OpenAI API
            if not streamchat:
                total_tokens = response['usage']['total_tokens']
                prompt_tokens = response['usage']['prompt_tokens']
                completion_tokens = response['usage']['completion_tokens']
                api_response = response['choices'][0]['message']['content']
                print(f'{prompt_tokens} prompt tokens and {completion_tokens} completion tokens used.')
        # Print the API response
                print(api_response)
                st.write('**M:**',api_response)
                st.write('Tokens:',total_tokens)
            else:
                api_response=''
                texto=st.empty()
                frase=''
                for chunk in response:
                    content= chunk["choices"][0]["delta"].get("content","")
                    api_response=api_response+content
                    frase=frase+content
                    if '. ' in frase:
                        index=frase.index('. ')
                        print(frase[:index+1])
                        frase=frase[index+1:]
                    if '.\n' in frase:
                        index=frase.index('.\n')
                        print(frase[:index+1])
                        frase=frase[index+1:]

                    texto.write('**M:** '+api_response)

        #        print(mensaje)
            mensaje.append({"role":"assistant","content":api_response})
            for item in mensaje:
                json.dump(item,fid)
            st.session_state.mensaje=mensaje
            tts_language=detect(api_response)
        # Generate audio from transcript
            tts = gTTS(text=api_response, lang=tts_language, slow=False)
            mp3_fp = BytesIO()
            tts.write_to_fp(mp3_fp)
            autoplay_audio(mp3_fp.getvalue())


    else:

        st.write(notranscripcion)
        print("Transcription failed")



#    Salir = input("¿Quieres salir? (S/N): ").lower().strip() == "s"

