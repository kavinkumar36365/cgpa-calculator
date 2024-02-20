import cv2
import pytesseract
import pandas as pd

def perform_ocr_and_extract_details(image_path):
    # Read the table region image
    table_image = cv2.imread(image_path)

    # Perform OCR on the table image
    ocr_text = pytesseract.image_to_string(table_image)
   

    # Split the OCR text into lines
    lines = ocr_text.split('\n')
    return lines

    # Extract details from OCR text
    details = []
    for line in lines:
        if line.strip():  # Ignore empty lines
            details.append(line.split())
   
    # Convert details to DataFrame
    df = pd.DataFrame(details)

    return df

# Example usage
table_df = perform_ocr_and_extract_details("table_region3.png")
print(table_df)