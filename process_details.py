import fitz
from PIL import Image
import cv2
import numpy as np
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import time
import io

class sgpa:
    def __init__(self,pdf_path):
        self.grades=[]
        self.credits=[]
        self.sgpa=0
        self.path= pdf_path
        self.image=None
    
    def pdf_to_image(self):
        # Open the PDF
        pdf_document = fitz.open(self.path)
        # Load the first page
        page = pdf_document.load_page(0)

        dpi=1000
        # Get the pixmap
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
        '''
        #use this for scaling the image

        width_ratio = target_width / image.width
        height_ratio = target_height / image.height

        # Choose the smaller scaling factor to avoid upscaling
        scale_factor = min(width_ratio, height_ratio)

        # Compute the new dimensions
        new_width = int(image.width * scale_factor)
        new_height = int(image.height * scale_factor)

        '''
        # Convert the pixmap to a NumPy array
        img_array = pix.samples

        # Resize the image using PIL's resizing function with antialiasing
        resized_img = Image.frombytes("RGB", [pix.width, pix.height], img_array)

        '''add new_width and new_height to the resize function in place of pix.width and pix.height below if used above in the comments'''
        resized_img = resized_img.resize((pix.width, pix.height), resample=Image.LANCZOS)
        self.image=resized_img
        return
    
    def extract_table(self):

        self.pdf_to_image()
        temp_image = np.array(self.image)
        gray = cv2.cvtColor(temp_image, cv2.COLOR_BGR2GRAY)

        # Apply adaptive thresholding
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        # Remove noise using morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour (presumably the table)
        max_contour = max(contours, key=cv2.contourArea)

        # Get the bounding box of the contour
        x, y, w, h = cv2.boundingRect(max_contour)

        # Extract the table region
        self.image = temp_image[y:y+h, x:x+w]
      
        return
    
    def perform_ocr(self):
        # Convert the image to a stream
        self.extract_table()
        # Convert the image to a stream
        # Convert the bytes object to a file-like object
        is_success, im_buf_arr = cv2.imencode(".jpg", self.image)
        byte_im = im_buf_arr.tobytes()

        image_stream = io.BytesIO(byte_im)
        # Set up the Computer Vision client
        key='7756f8a901bc4fddafb9a66d2bafe7bb'
        endpoint='https://cv-t.cognitiveservices.azure.com/'

        computervision_client=ComputerVisionClient(endpoint,CognitiveServicesCredentials(key))
        #CalltheAPI
        read_response=computervision_client.read_in_stream(image_stream,raw=True)
        #Gettheoperationlocation(URLwithanIDattheend)
        read_operation_location=read_response.headers["Operation-Location"]
        #GrabtheIDfromtheURL
        operation_id=read_operation_location.split("/")[-1]
        #Retrievetheresults
        #retreive the results as json
        read_result=computervision_client.get_read_result(operation_id)
        #checkiftheoperationiscompleted

        while True:
            read_result = computervision_client.get_read_result(operation_id)
            if read_result.status.lower() not in ['notstarted', 'running']:
                break
            time.sleep(1)
        
        
        # Retrieve the results as json
        read_result_json = read_result.as_dict()
        #save as json file
        text=read_result_json['analyze_result']['read_results'][0]['lines']

        for i in text:
            if (((i['bounding_box'][0]>4260 and i['bounding_box'][2]<5300) or i['bounding_box'][0]>5775 and i['bounding_box'][2]<6710)) and (i['bounding_box'][5]>600):
                if (i['bounding_box'][0]>4260 and i['bounding_box'][2]<5300):
                    self.grades.append(int(i['text']))
                else:
                    self.credits.append(int(i['text']))

                if(len(self.credits)>0 and self.credits[len(self.credits)-1]==1):
                    self.credits.pop()
                    self.grades.pop()
        
        return
    
    def calculate_sgpa(self):
        self.total_credits=np.sum(self.credits)
        self.sgpa= (np.matmul(self.grades,np.reshape(self.credits,(len(self.grades),-1)))/self.total_credits)[0]
        return