from collections import Counter
import cv2
from cv2 import IMREAD_ANYCOLOR
import numpy as np

_scale = 1 / 255

# filter duplicate boxes
def filter_results(boxes, confidences, class_ids, labels):
    conf_threshold = 0.5
    nms_threshold = 0.4
    # apply non-max suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    results = [labels[class_ids[i]] for i in indices]
    results_count = Counter(results)
    return dict(results_count)



def prepare_blob(image):
    img_buff = np.fromstring(image, np.uint8)
    sample_image = cv2.imdecode(img_buff, IMREAD_ANYCOLOR)
    width = sample_image.shape[1]
    height = sample_image.shape[0]
    image_blob = cv2.dnn.blobFromImage(sample_image, _scale, (416, 416), (0, 0, 0), True, crop=False)

    return image_blob, width, height
