from django.contrib import admin
from django.urls import include, path
# basic URL config.
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import *


urlpatterns = [
		path('pdf2/',  MyPDF.as_view(template_name='pdfReport.html',filename='my_pdf.pdf'), name='pdf'),
		path('pdf4/',  LabelsView.as_view(), name='pdf4'),
	]

