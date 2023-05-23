import os
import tempfile
import flask
from flask import request
from flask_cors import CORS
import whisper

app = flask.Flask(__name__)
CORS(app)
actmodel='medium'
audio_model = whisper.load_model(actmodel)
# endpoint for handling the transcribing of audio inputs
@app.route('/transcribe', methods=['POST'])
def transcribe():
    global actmodel
    global audio_model
    if request.method == 'POST':
        archivo_audio = request.files['audio_data']
        language = request.form['language']
        model = request.form['model_size']
        # there are no english models for large
        # is there a model change?
        if model != actmodel:
            if model != 'large' and language == 'english':
                actmodel=model
                model = model + '.en'
                audio_model = whisper.load_model(model)
            else:
                audio_model = whisper.load_model(model)
                actmodel=model
        temp_dir = tempfile.mkdtemp()
        save_path = os.path.join(temp_dir, 'temp.wav')
        archivo_audio.save(save_path)
        print("Saved audio to: " + save_path
              + " with language: " + language
              + " and model: " + model)
        if language == 'english':
            result = audio_model.transcribe(save_path, language='english')
        else:
            result = audio_model.transcribe(save_path, language=language)
        print('Transcripción: ',result['text'])
        return result['text']
    else:
        return "This endpoint only processes POST wav blob"