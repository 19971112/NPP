# pdfに一括してテキストを入力すr


ローカル環境
```
from PyPDF2 import PdfFileReader

pdf = PdfFileReader("./word_sample.pdf")
import io

from PyPDF2 import PdfFileWriter
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
page = pdf.getPage(0)

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)

font_size = 16
can.setFillColor(Color(0, 0, 0, alpha=1))
can.drawString(
    page.mediaBox.getWidth() / 2,
    page.mediaBox.getHeight() / 2,
    "こんにちは世界！"
)

can.save()
packet.seek(0)
new_pdf = PdfFileReader(packet)
page.mergePage(new_pdf.getPage(0))

output = PdfFileWriter()
output.addPage(page)
with open("word_sample_output.pdf", "wb") as fout:
    output.write(fout)
history
```
