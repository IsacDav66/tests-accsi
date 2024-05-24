import os
import subprocess
import cv2
import numpy as np
from flask import Flask, request, send_file, jsonify
import threading
import time
from PIL import Image, ImageDraw

app = Flask(__name__)

# Variables globales para el progreso de procesamiento y fotogramas ASCII
processing_progress = 0
ascii_frames = []
# Obtener la ruta absoluta del directorio actual
current_dir = os.path.abspath(os.path.dirname(__file__))
# Directorio donde se almacenarán los archivos subidos
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    delete_previous_files()  # Eliminar archivos anteriores cuando se recarga la página
    return send_file('index.html')

def main():
    app.run(port=int(os.environ.get('PORT', 5000)))

def extract_audio(video_path, audio_path):
    command = f'ffmpeg -i {video_path} -q:a 0 -map a {audio_path}'
    subprocess.call(command, shell=True)

def delete_previous_files():
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        os.rmdir(UPLOAD_FOLDER)
    
    if os.path.exists('ascii_frames'):
        for filename in os.listdir('ascii_frames'):
            file_path = os.path.join('ascii_frames', filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        os.rmdir('ascii_frames')

    if os.path.exists('video_output'):
        for filename in os.listdir('video_output'):
            file_path = os.path.join('video_output', filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        os.rmdir('video_output')
    
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs('ascii_frames', exist_ok=True)
    os.makedirs('video_output', exist_ok=True)


def video_to_ascii(video_path, new_width=100):
    global processing_progress, ascii_frames
    try:
        cap = cv2.VideoCapture(video_path)
        ascii_frames = []
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
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

            # Guardar el frame ASCII como una imagen
            save_frames_as_images([ascii_frame], current_frame, new_width * 2, new_height * 2)

            # Calcular la duración del fotograma actual
            frame_duration = 1 / fps
            time.sleep(frame_duration)  # Esperar la duración del fotograma

        cap.release()
        processing_progress = 100  # Asegurarse de que esté al 100% al finalizar

        # Generar video a partir de los frames
        audio_path = os.path.join(UPLOAD_FOLDER, 'uploaded_audio.mp3')
        generate_video_from_frames('ascii_frames', 'video_output/ascii_video.mp4', audio_path, fps, original_width, original_height)

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
        
        video_path = os.path.join(UPLOAD_FOLDER, 'uploaded_video.mp4')
        audio_path = os.path.join(UPLOAD_FOLDER, 'uploaded_audio.mp3')
        file.save(video_path)
        
        # Extraer el audio del video
        extract_audio(video_path, audio_path)
        
        # Convertir el video a ASCII en un hilo separado
        video_thread = threading.Thread(target=video_to_ascii, args=(video_path,))
        video_thread.start()
        
        # Enviar el resultado al cliente
        fps = cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FPS)
        return jsonify({"message": "Processing started", "fps": fps}), 200

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
    audio_path = os.path.join(os.path.dirname(current_dir),UPLOAD_FOLDER,'uploaded_audio.mp3')
    print(audio_path)
    if not os.path.exists(audio_path):
        return jsonify({"error": "Audio file does not exist"}), 404
    return send_file(audio_path, as_attachment=True)

def save_frames_as_images(frames, frame_number, width, height):
    image_folder = "ascii_frames"
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    
    for i, frame in enumerate(frames):
        image_path = os.path.join(image_folder, f"frame_{frame_number:04d}.png")
        img = Image.new('RGB', (width * 3, height * 8), color = 'black')
        d = ImageDraw.Draw(img)
        d.text((10,10), frame, fill=(255,255,255))
        img.save(image_path)

def generate_video_from_frames(image_folder, output_video_path, audio_path, fps, width, height):
    temp_video_path = output_video_path.replace('.mp4', '_temp.mp4')
    command = (
        f'ffmpeg -framerate {fps} -i {image_folder}/frame_%04d.png '
        f'-vf "scale={width}:{height}" '
        f'-c:v libx264 -r {fps} -pix_fmt yuv420p {temp_video_path}'
    )
    print(f"Running command to generate video: {command}")  # Debugging statement
    result = subprocess.call(command, shell=True)
    
    if result == 0:
        print("Video generated successfully.")
        # Combinar el video generado con el audio
        command = (
            f'ffmpeg -i {temp_video_path} -i {audio_path} '
            f'-c:v copy -c:a aac -strict experimental {output_video_path}'
        )
        print(f"Running command to add audio: {command}")  # Debugging statement
        result = subprocess.call(command, shell=True)
        
        if result == 0:
            print("Audio added to video successfully.")
            os.remove(temp_video_path)  # Eliminar el video temporal
        else:
            print("Error adding audio to video.")
    else:
        print("Error generating video.")


if __name__ == '__main__':
    app.run(debug=True)
