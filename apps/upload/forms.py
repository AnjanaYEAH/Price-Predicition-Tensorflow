from django import forms
from .models import FileUpload


class UploadForm(forms.ModelForm):

    """ Form to handle CSV file uploads. Uploads are cleaned and validated. """

    class Meta:

        """ Information about the form. """

        model = FileUpload
        fields = ('file', )  # store as tuple

    def clean(self):
        """ Cleans upload and checks if filename already exists. """

        f = str(self.cleaned_data.get('file')).strip()
        for v in FileUpload.objects.all():
            s = str(v.file).partition('/')[2]
            if f == s.strip():
                raise forms.ValidationError('Filename already exists.')
