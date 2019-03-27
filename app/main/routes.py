from flask import session, redirect, url_for, render_template, request, Response
from . import main
from importlib import import_module
import os
from app.main.camera_1 import Camera
from .. import socketio
from app.main.utilities import emit_log




def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@main.route('/video_feed')
def video_feed():
    emit_log('hello world!')
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
