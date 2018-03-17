import os
import cv2
import sys
from base_camera import BaseCamera
from audiopy import start_player
import asyncio


basedir = os.path.abspath(os.path.dirname(__file__))
##https://irwinkwan.com/2013/04/29/python-executables-pyinstaller-and-a-48-hour-game-design-compo/
def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

class Camera(BaseCamera):
    video_source = 0
    score = 100
    classifier = 0


    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def set_classifier(status):
        Camera.classifier = status

    @staticmethod
    def camera_reset():
        Camera.score = 100

    @staticmethod
    def get_score():
        return Camera.score

    @staticmethod
    def frames():
        audio = resource_path(os.path.join('static', 'story.mp3'))
        face_cascade = cv2.CascadeClassifier(resource_path(os.path.join('static', 'haarcascade_frontalface_alt.xml')))
        eye_cascade = cv2.CascadeClassifier(resource_path(os.path.join('static','parojosG.xml')))
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        counter = 0
        while True:
            # Capture frame-by-frame
            
            ret, frame = camera.read()
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #https://docs.opencv.org/master/d6/d00/tutori al_py_root.html
            faces = face_cascade.detectMultiScale(gray,
                                      scaleFactor=1.1,
                                      minNeighbors=3,
                                      minSize=(100, 100),
                                      flags=cv2.CASCADE_SCALE_IMAGE)
    
            font = cv2.FONT_HERSHEY_SIMPLEX
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=4,
                                                    flags=cv2.CASCADE_FIND_BIGGEST_OBJECT)
                if Camera.classifier == 1:
                    if(not len(eyes)):
                        cv2.putText(roi_color, 'Sleeping', (20, 20), font,
                                1, (255, 255, 255), 2, cv2.LINE_AA)
                        counter += 1
                        if counter == 50:
                            Camera.score -= 1
                            loop = asyncio.new_event_loop()
                            loop.run_until_complete(start_player(audio))
                            loop.close
                            counter = 0
                            
                    else:
                        cv2.putText(roi_color, 'Awake', (20, 20), font,
                            1, (255, 255, 255), 2, cv2.LINE_AA)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                cv2.putText(roi_color, '{}'.format(Camera.score), (w//2, h//2), font, 1, (255,0,255), 2, cv2.LINE_AA)
            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', frame)[1].tobytes()
#pyinstaller -w -F webcamtest.py --hidden-import  ctypes --path 'C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64'
#pyinstaller -F webcamtest.py --hidden-import  ctypes --path 'C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64'yinstaller -F webcamtest.py --hidden-import  ctypes --path 'C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64'
#pyinstaller -w -F app.py --hidden-import  ctypes --path 'C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64'
#pyinstaller -w webcamtest.py --hidden-import  ctypes --path 'C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64'
#pyinstaller -w --add-data "templates;templates" --add-data "static;static" app.py --hidden-import  ctypes --path 'C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64'
#pyinstaller -w -F --add-data "templates;templates" --add-data "static;static" app.py --hidden-import  ctypes --path 'C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64'
