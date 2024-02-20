import fitz  
from PIL import Image

pdf_document = fitz.open('sem3.pdf')

page = pdf_document.load_page(0)
pix = page.get_pixmap(alpha = False)    
image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
image.save("output.png")
