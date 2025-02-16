import json
from django.http import StreamingHttpResponse, HttpResponse
import cv2
import os
import numpy as np
from django.shortcuts import render
from mediapipe.python.solutions.holistic import Holistic
from keras.models import load_model
from core.utils.text_to_speech import text_to_speech
from core.utils.helpers import draw_keypoints, extract_keypoints, format_sentences, get_actions, mediapipe_detection, there_hand
from core.utils.constants import DATA_PATH, MAX_LENGTH_FRAMES, MIN_LENGTH_FRAMES, MODEL_NAME, MODELS_PATH

camera_running = False
camera = None

model = load_model(os.path.join(MODELS_PATH, MODEL_NAME))

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.holistic_model = Holistic()
        self.model = model
        self.kp_sequence = []
        self.sentence = []
        self.repe_sent = 1
        self.count_frame = 0
        self.actions = get_actions(DATA_PATH)
        self.palabras = ""
        self.acumulado_palabras = ""

    def __del__(self):
        self.video.release()
        self.holistic_model.close()

    def get_frame(self):
        success, frame = self.video.read()
        if not success:
            return None, self.acumulado_palabras

        image, results = mediapipe_detection(frame, self.holistic_model)
        self.kp_sequence.append(extract_keypoints(results))

        if len(self.kp_sequence) > MAX_LENGTH_FRAMES and there_hand(results):
            self.count_frame += 1
        else:
            if self.count_frame >= MIN_LENGTH_FRAMES:
                res = self.model.predict(np.expand_dims(self.kp_sequence[-MAX_LENGTH_FRAMES:], axis=0))[0]
                if res[np.argmax(res)] > 0.3:
                    sent = self.actions[np.argmax(res)]
                    self.sentence.insert(0, sent)
                    text_to_speech(sent)
                    self.sentence, self.repe_sent = format_sentences(sent, self.sentence, self.repe_sent)
                else:
                    text_to_speech("no hay coincidencia")
                self.count_frame = 0
                self.kp_sequence = []

        #cv2.rectangle(image, (0,0), (640, 35), (245, 117, 16), -1)
        #cv2.putText(image, ' | '.join(self.sentence), FONT_POS, FONT, FONT_SIZE, (255, 255, 255))

        if self.sentence and len(self.sentence) > 0 and self.sentence[0] != self.palabras:
            self.palabras += self.sentence[0] + " "
            self.acumulado_palabras = self.palabras
            self.sentence.pop(0)

        draw_keypoints(image, results)
        ret, jpeg = cv2.imencode('.jpg', image)

        return jpeg.tobytes()

    def obtener_version_concatenada(self):
        return self.acumulado_palabras

def gen(camera):
    while camera_running:
        frame = camera.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def start_camera(request):
    global camera_running, camera
    camera_running = True
    if camera is None:
        camera = VideoCamera()
    return HttpResponse("Camera started")

def stop_camera(request):
    global camera_running, camera

    version_concatenada = camera.obtener_version_concatenada()

    camera_running = False
    if camera is not None:
        del camera
        camera = None

    response_data = {
        'palabras_concatenadas': version_concatenada
    }

    return HttpResponse(json.dumps(response_data), content_type='application/json')

def video_feed(request):
    global camera
    if camera is not None:
        return StreamingHttpResponse(gen(camera),
                                     content_type='multipart/x-mixed-replace; boundary=frame')
    else:
        return HttpResponse("Camera not started", status=404)
