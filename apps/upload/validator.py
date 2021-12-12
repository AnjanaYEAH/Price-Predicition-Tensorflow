def validate_file_extension(value):
    """ Ensures uploaded file is a CSV file. """
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    if not ext.lower() == ".csv":
        print("Incorret file upload")
        raise ValidationError(u'Unsupported file extension.')
