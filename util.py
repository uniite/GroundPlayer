__author__ = "Jon Botelho"

from django.http import HttpResponse

import os, mimetypes

def send_data(path, filename = None, mimetype = None):

    if filename is None: filename = os.path.basename(path)

    if mimetype is None:
        mimetype, encoding = mimetypes.guess_type(filename)

    response = HttpResponse(mimetype=mimetype)
    response.write(file(path, "rb").read())
    return response

def send_file(path, filename = None, mimetype = None):

    if filename is None: filename = os.path.basename(path)

    if mimetype is None:
        mimetype, encoding = mimetypes.guess_type(filename)

    response = HttpResponse(mimetype=mimetype)
    response['Content-Disposition'] = 'attachment; filename=%s' %filename
    response.write(file(path, "rb").read())
    return response




  