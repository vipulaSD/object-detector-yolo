from model_util import load_model, get_output_layer_names
from utils import filter_results, prepare_blob
import numpy as np


class Predictor:
    def __init__(self) -> None:
        self._model, self._labels = load_model()
        self._output_layers = get_output_layer_names(self._model)

    def make_predictions(self, image):
        return self._predict(image)

    def _predict(self, image):
        image_blob, width, height = prepare_blob(image)

        self._model.setInput(image_blob)
        outputs = self._model.forward(self._output_layers)
        class_ids = []
        confidences = []
        boxes = []
        for output in outputs:
            for detection in output:
                scores = detection[5:] # prediction probability for each class
                class_idx = np.argmax(scores) # most probable class
                confidence = scores[class_idx]
                if confidence > 0.5: # filter high confidence predictions
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_idx)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        return filter_results(boxes, confidences, class_ids, self._labels)
