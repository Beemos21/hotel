from django.urls import path
# basic URL config.

from .views import *
# from ..booking.views import *
from . import views

urlpatterns = [
    # path('pdf1/', MyPDF.as_view(template_name='pdfReport.html', filename='my_pdf.pdf'), name='pdf'),

    path('roomAvailabilityReport/', views.roomAvailabilityReportViews, name="roomAvailabilityReport")

    # path('new/', views.newbooking, name="new_booking"),
    # # path('pdf4/', LabelsView.as_view(), name='pdf4'),
]
