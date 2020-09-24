from flask import Flask,render_template,request
from werkzeug import secure_filename
import cv2
from PIL import Image
import pytesseract
import os
import re
import joblib

pytesseract.pytesseract.tesseract_cmd='C://Program Files/Tesseract-OCR/tesseract.exe'


app=Flask(__name__)

@app.route('/')
def index():

	return render_template('sideeffect.html')

@app.route('/prediction',methods=['POST', 'GET'])
def prediction():

	diseases={0:"neurofibromatosis",1:"carcinoma syndrome",2:"von Hippel-Lindau",3:"Glioblastoma multiforme",4:"tuberous sclerosis"}
	
	input_data = request.form 
	
	firstname=input_data['First Name']
	lastname=input_data['Last Name']
	age=input_data['Age']
	gender=input_data['Gender']
	email=input_data['E-mail']

	f = request.files['Upload Report']
	f.save(secure_filename(f.filename))

	image=cv2.imread(f.filename)

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	thresh = cv2.threshold(gray,140, 255,cv2.THRESH_BINARY)[1]
	#thresh = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

	text = pytesseract.image_to_string(thresh)

	
	numbers=re.findall(r"[-+]?\d*\.\d+|\d+",text)
	Hemoglobin         =numbers[3]
	RED BLOOD CELLS    =numbers[4]
	WHITE BLOOD CELLS  =numbers[]
	NEUTROPHILS        =numbers[17]
	LYMPHOCYTES        =numbers[15]

	if(gender=='male'):

		model=joblib.load('male-test1.sav')
	else:
		model=joblib.load('female.sav')

	result=model.predict([[himo,rbc,wbc,lym,neu]])

	disease=diseases[result]

	return render_template('result.html',disease=disease)

	#{{disease}}

app.run(debug=True)