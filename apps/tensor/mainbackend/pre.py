import os
import cv2
from django.conf import settings


media_root = settings.MEDIA_ROOT.replace('\\', '/')

# DIRECTORY FOR OUR NEURAL NETWORK TRAINING DATA
TRAINING_DATA_DIR = media_root + '/../apps/tensor/static/tensor/training-data/'

CLASSIFIED_TRAIN0= TRAINING_DATA_DIR + "classified-train/0/"
CLASSIFIED_TRAIN1= TRAINING_DATA_DIR + "classified-train/1/"
CLASSIFIED_TRAINgrey0= TRAINING_DATA_DIR + "classified-traingrey/0/"
CLASSIFIED_TRAINgrey1= TRAINING_DATA_DIR + "classified-traingrey/1/"
UNCLASSIFIED_TRAIN = TRAINING_DATA_DIR + "unclassified-train/"
IMG_SIZE = 100

""" Classifies the training data into 0 (sell) 1 (buy) so that we can train the model. """
def create_train_test_dir():
	for i in os.listdir(UNCLASSIFIED_TRAIN):
		b = str(i)
		if (b[-1] == 'g' and b[-2] == 'n' and b[-3] == 'p'):
			img = resize(i,UNCLASSIFIED_TRAIN)
			imggrey = resizegrey(i,UNCLASSIFIED_TRAIN)
			buyorsell = b[-5]
			if img is None:
				continue
			writeimage()
			if buyorsell == '1':
				cv2.imwrite(CLASSIFIED_TRAIN1 + i, img)
				cv2.imwrite(CLASSIFIED_TRAINgrey1 + i, imggrey)
			elif buyorsell == '0':
				cv2.imwrite(CLASSIFIED_TRAIN0 + i, img)
				cv2.imwrite(CLASSIFIED_TRAINgrey0 + i, imggrey)


""" Resize the images so that it can be an input to CNN model. """
def resize(i,path):
	img = cv2.imread(path + i)
	if img is None:
		return None
	img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
	return img


""" Resize the images so that it can be an input to TSNE algorithm. """
def resizegrey(i,path):
	imggrey = cv2.imread(path + i, cv2.IMREAD_GRAYSCALE)
	if imggrey is None:
		return None
	imggrey = cv2.resize(imggrey, (IMG_SIZE, IMG_SIZE))
	return imggrey
