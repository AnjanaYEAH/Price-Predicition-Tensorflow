from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class CorsMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        print('test')
        response['Access-Control-Allow-Origin'] = '*'
        print(response['Access-Control-Allow-Origin'])
        return response
