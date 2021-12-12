import pandas as pd
from datetime import datetime
from itertools import count
import matplotlib
matplotlib.use('TkAgg')   # required for some OS
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ohlc as candlestick
from django.core.files.storage import default_storage
from shutil import rmtree
import io
import os
from .constant import *


allData = 0   # Entire CSV file stored here
subset = 0    # Each 10-minute subset for graphing stored here


def getImageName(fromT, toT):
    """ Join two datetime arguments and return their string. """

    format = '%d-%m-%Y_%H-%M'
    return fromT.strftime(format) + '__' + toT.strftime(format)


def getLabel(before, after):
    """ Label each image:
        1: The stock is increasing.
        0: The stock is decreasing. """

    prefix = '__'
    if before < after:
        prefix += '1'
    else:
        prefix += '0'
    return prefix


def graph(data, savePath):
    """ Graphs and saves candlesticks as image files.
        :param data: pd.DataFrame object of a csv file
        :return: void """

    (fig, ax) = plt.subplots()
    for n in count(0, FREQ):
        subset = data[n:n + FREQ]
        plt.axis('off')
        plt.subplots_adjust(
            left=0,
            bottom=0,
            right=1,
            top=1,
            wspace=0,
            hspace=0,
            )
        if len(subset) == 10:
            candlestick(
                ax,
                subset['Open'],
                subset['High'],
                subset['Low'],
                subset['Close'],
                width=0.8,
                colorup='yellow',
                colordown='black',
                alpha=1,
                )
            try:
                imgFileName = getImageName(subset.iloc[0, 0],
                        subset.iloc[-1, 0]) + getLabel(subset.iloc[9,
                        4], data.iloc[n + FREQ + 9, 4])
            except IndexError:
                break
            except AttributeError:
                raise ValueError('Incorrect date-time format.')

            fig.savefig('{}/{}.png'.format(savePath, imgFileName))
            ax.clear()
        else:
            break


def readFile(fileName):
    """ Reads csv file into a DataFrame object.
        :param fileName: address to csv file
        :return: pd.DataFrame object of the csv file """

    colNames = [
        'Date',
        'Time',
        'Open',
        'High',
        'Low',
        'Close',
        ]
    return pd.read_csv(
        fileName,
        header=0,
        names=colNames,
        usecols=colNames,
        parse_dates={'Datetime': ['Date', 'Time']},
        infer_datetime_format=True,
        )


def cleanImageStorage():
    """ Removes folder where graph-images are saved. """
    try:
        rmtree(MEDIA_DIR + 'graph-images')
    except FileNotFoundError:
        pass


def main(url):
    """ Main function controller:
        1. Prepares directories
        2. Manipulates data with pandas
        3. Generates and saves candlestick images """
    cleanImageStorage()
    filePath = MEDIA_DIR + url
    imagePath = default_storage.path('graph-images')
    if not default_storage.exists('graph-images'):
        os.mkdir(imagePath)

    allData = readFile(filePath)
    print (type(allData), type(imagePath))
    graph(allData, imagePath)
