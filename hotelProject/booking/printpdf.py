# -*- coding: utf-8 -*-
from django.template.loader import get_template

from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.conf import settings
from xhtml2pdf import pisa
from .models import Reservation
try:
    from StringIO import StringIO ## for Python 2
except ImportError:
    from io import StringIO ## for Python 3
from bs4 import BeautifulSoup

def pdf_report_create(request):
    booking = Booking.objects.all()
    # for room in rooms:
    #     print(room.room_image.path)

    template_path = 'pdfReport.html'
    # print(settings.TEMPLATE_DIR)
    context = {
        'datatoshow': booking,
        'hostname': settings.HOSTNAME,

    }
    response = HttpResponse(content_type='application/pdf')


    # response['Content-Disposition'] = 'filename="bookings_report.pdf"'
    # response['Content-Disposition'] = 'attachement;"filename="pdffilename.pdf"'
    response['Content-Disposition'] = '"filename="pdffilename.pdf"'
    template = get_template(template_path)
    html = template.render(context)


    # return HttpResponse('We had some errors <pre>' + html + '</pre>')

    # create a pdf
    # return HttpResponse('We had some errors <pre>' + html + '</pre>')

    pisa_status = pisa.CreatePDF(StringIO(html), dest=response, encoding='UTF-8')
    # pisa_status = pisa.CreatePDF(html.encode('UTF-8'), response, encoding='UTF-8')
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
