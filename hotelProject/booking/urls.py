from django.urls import path
from django.http import HttpResponse,HttpRequest
from wkhtmltopdf.views import PDFTemplateView
from .views import MyPDF,customers
from . import printpdf
from . import views
from roomManager.views import GetRoom
# from django.conf.urls import url

from modernrpc.views import RPCEntryPoint

urlpatterns = [
    path('', printpdf.pdf_report_create, name='create-pdf'),
    path('pdf1', PDFTemplateView.as_view(template_name='pdfReport.html',
                                           filename='my_pdf.pdf'), name='pdf'),



    path('pdf2',  MyPDF.as_view(template_name='pdfReport.html'), name='pdf'),

    path('pdf3',  GetRoom.as_view(template_name='pdfRoom.html'), name='pdf'),

    path('rpc/', RPCEntryPoint.as_view()),
    path('customers/', views.customers),
    path('new/', views.newbooking,name="new_booking"),
    # path('searchforroom/', views.searchforroom,name="searchforroom"),
    path('search/<int:city>/<int:roomtype>/<str:checkin>/<str:checkout>',views.searchbooking,name='search_booking'),
]