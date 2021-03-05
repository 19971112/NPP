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

file = "./word_sample.pdf"
pdf = PdfFileReader(file)

box = ["B1","B2","B3","B4","B5","B6","B7","B8","B9","B10","B11","B12","B13","B14","B15","B16","B17","B18","B19","B20","B21","B22","B23","B24","B25","B26","M1","M2","M3","M4","M5","M6","M7","M8","M9","M10","M11","M12","M13","M14","M15","M16","M17","M18","M19","M20","M21","M22","M23","MB1","MB2","MB3","MB4","MB5","MB6","MB7","MB8","MB9","MB10","MB11","MB12","MB13","MB14","MB15"]
box = ["B1"]

page_count = 0


for each_page in box:
  
    
    page = pdf.getPage(page_count)
    
    input_txt = box[page_count]
    print(each_page,page_count,input_txt)
    
    page_count = page_count + 1

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)

    font_size = 20
    can.setFont('Helvetica', font_size)
    can.setFillColor(Color(0, 0, 0, alpha=1))
    can.drawString(15,700,input_txt)

    can.save()
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    page.mergePage(new_pdf.getPage(0))

    output = PdfFileWriter()
    output.addPage(page)
    output_file_name = str(page_count) + '_' + each_page + '.pdf'
    with open(output_file_name, "wb") as fout:
        output.write(fout)
