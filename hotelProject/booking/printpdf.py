# from __future__ import unicode_literals
# from django.template.loader import get_template
# from django.shortcuts import render, get_object_or_404, redirect
# from django.template import loader
# from django.http import HttpResponse
# from django import template
# from django.conf import settings
# #from xhtml2pdf import pisa
# from .models import *
#
#
# def pdf_report_create(request):
#     booking = Booking.objects.all()
#     # for room in rooms:
#     #     print(room.room_image.path)
#
#     template_path = 'pdfReport.html'
#     # print(settings.TEMPLATE_DIR)
#     context = {
#         'datatoshow': booking,
#         'hostname': settings.HOSTNAME,
#
#     }
#     response = HttpResponse(content_type='application/pdf')
#     # response['Content-Disposition'] = 'filename="bookings_report.pdf"'
#     response['Content-Disposition'] = 'attachement;"filename="pdffilename.pdf"'
#     template = get_template(template_path)
#     html = template.render(context)
#
#     #return HttpResponse('We had some errors <pre>' + html + '</pre>')
#
#     # create a pdf
#     #pisa_status = pisa.CreatePDF(html, dest=response)
#     #if pisa_status.err:
#     #    return HttpResponse('We had some errors <pre>' + html + '</pre>')
#
#     return response
