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
        print("Received file:", file)
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

                words = page.extract_words(extra_attrs=["size", "top", "x0", "x1"])
                lines = {}
                for word in words:
                    top = round(word['top'])  # Group words with similar vertical position
                    line = lines.get(top, [])
                    line.append(word)
                    lines[top] = line

                for top in sorted(lines.keys()):
                    
                    line_words = sorted(lines[top], key=lambda w: w['x0'])
                    line_text = ''
                    prev_x1 = None

                    for word in line_words:
                        if prev_x1 is not None and word['x0'] - prev_x1 > 3:  # threshold to detect space (tune this)
                            line_text += ' '  # add space between words
                        line_text += word['text']
                        prev_x1 = word['x1']
                    
                    # Determine if this line is a heading based on average font size
                    avg_font_size = sum([float(w.get('size', 0)) for w in line_words]) / len(line_words)
                    
                    if avg_font_size > 16:  # Example threshold for heading detection
                        heading_elem = etree.SubElement(page_elem, "heading")
                        heading_elem.text = line_text
                    else:
                        line_elem = etree.SubElement(page_elem, "line")
                        line_elem.text = line_text

                
        # Generate XML string
        xml_str = etree.tostring(root, pretty_print=True, encoding='unicode')
        return Response({"xml": xml_str})


# Create your views here.
