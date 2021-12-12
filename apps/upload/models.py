from django.db import models
from .validator import validate_file_extension


class FileUpload(models.Model):

    """  Upload model extends FileField.
         Model fields: name, id, url, uploaded_at. """

    file = models.FileField(upload_to='csv-files/',
                            validators=[validate_file_extension])
    uploaded_at = models.DateField(auto_now_add=True)
