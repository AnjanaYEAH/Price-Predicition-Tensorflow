from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='formatFilename')
@stringfilter
def formatFileName(name):
    """ Function used in templates to get CSV file name. """
    return name.split('/')[1]
