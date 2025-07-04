import numpy as np
from mmocr.apis import TextDetInferencer


class PANet:
    _model = TextDetInferencer(model='PANet_CTW', weights='model/panet_ctw_20220826.pth')

    @classmethod
    def detect_text(cls, image):
        """
        Detect text in image.
        :param image: image need to detect text
        :return: polygons of detected texts (numpy array)
        """
        result = cls._model(image)
        # result has 2 key: 'predictions' and 'visualization', we do not use 'visualization'
        # predictions is a list of {'polygons': [[x1, y1, x2, y2, x3, y3, x4, y4],[...]], 'scores': []}
        # We just need polygons and predict one image at a time
        polygons = np.array(result['predictions'][0]['polygons'])
        polygons = polygons.round().astype('int')
        return polygons.reshape((len(polygons), -1, 2))
