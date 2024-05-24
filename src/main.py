import os
import subprocess
import cv2
import numpy as np
from flask import Flask, request, send_file, jsonify
import threading
import time

app = Flask(__name__)

# Variables globales para el progreso de procesamiento y fotogramas ASCII
processing_progress = 0
ascii_frames = []

@app.route("/")
def index():
    return send_file('index.html')

def main():
    app.run(port=int(os.environ.get('PORT', 5000)))

def extract_audio(video_path, audio_path):
    command = f'ffmpeg -i {video_path} -q:a 0 -map a {audio_path}'
    subprocess.call(command, shell=True)

def delete_previous_files():
    video_path = 'uploaded_video.mp4'
    audio_path = os.path.join('src', 'uploaded_audio.mp3')
    if os.path.exists(video_path):
        os.remove(video_path)
    if os.path.exists(audio_path):
        os.remove(audio_path)

def video_to_ascii(video_path, new_width=100):
    global processing_progress, ascii_frames
    try:
        cap = cv2.VideoCapture(video_path)
        ascii_frames = []
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        current_frame = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Redimensionar el fotograma manteniendo la relación de aspecto
            height, width = frame.shape[:2]
            aspect_ratio = height / width
            new_height = int(aspect_ratio * new_width)
            resized_frame = cv2.resize(frame, (new_width, new_height))

            # Convertir el fotograma a escala de grises
            gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
            ascii_frame = convert_frame_to_ascii(gray_frame)
            ascii_frames.append(ascii_frame)

            current_frame += 1
            processing_progress = (current_frame / total_frames) * 100

            # Calcular la duración del fotograma actual
            frame_duration = 1 / cap.get(cv2.CAP_PROP_FPS)
            time.sleep(frame_duration)  # Esperar la duración del fotograma

        cap.release()
        processing_progress = 100  # Asegurarse de que esté al 100% al finalizar
    except Exception as e:
        processing_progress = 0
        ascii_frames = []
        print("Error:", str(e))

def convert_frame_to_ascii(gray_frame):
    chars = np.where(gray_frame > 127, 'ñ', '_')
    ascii_frame = "\n".join("".join(row) for row in chars)
    return ascii_frame

@app.route('/upload', methods=['POST'])
def upload_file():
    global ascii_frames
    file = request.files['videoFile']
    if file:
        # Eliminar archivos anteriores y limpiar frames ASCII
        delete_previous_files()
        ascii_frames = []
        
        video_path = 'uploaded_video.mp4'
        audio_path = os.path.join('src', 'uploaded_audio.mp3')
        file.save(video_path)
        
        # Extraer el audio del video
        extract_audio(video_path, audio_path)
        
        # Convertir el video a ASCII en un hilo separado
        video_thread = threading.Thread(target=video_to_ascii, args=(video_path,))
        video_thread.start()
        
        # Enviar el resultado al cliente
        return jsonify({"message": "Processing started"}), 200

@app.route('/ascii', methods=['GET'])
def get_ascii():
    global ascii_frames
    if not ascii_frames:
        return jsonify({"error": "Error al obtener los frames ASCII."}), 500
    return jsonify({"frames": ascii_frames})

@app.route('/progress', methods=['GET'])
def get_progress():
    global processing_progress
    return jsonify({"progress": processing_progress})

@app.route('/audio', methods=['GET'])
def get_audio():
    audio_path = os.path.join('uploaded_audio.mp3')
    full_audio_path = os.path.join(app.root_path, audio_path)  # Obtener la ruta completa al archivo de audio
    if not os.path.exists(full_audio_path):
        return jsonify({"error": "Audio file does not exist"}), 404
    return send_file(full_audio_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)