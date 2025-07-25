import cv2
import numpy as np
from flask import Flask, Response, request, render_template, json
from service import ocr_service
from utilities.constant import Const

app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    # Render demo page
    return render_template('index.html')


@app.route('/read-tag', methods=['POST'])
def read_tag():
    # Check content_type
    if request.content_type is None or not request.content_type.startswith(Const.FORM):
        res = {'code': 400, 'message': Const.NOT_FORM, 'data': {}}
    # Check for image
    elif 'image' not in request.files:
        res = {'code': 400, 'message': 'Missing image', 'data': {}}
    else:
        # Read image
        file = request.files['image'].read()
        if not file:
            image = cv2.imread('static/image/IMG_4962.jpeg')
        else:
            arr = np.frombuffer(file, np.uint8)
            image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if image is None:
            res = {'code': 400, 'message': 'Cannot read image', 'data': {}}
        # Read text from tag
        else:
            res = {'code': 200, 'message': 'Success',
                   'data': ocr_service.read_tag(image)}
    return Response(response=json.dumps(res), **Const.RES_PARAM)


@app.route('/demo-read-tag', methods=['GET', 'POST'])
def demo_read_tag():
    template = 'read_tag.html'
    if request.method == 'GET':
        return render_template(template, output={}, raw_out='')
    # Else POST method
    # Check content_type
    if not request.content_type.startswith(Const.FORM):
        res = {'code': 400, 'message': Const.NOT_FORM, 'data': {}}
    # Check for image
    elif 'image' not in request.files:
        res = {'code': 400, 'message': 'Missing image', 'data': {}}
    else:
        # Read image
        file = request.files["image"].read()
        if not file:
            image = cv2.imread('static/image/IMG_4962.jpeg')
        else:
            arr = np.frombuffer(file, np.uint8)
            image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if image is None:
            res = {'code': 400, 'message': 'Cannot read image', 'data': {}}
        else:
            res = {'code': 200, 'message': 'Success',
                   'data': ocr_service.read_tag(image)}
    raw_output = _decor_output(res)
    return render_template(template, output=res, raw_out=raw_output)


def _decor_output(obj):
    """
    Make a pretty JSON string for response object.
    :param obj: response object
    :return: string
    """
    data = {}
    for k in obj['data']:
        if k != 'polygons':
            data[k] = obj['data'][k]
    copy_obj = {'code': obj['code'], 'message': obj['message'], 'data': data}
    res = json.dumps(copy_obj, indent=4)
    if obj['data']:
        poly = obj['data']['polygons']
        poly_str = ''
        for p in poly:
            poly_str += str(p) + ',\n' + ' ' * 12
        poly_str = poly_str[:-14]
        i = res.find('data":')
        res = (res[:i+8] + '\n        "polygons": [\n            ' + poly_str
               + '\n        ],' + res[i+8:])
    return res


if __name__ == '__main__':
    app.run()
