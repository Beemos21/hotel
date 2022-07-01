from .models import *
from django.conf import settings

from wkhtmltopdf.views import PDFTemplateView

from roomManager.views import *
from django.views.generic import TemplateView
from django_renderpdf.views import PDFView

from django.contrib.auth.mixins import LoginRequiredMixin
from roomManager.models import *


# Create your views here.

class MyPDF(PDFTemplateView):
    def get_context_data(self, **kwargs):
        context = super(MyPDF, self).get_context_data(**kwargs)
        booking = Reservation.objects.all()
        context = {
            'datatoshow': booking,
            'hostname': settings.HOSTNAME,
        }
        return context


class AboutView(TemplateView):
    template_name = "about.html"


class PromptDownloadView(PDFView):
    # template_path = 'pdfReport.html'
    # template_name = get_template(template_path)
    template_name = 'pdfReport.html'
    prompt_download = True
    download_name = "myfile.pdf"


class LabelsView(LoginRequiredMixin, PDFView):
    """Generate labels for some Shipments.

    A PDFView behaves pretty much like a TemplateView, so you can treat it as such.
    """
    template_name = 'pdfReport.html'

    # template_name = 'test.html'

    def get_context_data(self, *args, **kwargs):
        """Pass some extra context to the template."""
        context = super().get_context_data(*args, **kwargs)
        # booking = Booking.objects.all()

        context['booking'] = Reservation.objects.all()

        return context


def demodatabooking(request):
    pass
