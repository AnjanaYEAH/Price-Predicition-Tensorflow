import os
from PIL import Image
from array import *
from random import shuffle
import shutil
from django.conf import settings


media_root = settings.MEDIA_ROOT.replace('\\', '/')

graph_images_url = media_root + "/sorted-graph-images/"
TRAINING_DATA_DIR = media_root + '/../apps/tensor/static/tensor/training-data/'


def convert():
	""" Converts the images into ubyte files that tensorboard can read. """
	uby_url = media_root + "/uby/"
	Names = [[TRAINING_DATA_DIR + 'classified-traingrey', 'train'], [graph_images_url, 'test']]
	for name in Names:
		data_image = array('B')
		data_label = array('B')
		FileList = createListofFiles(name)
		data = createData(FileList, data_image, data_label)
		width = data[2]
		height = data[3]
		header = createHeader(FileList)
		data_label = header + data[1]
		data_image = extendHeader(width, height, header) + data[0]
		createUbyte(name, data_image, data_label)
	# additional header for images array
	moveToMedia(Names, uby_url)



def createListofFiles(name):
	""" Creates a list of files from the train and test directories. """
	FileList = []
	for dirname in os.listdir(name[0])[0:]:
		path = os.path.join(name[0],dirname)
		for filename in os.listdir(path):
			if filename.endswith(".png"):
				FileList.append(os.path.join(name[0],dirname,filename))

	shuffle(FileList) # Usefull for further segmenting the validation set
	return FileList

def createData(FileList, data_image, data_label):
	""" Creates metadata of the images in the file list. """
	for filename in FileList:
		label = int(filename.split('/')[-2])
		Im = Image.open(filename)
		pixel = Im.load()
		width, height = Im.size

		for x in range(0,width):
			for y in range(0,height):
				data_image.append(pixel[y,x])

		data_label.append(label) # labels start (one unsigned byte each)

	return data_image, data_label, width, height

def createHeader(FileList):
	""" Add a hexval header that tensorboard will look for. """
	hexval = "{0:#0{1}x}".format(len(FileList),6) # number of files in HEX

	# header for label array
	header = array('B')
	header.extend([0,0,8,1,0,0])
	header.append(int('0x'+hexval[2:][:2],16))
	header.append(int('0x'+hexval[2:][2:],16))

	return header


def extendHeader(width, height, header):
	""" Add padding to the metadata. """
	# additional header for images array
	if max([width,height]) <= 256:
		header.extend([0,0,0,width,0,0,0,height])
	else:
		raise ValueError('Image exceeds maximum size: 256x256 pixels');

	header[3] = 3 # Changing MSB for image data (0x00000803)

	return header


def createUbyte(name, data_image, data_label):
	""" Generate ubyte files using the newly constructed metadata with the header and padding. """
	output_file = open(name[1] + '-images-idx3-ubyte', 'wb')
	print(name[1])
	data_image.tofile(output_file)
	output_file.close()

	output_file = open(name[1] + '-labels-idx1-ubyte', 'wb')
	data_label.tofile(output_file)
	output_file.close()


def moveToMedia(Names, uby_url):
	""" Zip the ubyte files and move them to the media directory. """
	for name in Names:
		os.system('gzip ' + name[1] + '-images-idx3-ubyte')
		os.system('gzip ' + name[1] + '-labels-idx1-ubyte')
	for name in Names:
		shutil.move(media_root + '/../' + name[1] + '-images-idx3-ubyte' + '.gz', uby_url + name[1] + '-images-idx3-ubyte' + '.gz')
		shutil.move(media_root + '/../' + name[1] + '-labels-idx1-ubyte' + '.gz', uby_url + name[1] + '-labels-idx1-ubyte' + '.gz')
