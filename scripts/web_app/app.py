from flask import Flask, request, send_file, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import cv2
import numpy as np
from ultralytics import YOLO
import io
import socket

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app, default_limits=["3 per second"])

model = YOLO("scripts/web_app/model/best.engine")  # Assure-toi que le fichier est dans le dossier

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/detect', methods=['POST'])
@limiter.limit("2/second")
def detect():
    file = request.files['frame'].read()
    npimg = np.frombuffer(file, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    results = model.predict(   
                                        frame,
                                        conf=0.5, 
                                        iou=0.5, 
                                        classes=23
                                    )[0]
    annotated_frame = results.plot()

    _, img_encoded = cv2.imencode('.jpg', annotated_frame)
    return send_file(
        io.BytesIO(img_encoded.tobytes()),
        mimetype='image/jpeg'
    )

if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    print(f"App running on http://{ip}:8000")
    app.run(host='0.0.0.0', port=8000)
