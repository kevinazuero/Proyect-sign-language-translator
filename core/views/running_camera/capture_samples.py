import json
import os
import cv2
import numpy as np
from mediapipe.python.solutions.holistic import Holistic
from core.utils.helpers import create_folder, draw_keypoints, mediapipe_detection, save_frames, there_hand,delete_files
from core.utils.constants import FONT, FONT_POS, FONT_SIZE, FRAME_ACTIONS_PATH, ROOT_PATH, DATA_PATH, MODEL_NAME
from django.http import StreamingHttpResponse, HttpResponse


camera_running = False
camera = None
palabra=""

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.holistic_model = Holistic()
        self.count_frame = 0
        self.frames = []
        self.current_sample = 0  # Progreso actual del sample
        self.current_word = ""  # Palabra actual

    def __del__(self):
        self.video.release()
        self.holistic_model.close()

    def get_frame(self):
        count_sample = 0
        path = get_path()
        if not os.path.exists(path):
            create_folder(path)
        cant_sample_exist = len(os.listdir(path))
        margin_frame=2
        min_cant_frames=5
        
        while self.video.isOpened():
            _, frame = self.video.read()
            image, results = mediapipe_detection(frame, self.holistic_model)
            
            if there_hand(results):
                self.count_frame += 1
                if self.count_frame > margin_frame: 
                    cv2.putText(image, 'Capturando...', FONT_POS, FONT, FONT_SIZE, (255, 50, 0))
                    self.frames.append(np.asarray(frame))
                
            else:
                if len(self.frames) > min_cant_frames + margin_frame:
                    self.frames = self.frames[:-margin_frame]
                    output_folder = os.path.join(path, f"sample_{cant_sample_exist + count_sample + 1}")
                    create_folder(output_folder)
                    save_frames(self.frames, output_folder)
                    count_sample += 1
                    self.current_sample = cant_sample_exist + count_sample  # Actualizar progreso
                    self.current_word = palabra  # Actualizar palabra actual
                
                self.frames = []
                self.count_frame = 0
                cv2.putText(image, 'Listo para capturar...', FONT_POS, FONT, FONT_SIZE, (0,220, 100))
                
            draw_keypoints(image, results)
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()

def gen(camera):
    while camera_running:
        frame = camera.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def start_camera(request):
    
    data = json.loads(request.body)    
    word = data.get('word', None)
        
    global camera_running, camera,palabra
    palabra=word
    camera_running = True
    if camera is None:
        camera = VideoCamera()
    return HttpResponse(json.dumps({"mensaje": "exito"}), content_type='application/json')

def stop_camera(request):
    global camera_running, camera

    camera_running = False
    if camera is not None:
        del camera
        camera = None
        
    return HttpResponse(json.dumps({"mensaje": "exito"}), content_type='application/json')

def video_feed(request):
    global camera
    if camera is not None:
        return StreamingHttpResponse(gen(camera),
                                     content_type='multipart/x-mixed-replace; boundary=frame')
    else:
        return HttpResponse("Camera not started", status=404)

def get_path():
    word_name = palabra
    word_path = os.path.join(ROOT_PATH, FRAME_ACTIONS_PATH, word_name)
    return word_path

def get_progress(request):
    global camera
    if camera is not None:
        return HttpResponse(
            json.dumps({
                "current_sample": camera.current_sample,
                "current_word": camera.current_word,
            }),
            content_type="application/json"
        )
    else:
        return HttpResponse(json.dumps({"error": "Camera not started"}), status=404, content_type="application/json")