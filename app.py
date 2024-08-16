from flask import Flask, render_template, request, redirect, url_for
import os
from your_module import AudioVideoProcessor  # Substitua 'your_module' pelo nome real do módulo

app = Flask(__name__)

# Diretório para armazenar arquivos temporários
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    video_file = request.files['video']
    audio_file = request.files['audio']
    
    if not video_file or not audio_file:
        return "Please upload both video and audio files."
    
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)

    video_file.save(video_path)
    audio_file.save(audio_path)

    processor = AudioVideoProcessor(video_path, audio_path, UPLOAD_FOLDER)
    processor.process()

    return redirect(url_for('result'))

@app.route('/result')
def result():
    return render_template('result.html', video_file='video_final.mp4')

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
