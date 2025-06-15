from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from PyPDF2 import PdfReader
from lxml import etree
import io
import pdfplumber

class PDFtoXMLView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file = request.data.get('file')
        if not file:
            return Response({"error": "No file uploaded."}, status=400)

        root = etree.Element("document")

        with pdfplumber.open(file) as pdf:
            for page_number, page in enumerate(pdf.pages):
                page_elem = etree.SubElement(root, "page", number=str(page_number + 1))

                # Extract Tables
                tables = page.extract_tables()
                for table_idx, table in enumerate(tables):
                    table_elem = etree.SubElement(page_elem, "table", index=str(table_idx + 1))
                    for row in table:
                        row_elem = etree.SubElement(table_elem, "row")
                        for cell in row:
                            cell_elem = etree.SubElement(row_elem, "cell")
                            cell_elem.text = str(cell) if cell else ""

                # Extract Text with Heading Detection
                words = page.extract_words(use_text_flow=True, keep_blank_chars=False, extra_attrs=["size"])
                for word in words:
                    font_size = word.get('size', 0)
                    text = word.get('text', '').strip()

                    if not text:
                        continue

                    try:
                        font_size = float(font_size)
                    except (TypeError, ValueError):
                        font_size = 0

                    # Heuristic: Consider font sizes >12 as headings (adjust as needed)
                    if font_size > 12:
                        heading_elem = etree.SubElement(page_elem, "heading")
                        heading_elem.text = text
                    else:
                        line_elem = etree.SubElement(page_elem, "line")
                        line_elem.text = text

        # Generate XML string
        xml_str = etree.tostring(root, pretty_print=True, encoding='unicode')
        return Response({"xml": xml_str})


# Create your views here.
