import sys
TEST_MODE = 'test' in sys.argv[1:]

if not TEST_MODE:
    global model_from_json
    from keras.models import model_from_json
    global K
    from keras import backend as K

import cv2
import os
from django.conf import settings
from django.core.files.storage import default_storage
from shutil import rmtree

media_root = settings.MEDIA_ROOT.replace('\\', '/') + "/"
TEST_DIR = media_root + "/graph-images/"

sIPath = default_storage.path('sorted-graph-images')
images0 = sIPath + '/0'
images1 = sIPath + '/1'

def get_sIPath():
    return sIPath

logs_path = media_root + "/logs/embedding/"

neuralnetwork_dir = media_root + '/../apps/tensor/neuralnetwork/'
model_json_url = neuralnetwork_dir + 'model.json'
model_h5_url = neuralnetwork_dir + 'model.h5'

if not TEST_MODE:
    json_file = open(model_json_url, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    global loaded_model
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(model_h5_url)
    loaded_model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
    loaded_model._make_predict_function()

def cleanStorage(folder):
    try:
        rmtree(media_root + folder)
    except FileNotFoundError:
        pass

def write_image(img, path):
    if not cv2.imwrite(path, img):
        raise Exception("Could not write file")

def is_png(image_path):
    return image_path[-3:] == 'png'

def parse_prediction(prediction):
    return str(prediction)[2]

def get_image_path(parsed_prediction, image_file):
    if parsed_prediction == '1':
        return images1 + '/' + image_file
    elif parsed_prediction == '0':
        return images0 + '/' + image_file
    else:
        return sIPath + '/unknown/' + image_file

def categorise_images():
    cleanStorage("sorted-graph-images")
    if not default_storage.exists('sorted-graph-images'):
        os.mkdir(sIPath)
        os.mkdir(images0)
        os.mkdir(images1)
    cleanStorage("logs/embedding")
    if not default_storage.exists('logs/embedding'):
        os.mkdir(logs_path)

    for listdir_file in os.listdir(TEST_DIR):
        image_file = str(listdir_file)
        if is_png(image_file):
            original_img = cv2.imread(TEST_DIR + image_file, cv2.IMREAD_GRAYSCALE)
            if original_img is None:
                continue
            original_img = cv2.resize(original_img, (100, 100))

            image = cv2.imread(TEST_DIR + image_file)
            img = cv2.resize(image, (100, 100))
            img = img.reshape(1, 100, 100, 3)

            prediction_output = parse_prediction(loaded_model.predict(img))
            write_image(original_img, get_image_path(prediction_output, image_file))
