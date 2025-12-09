
from xhtml2pdf import pisa
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

print("Testing xhtml2pdf...")
try:
    font_path = r'C:\Windows\Fonts\simhei.ttf'
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('SimHei', font_path))
        print(f"Registered font: {font_path}")
    else:
        print("Font not found!")

    html = """
    <html>
    <head>
    <style>
        body { font-family: SimHei; }
    </style>
    </head>
    <body>
        <h1>Hello World</h1>
        <p>你好，世界</p>
    </body>
    </html>
    """
    
    with open('test_output.pdf', 'wb') as f:
        pisa_status = pisa.CreatePDF(html, dest=f)
    
    if pisa_status.err:
        print("Error generation PDF")
    else:
        print("PDF generated successfully: test_output.pdf")

except Exception as e:
    print(f"Failed: {e}")
