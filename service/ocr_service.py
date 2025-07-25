import numpy as np
import cv2
import pytesseract
from unidecode import unidecode
from utilities.model import PANet


def order_points(points):
    """
    Get numpy array with 4 points (x, y), sort them in order (top-left, top-right, bottom-right, bottom-left) and
    return sorted array.
    :param points: numpy array with 4 points (x, y) to sort
    :return: Sorted array.
    """
    # Initialize a list of coordinates
    quadrilateral = np.zeros((4, 2), dtype='float32')
    # The top-left point will have the smallest sum, whereas the bottom-right point will have the largest sum
    total = points.sum(axis=1)
    quadrilateral[0] = points[np.argmin(total)]
    quadrilateral[2] = points[np.argmax(total)]
    # Compute the difference between the points, the top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    difference = np.diff(points, axis=1)
    quadrilateral[1] = points[np.argmin(difference)]
    quadrilateral[3] = points[np.argmax(difference)]
    # Return the ordered coordinates
    return quadrilateral


def four_point_transform(image, points):
    """
    Get image and numpy array with 4 points (x, y) of a polygon, crop image due to polygon and transform into a
    rectangle
    :param image: original image
    :param points: numpy array with 4 points (x, y) of a polygon
    :return: Cropped and warped image
    """
    # Obtain a consistent order of the points and unpack them
    quadrilateral = order_points(points)
    (tl, tr, br, bl) = quadrilateral
    # Compute the width of the new image, which will be the maximum distance between bottom-right and bottom-left
    # x-coordinates or the top-right and top-left x-coordinates
    width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    max_width = max(int(width_a), int(width_b))
    # Compute the height of the new image, which will be the maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    max_height = max(int(height_a), int(height_b))
    # Now that we have the dimensions of the new image, construct the set of destination points to obtain a
    # "birds eye view", (i.e. top-down view) of the image, again specifying points in the top-left, top-right,
    # bottom-right, and bottom-left order
    destination = np.array([[0, 0], [max_width - 1, 0], [max_width - 1, max_height - 1], [0, max_height - 1]],
                           dtype='float32')
    # Compute the perspective transform matrix and then apply it
    matrix = cv2.getPerspectiveTransform(quadrilateral, destination)
    warped = cv2.warpPerspective(image, matrix, (max_width, max_height))
    # Return the warped image
    return warped


def get_price_from_text(text):
    """
    Try to get selling price from text string.
    :param text: text want to check
    :return: price (in number) or None
    """
    # Turn to lower case
    check_price = text.lower()
    # Remove unit (/box, /kg, /ml, ...) if any
    check_price = check_price.split('/')
    # Remove currency unit, space and punctuation if any
    for e in ['vnd', 'dong', 'd', '.', ',', ' ']:
        check_price[0] = check_price[0].replace(e, '')
    # If there is a "/" or less, and first string is all digits
    if (len(check_price) < 3) and (check_price[0].isdigit()):
        return int(check_price[0])
    return None


def read_text(image, polygon):
    """
    Read text from a position in image.
    :param image: image to read
    :param polygon: position to read
    :return: text and area
    """
    # Transform the quadrilateral to rectangle and change color to grayscale
    text_img = four_point_transform(image, polygon)
    text_img = cv2.cvtColor(text_img, cv2.COLOR_BGR2GRAY)
    # Get the text by Tesseract, remove new line character returned by tesseract
    text = pytesseract.image_to_string(text_img, lang='vie_price_tag', config='--psm 7 -c page_separator=')
    return {'text': text[:-1], 'area': text_img.shape[0] * text_img.shape[1]}


def read_tag(image):
    """
    Detect and read all the text from image and return them in accents form and decoded form with their
    positions. Try to get number with the largest area as selling price.
    :param image: image to read text
    :return: product name, selling price information and all texts
    """
    # Detect text in image
    text_position = PANet.detect_text(image)
    # Initialize some list to contain information of each text
    texts = []
    decoded_texts = []
    polygons = []
    price = None
    price_index = None
    number_area = 0
    # Process each detected text
    for position in text_position:
        # Get text
        text = read_text(image, position)
        # Do nothing if read empty text
        if len(text['text']) == 0:
            continue
        decoded_text = unidecode(text['text'])
        # Add text, decoded text and its position
        texts.append(text['text'])
        decoded_texts.append(decoded_text)
        polygons.append(position.tolist())
        # Do not need to check for selling price if current area is smaller
        if text['area'] <= number_area:
            continue
        # Check for price and get number
        check_price = get_price_from_text(decoded_text)
        if check_price is not None:
            price = check_price
            price_index = len(texts) - 1
            number_area = text['area']
    result = {
        'height': image.shape[0], 'width': image.shape[1],
        'texts': texts, 'decoded_texts': decoded_texts, 'polygons': polygons,
        'price': price, 'price_index': price_index
    }
    if len(texts) == 0:
        result['product_name'] = '' if len(decoded_texts) == 0 else decoded_texts[0]
    else:
        result['product_name'] = texts[0]
    return result
