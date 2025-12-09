
import os
from xhtml2pdf import pisa
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import logging

logging.basicConfig(level=logging.INFO)

def test_font(font_name, font_path, index=0):
    print(f"Testing font: {font_name} at {font_path} (idx={index})")
    try:
        # Register Font
        key_name = font_name
        if font_path.lower().endswith('.ttc'):
            pdfmetrics.registerFont(TTFont(key_name, font_path, subfontIndex=index))
        else:
            pdfmetrics.registerFont(TTFont(key_name, font_path))
        
        print(f"  Successfully registered {key_name}")
        
        # Create HTML
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                @font-face {{
                    font-family: 'MyCustomFont';
                    src: url('{font_path}');
                }}
                body {{
                    font-family: '{key_name}', sans-serif;
                }}
            </style>
        </head>
        <body>
            <h1>Test Font: {key_name}</h1>
            <p>你好，世界！This is a test.</p>
            <p><b>Bold Text 测试粗体</b></p>
        </body>
        </html>
        """
        
        fname = f"test_{font_name}.pdf"
        with open(fname, "wb") as f:
            pisa_status = pisa.CreatePDF(html, dest=f, encoding='utf-8')
            
        if pisa_status.err:
            print(f"  Error generating PDF for {font_name}")
        else:
            print(f"  Generated {fname}, please check if it displays rectangles.")
            
    except Exception as e:
        print(f"  Failed to use {font_name}: {e}")

# Test common Windows fonts
fonts_to_test = [
    # name, filename, is_ttc, index
    ('SimHei', 'simhei.ttf', False, 0),
    ('SimSun', 'simsun.ttc', True, 0),
    ('MSYH', 'msyh.ttc', True, 0),
]

font_dir = r"C:\Windows\Fonts"

for name, fname, is_ttc, idx in fonts_to_test:
    path = os.path.join(font_dir, fname)
    if os.path.exists(path):
        test_font(name, path, idx)
    else:
        print(f"Skipping {name}, file not found at {path}")
