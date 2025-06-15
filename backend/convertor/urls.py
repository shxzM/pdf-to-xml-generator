from django.urls import path
from .views import PDFtoXMLView

urlpatterns = [
    path('convert/', PDFtoXMLView.as_view(), name='pdf_to_xml'),
]
