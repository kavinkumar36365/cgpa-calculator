import fitz
from PIL import Image

def resize_with_antialiasing(image, target_width, target_height):
    # Calculate scaling factors
    width_ratio = target_width / image.width
    height_ratio = target_height / image.height

    # Choose the smaller scaling factor to avoid upscaling
    scale_factor = min(width_ratio, height_ratio)

    # Compute the new dimensions
    new_width = int(image.width * scale_factor)
    new_height = int(image.height * scale_factor)

    # Convert the pixmap to a NumPy array
    img_array = image.samples

    # Resize the image using PIL's resizing function with antialiasing
    resized_img = Image.frombytes("RGB", [image.width, image.height], img_array)
    resized_img = resized_img.resize((new_width, new_height), resample=Image.LANCZOS)

    return resized_img

# Open the PDF
pdf_document = fitz.open('sem3.pdf')

# Load the first page
page = pdf_document.load_page(0)
dpi=300
# Get the pixmap
pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))  # Scale up the image by a factor of 2

# Resize the pixmap with antialiasing
resized_img = resize_with_antialiasing(pix, pix.width, pix.height)

# Save the resized image as a PNG file
resized_img.save("output_antialiased.png")
