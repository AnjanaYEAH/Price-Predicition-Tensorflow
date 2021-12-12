import os
from django.conf import settings


media_root = settings.MEDIA_ROOT.replace('\\', '/')
test_images = media_root + "/sorted-graph-images/"
TEST_IMAGES0= test_images + "/0/"#"../test-images/0/"
TEST_IMAGES1= test_images + "/1/"#./test-images/1/"
TEST= media_root + "/graph-images/"


def accuracy(directory0, directory1, total):
	""" Creates an accuracy prediction for the data that tensorflow has predicted. """
	correct0 = 0
	correct1 = 0

	for i in directory0:
		if i[-5] == '0':
			correct0 += 1

	for i in directory1:
		if i[-5] == '1':
			correct1 += 1

	return (correct0 + correct1)/total


def buysellhold():
	""" Generate the probabilty of buy, sell or hold. """
	directory0 = sorted(os.listdir(TEST_IMAGES0))
	directory1 = sorted(os.listdir(TEST_IMAGES1))
	directory = sorted(directory0 + directory1)
	print("Size of dir: {}".format(len(directory)))
	if directory[-1][-5] == '1':
		buy = accuracy(directory0, directory1, len(directory))
		total0 = 0
		for i in directory[-10:]:
			if i[-5] == '0':
				total0+=1
		sell = (total0/10) * (1-buy)
		hold = 1 - sell - buy
	else:
		sell = accuracy(directory0, directory1, len(directory))
		total1 = 0
		for i in directory[-10:]:
			if i[-5] == '1':
				total1+=1
		buy = (total1/10) * (1-sell)
		hold = 1 - sell - buy

	buy2dp = "{:.2f}".format(buy*100)
	sell2dp = "{:.2f}".format(sell*100)
	hold2dp = "{:.2f}".format(hold*100)
	list = [buy2dp, sell2dp, hold2dp]
	return list
