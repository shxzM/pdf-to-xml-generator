from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from PyPDF2 import PdfReader
from lxml import etree
import io

class PDFtoXMLView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file = request.data.get('file')
        if not file:
            return Response({"error": "No file uploaded."}, status=400)
        
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

        # Convert to XML
        root = etree.Element("document")
        etree.SubElement(root, "content").text = text
        xml_str = etree.tostring(root, pretty_print=True, encoding='unicode')

        return Response({"xml": xml_str})


# Create your views here.
