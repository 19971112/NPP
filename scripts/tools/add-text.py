import random
import io
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from natsort import natsorted


pdfmetrics.registerFont(
    TTFont(
        'HelveticaHelvetica',
        '/System/Library/Fonts/HelveticaNeue.ttc'
    )
)

file = "./20210305_nanopore_tax-barplot.pdf"
pdf = PdfFileReader(file)

box = ["BF_05","BF_06","BF_07","BF_08","BF_09","BF_10","BF_11","BF_12","BF_14","BF_15","BF_16","BF_17","BF_18","BF_19","BF_20","BF_23","BF_24","BF_29","BF_34","BF_38","BF_39","BF_40"]

page_count = 0


for each_page in box:
    page = pdf.getPage(page_count)
    
    input_txt = box[page_count]
    print(each_page,page_count,input_txt)
    
    page_count = page_count + 1

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)

    font_size = 25
    can.setFont('Helvetica', font_size)
    can.setFillColor(Color(0, 0, 0, alpha=1))
    can.drawString(500,810,input_txt)

    can.save()
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    page.mergePage(new_pdf.getPage(0))

    output = PdfFileWriter()
    output.addPage(page)
    output_file_name = str(page_count) + '_' + each_page + '.pdf'
    with open(output_file_name, "wb") as fout:
        output.write(fout)
