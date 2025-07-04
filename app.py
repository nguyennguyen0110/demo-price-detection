import cv2
import numpy as np
from flask import Flask, Response, request, render_template, json
from service import ocr_service
from utilities.constant import Const

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_demo():
    # Render demo page
    return render_template('index.html')


@app.route('/read-tag', methods=['POST'])
def read_tag():
    # Check content_type
    if not request.content_type.startswith("multipart/form-data"):
        res = {'code': 400, 'message': 'Content type must be multipart/form-data', 'data': None}
    # Check for image
    elif 'image' not in request.files:
        res = {'code': 400, 'message': 'Missing image', 'data': None}
    else:
        # Read image
        file = request.files["image"].read()
        if not file:
            image = cv2.imread('/static/image/IMG_4962.jpeg')
        else:
            arr = np.frombuffer(file, np.uint8)
            image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if image is None:
            res = {'code': 400, 'message': 'Cannot read image', 'data': None}
        # Read text from tag
        else:
            res = {'code': 200, 'message': 'Success', 'data': ocr_service.read_tag(image)}
    return Response(response=json.dumps(res), **Const.RES_PARAM)


@app.route('/demo-read-tag', methods=['GET', 'POST'])
def demo_read_tag():
    template = 'read_tag.html'
    if request.method == 'GET':
        return render_template(template, output={}, raw_out='')
    # Else POST method
    # Check content_type
    if not request.content_type.startswith("multipart/form-data"):
        res = {"error": "content_type not supported"}
    # Check for image
    elif 'image' not in request.files:
        res = {"error": "missing image"}
    else:
        # Read image
        file = request.files["image"].read()
        if not file:
            image = cv2.imread('/static/image/IMG_4962.jpeg')
        else:
            arr = np.frombuffer(file, np.uint8)
            image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if image is None:
            res = {"error": "cannot read image"}
        else:
            res = ocr_service.read_tag(image)
    return render_template(template, output=res, raw_out=json.dumps(res, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    app.run()

# docker build -t demo_pd:v0.0.1 .
# docker run -p 8000:8080 demo_pd:v0.0.1
