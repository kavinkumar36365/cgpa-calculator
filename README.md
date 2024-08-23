# CGPA Calculator

## Overview
This project is a Python-based CGPA calculator that processes PDF documents of student grade reports, extracts relevant data using Optical Character Recognition (OCR), and calculates the SGPA (Semester Grade Point Average) for each semester. The tool also checks for any arrears and computes the CGPA (Cumulative Grade Point Average) based on the extracted grades and credits.

## Features
- **PDF to Image Conversion:** Converts PDF files to images for easier processing.
- **OCR for Data Extraction:** Utilizes Azure's Computer Vision API to extract grades and credits from the grade report images.
- **SGPA Calculation:** Calculates the SGPA for each semester by processing the grades and credits.
- **Arrear Detection:** Checks for any arrears and adjusts the SGPA accordingly.

## Files
- **`process_details.py`**: Contains the `sgpa` class, which handles the core functionality including PDF processing, OCR, and SGPA calculation.
- **`test.py`**: A script to test the CGPA calculator across multiple semesters, processing PDFs for each semester and calculating the overall CGPA.

## Dependencies
- `fitz` (PyMuPDF)
- `PIL` (Pillow)
- `cv2` (OpenCV)
- `numpy`
- `azure.cognitiveservices.vision.computervision`
- `msrest`

## Usage
1. Ensure all dependencies are installed.
2. Place your semester PDF files in the project directory.
3. Run `test.py` to process the PDFs and calculate the CGPA.

