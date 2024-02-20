import fitz
from PIL import Image

# Define the DPI (dots per inch)
dpi = 300  # You can adjust this value as needed

pdf_document = fitz.open('sem3.pdf')

page = pdf_document.load_page(0)

# Create the pixmap with a higher DPI
pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))

# Save the image
image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
image.save("output1.png")