from django.shortcuts import render, redirect, get_object_or_404  # used to render templates
from django.views.generic.edit import DeleteView
from django.http import JsonResponse, HttpResponse
from django.views import View
import json
from django.urls import reverse
from .forms import UploadForm
from .models import FileUpload
from django.contrib import messages
from .python.candlestick_images import main as generateImages
from apps.tensor import views as tf


class UploadView(View):

    """ Handles GET/POST requests for the upload page. """

    def get(self, request):
        if not self.request.user.is_authenticated:
            messages.warning(request,
                             'You must log in before you can access the app.'
                             )
            return redirect(reverse('accounts:login'))

        # List of CSV files to display in table for re-analysis

        files_list = FileUpload.objects.all()
        return render(self.request, 'upload/upload.html',
                      {'csv_files': files_list})

    def post(self, request):
        if request.is_ajax():
            try:

                # Only reuploadedfiles are decoded and need to be decoded

                reuploadedFile = json.loads(request.body.decode('utf-8'
                        ))['fileName']
            except:

                # Newly uploaded file

                reuploadedFile = None

            if reuploadedFile:
                data = {'name': reuploadedFile}
                try:
                    generateImages(reuploadedFile)
                except Exception as e:
                    data['error'] = e.args[0]
                return JsonResponse(data)

        form = UploadForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            csv_file = form.save()
            data = {
                'is_valid': True,
                'name': csv_file.file.name,
                'url': csv_file.file.url,
                'date': csv_file.uploaded_at,
                'id': csv_file.id,
                }

            filePath = csv_file.file.url
            try:
                generateImages(filePath[7:])
            except Exception as e:

                # Error with image generation, so faulty file: delete it

                FileUpload.objects.get(id=csv_file.id).delete()
                return JsonResponse({'is_valid': False,
                                    'file_error': e.args[0]})
        else:
            data = {'is_valid': False,
                    'form_error': form.errors.as_json()}
        return JsonResponse(data)


class FileDelete(DeleteView):

    """ Handling requests when a user wishes to delete a file. """

    template_name = 'upload/delete.html'

    def dispatch(self, *args, **kwargs):
        """ Function to handle redirects if the user isn't logged in. """

        if not self.request.user.is_authenticated:
            return redirect(reverse('accounts:login'))
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        """ Get id of CSV file to be deleted. """

        id_ = self.kwargs.get('id')
        return get_object_or_404(FileUpload, id=id_)

    def get_success_url(self):
        """ If deleted successfully, go to the upload page. """

        return reverse('upload:drag_and_drop')


class GraphView(View):

    """ Handling requests for the results page. """

    def get(self, request, csv_name):
        """ Redirects the user to the appropriate page. """

        if not self.request.user.is_authenticated:
            messages.warning(request,
                             'You must log in before you can access the app.'
                             )
            return redirect(reverse('accounts:login'))
        return render(self.request, 'upload/graph.html',
                      {'fileName': csv_name})

    def post(self, request, csv_name):
        """ Handles request from JS script that says when the page is ready. """

        data = {}
        if request.is_ajax():

            # If page is ready, automatically run TensorFlow backend

            try:
                pageReady = json.loads(request.body.decode('utf-8'
                        ))['ready']
            except:
                pageReady = 'no'
            if pageReady == 'yes':
                (buy, sell, hold) = tf.get_results()
                (visualisationLink, killLink) = tf.get_visualisation()

                data = {
                    'buy': buy,
                    'sell': sell,
                    'hold': hold,
                    'visualiseLink': visualisationLink,
                    'killLink': killLink,
                    }

            return JsonResponse(data)

        return render(self.request, 'upload/graph.html')
