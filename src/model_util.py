import os
import requests
import cv2

# get all output layers of the given model.
def get_output_layer_names(model):
    layers = model.getLayerNames()  # get all layer names
    outputs = [layers[i - 1] for i in model.getUnconnectedOutLayers()]  # filter names of the unconnected layers (outputs)
    return outputs


# check whether the file_path exists, otherwise download the file from given url
def __download_and_prepare_file(file_path, url):
    if not os.path.exists(file_path):
        response = requests.get(url)
        with open(file_path, "wb") as local_file:
            local_file.write(response.content)
        assert os.path.exists(file_path), f"{{file_path}} file not found."
    return file_path


# verify model configuration, weights and label files.
def __get_model_files():
    config_file = __download_and_prepare_file("./model_data/config.cfg", "https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3-spp.cfg")
    weights_file = __download_and_prepare_file("./model_data/weights", "https://pjreddie.com/media/files/yolov3-spp.weights")
    labels_file = __download_and_prepare_file("./model_data/labels", "https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names")

    return config_file, weights_file, labels_file


# load the model from the given files
def load_model():
    config_file, weights_file, labels_file = __get_model_files()
    model = cv2.dnn.readNet(weights_file, config_file)
    labels = []
    with open(labels_file) as file:
        labels = file.read().splitlines()
    return model, labels
