from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
import subprocess
import os
import signal
from random import randint
from django.contrib import messages
import sys
from .mainbackend import pre, use_model, buysellhold, convertUbyte, tsne6
from django.conf import settings
import shutil
import cv2

CALL_COMMAND = 'exec'
media_root = settings.MEDIA_ROOT.replace('\\', '/')
LOGS_URL = media_root + "/logs/embedding/"  # Logs for TensorBoard
SORTEDGRAPHS_URL0 = media_root + "/sorted-graph-images/0/"
SORTEDGRAPHS_URL1 = media_root + "/sorted-graph-images/1/"

ports_in_use = [8000]
pid_in_use = []


def get_results():
    """ Returns prediction output string to display on results page. """
    d = use_model.categorise_images()
    e = buysellhold.buysellhold()
    return e


def get_visualisation():
    """ Returns TensorBoard visualisation. """
    f = convertUbyte.convert()
    tsne = tsne6.run()
    port = generatePort()
    visualisation = createTensorboardInstance(port)
    return visualisation


def script2(request):
    """ Retrieves the port ID and calls kill port. """
    if request.method == 'GET':
        if not request.user.is_authenticated:
            messages.warning(request,
                            'You must be logged in before you can kill ports.')
            return redirect(reverse('accounts:login'))

    pid_to_kill = request.GET.get('pid', None)
    port_to_kill = request.GET.get('port', None)
    killPort(pid_to_kill, port_to_kill)

    return redirect(reverse('upload:drag_and_drop'))


def killPort(pid_to_kill, port_to_kill):
    """ Kills port with specified port and process ID. """
    if pid_to_kill is not None:
        try:
            # Terminate subprocess on Mac OS
            os.kill(int(pid_to_kill), signal.SIGTERM)
        except PermissionError:
            # Terminate subprocess on Windows
            os.kill(int(pid_to_kill), signal.CTRL_C_EVENT)
        pid_in_use.append(pid_to_kill)

    if port_to_kill in ports_in_use:
        ports_in_use.remove(port_to_kill)


def createTensorboardInstance(port):
    """ Retrieves link to fetch TensorBoard. """
    p = subprocess.Popen(CALL_COMMAND + ' tensorboard --port=' +
                         str(port) + ' --logdir=' + LOGS_URL +
                         ' --host localhost', stdout=subprocess.PIPE,
                         shell=True)
    g = p.pid
    pid_in_use.append(g)

    visualLink = 'http://localhost:%s/#projector&run=.' % port
    killLink = '/tensor/kill-port?pid=%s&port=%s' % (g, port)
    return (visualLink, killLink)


def generatePort():
    """ Generates a random port. """
    port = randint(3081, 9000)
    if port in ports_in_use:
        generatePort()
    else:
        ports_in_use.append(port)

    return port
