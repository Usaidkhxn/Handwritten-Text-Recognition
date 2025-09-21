from flask import Flask, request, render_template, jsonify
from PIL import Image
import pytesseract
import cv2
import numpy as np


app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

def preprocess_image(image_path):
    
    image = cv2.imread(image_path)

    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, thresholded = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

   
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(thresholded, kernel, iterations=1)

    return dilated



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    uploaded_file = request.files['file']

    if uploaded_file:
       
        image_path = 'uploads/uploaded_image.png'

        uploaded_file.save(image_path)
        
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 
        
        
        try:
            image = Image.open(image_path)
            recognized_text = pytesseract.image_to_string(image, lang='hin')
            return jsonify({"result": recognized_text})
        except Exception as e:
            return jsonify({"error": str(e)})

    return jsonify({"error": "No file uploaded"})

if __name__ == '__main__':
    app.run(debug=True)
    







