"""
    To run all tests:
    python manage.py test apps.tensor.tests

    To run specific test cases:
    python manage.py test apps.tensor.tests.<name of test class>
"""

from django.test import TestCase
from . import views
from .mainbackend import use_model, convertUbyte, pre, buysellhold
from django.conf import settings
from array import *
import os
media_root = settings.MEDIA_ROOT.replace('\\', '/')
graph_images_url = media_root + "/testgraphimages/"
TRAINING_DATA_DIR = media_root + '/../apps/tensor/static/tensor/training-data/'
Names = [[TRAINING_DATA_DIR + 'testtraingrey', 'train']]


class TensorTest(TestCase):
    def test_is_png(self):
        assert use_model.is_png('foo.png')
        assert not use_model.is_png('foo.jpg')

    def test_get_image_path(self):
        assert use_model.get_image_path('1', 'some_image.png') == (
            use_model.get_sIPath() + '/1/some_image.png')

    def test_accuracy(self):
        directory0 = sorted(os.listdir(TRAINING_DATA_DIR + 'testtraingrey/0/'))
        directory1 = sorted(os.listdir(TRAINING_DATA_DIR + 'testtraingrey/1/'))
        directory = sorted(directory0 + directory1)
        accuracy = buysellhold.accuracy(directory0, directory1, len(directory))
        assert accuracy == 1

    def test_resize(self):
        img = pre.resize('02-01-2009_09-31__02-01-2009_09-40__0.png',
                         TRAINING_DATA_DIR + 'testtraingrey/0/')
        assert img is not None

    def test_resizegrey(self):
        img = pre.resizegrey('02-01-2009_09-31__02-01-2009_09-40__0.png',
                             TRAINING_DATA_DIR + 'testtraingrey/0/')
        assert img is not None

    def test_create_list_of_files(self):
        testtraingrey = convertUbyte.createListofFiles(Names[0])
        greyimg1 = str(TRAINING_DATA_DIR) + \
            "testtraingrey/1/12-01-2009_11-51__12-01-2009_12-00__1.png"
        greyimg0 = str(TRAINING_DATA_DIR) + \
            "testtraingrey/0/02-01-2009_09-31__02-01-2009_09-40__0.png"
        assert testtraingrey[0] == greyimg1 or testtraingrey[0] == greyimg0

    def test_create_data(self):
        FileList = [str(TRAINING_DATA_DIR) +
                    "testtraingrey/1/12-01-2009_11-51__12-01-2009_12-00__1.png"]
        data_image = array('B')
        data_label = array('B')
        data = convertUbyte.createData(FileList, data_image, data_label)
        assert data[1] == array('B', [1]) and data[2] == 100 and data[3] == 100

    def test_create_header(self):
        FileList = [str(TRAINING_DATA_DIR) +
                    "testtraingrey/1/12-01-2009_11-51__12-01-2009_12-00__1.png"]
        header = convertUbyte.createHeader(FileList)
        assert header == array('B', [0, 0, 8, 1, 0, 0, 0, 1])

    def test_extend_header(self):
        FileList = [str(TRAINING_DATA_DIR) +
                    "testtraingrey/1/12-01-2009_11-51__12-01-2009_12-00__1.png"]
        width = 100
        height = 100
        header = array('B', [0, 0, 8, 1, 0, 0, 0, 1])
        xHeader = convertUbyte.extendHeader(width, height, header)
        assert xHeader == array(
            'B', [0, 0, 8, 3, 0, 0, 0, 1, 0, 0, 0, 100, 0, 0, 0, 100])

    def test_create_uby(self):
        greyimg1 = str(TRAINING_DATA_DIR) + \
            "testtraingrey/1/12-01-2009_11-51__12-01-2009_12-00__1.png"
        FileList = [greyimg1]
        width = 100
        height = 100
        header = array('B', [0, 0, 8, 1, 0, 0, 0, 1])
        xHeader = array('B', [0, 0, 8, 3, 0, 0, 0, 1,
                              0, 0, 0, 100, 0, 0, 0, 100])
        data_image = array('B')
        data_label = array('B')
        data = convertUbyte.createData(FileList, data_image, data_label)
        data_label = header + data[1]
        data_image = xHeader + data[0]
        convertUbyte.createUbyte(Names[0], data_image, data_label)
        ubyimages = "train-images-idx3-ubyte"
        ubylabels = "train-labels-idx1-ubyte"
        currentdir = os.listdir(media_root + "/..")
        if ubyimages and ubylabels in currentdir:
            assert True
        else:
            assert False

    def test_move_uby(self):
        uby_url = TRAINING_DATA_DIR + "/testtraingrey/uby/"
        convertUbyte.moveToMedia(Names, uby_url)
        ubyimages = "train-images-idx3-ubyte.gz"
        ubylabels = "train-labels-idx1-ubyte.gz"
        ubydir = os.listdir(uby_url)
        if ubyimages and ubylabels in ubydir:
            assert True
        else:
            assert False

    def test_tensorboard_instance(self):
        links = views.createTensorboardInstance(8080)
        pid = links[1].split("=")[1].split("&")[0]
        views.killPort(int(pid), 8080)
        assert links[0] == 'http://localhost:8080/#projector&run=.'

    def test_generate_port(self):
        port = views.generatePort()
        ports = views.ports_in_use
        if port >= 3081 and port <= 9000:
            assert port in ports
        else:
            assert False
