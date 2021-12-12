from django.conf import settings


COLS = 5   # no. of cols in CSV file to analyse
FREQ = 10  # no. of candlesticks per image
MEDIA_DIR = settings.MEDIA_ROOT.replace('\\', '/') + '/'
