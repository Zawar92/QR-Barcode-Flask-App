from flask import Flask, Response,request, render_template, jsonify
import zbar
import numpy as np
import imutils
from sqlalchemy import create_engine
from PIL import Image
import cv2
import pandas as pd
import json
from flask_cors import CORS
import psycopg2
import sys

app = Flask(__name__)
CORS(app)

## pcsir connection -> PostgresSQL
params = "postgresql://zawar:Zawar123@localhost:5432/pcsir"
con = psycopg2.connect(params)
cur = con.cursor()


senddata = ""

@app.route("/")
def component():
	return render_template("component.html")

@app.route('/index', methods=['GET','POST'])
def index():
	return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/index1', methods=['GET','POST'])
def index1():
	return render_template("index1.html")

@app.route('/eg', methods=['GET','POST'])
def eg():
	return render_template("eg.html")

@app.route('/qrbarcode', methods=['GET'])
def get_tasks():
	global senddata
	return jsonify({'tasks': senddata})

@app.route('/getdata', methods=['GET'])
def get_record():
	global senddata
	print(senddata)
	if senddata == None or senddata == "" or senddata ==0 or senddata == '':
		return jsonify("empty")
	else:
		try:
			cur.execute("SELECT * FROM \"barcode\" WHERE \"id\"=(%s)",(senddata,))
			while True:
				row = cur.fetchone()
				jsondata = {"report":[{'id':row[0],
								'name':row[1],
								'location':row[2],
								'Type':row[3]}]}
				return jsonify(jsondata)

		except psycopg2.DatabaseError, e:
			if con:
				con.rollback()


def gen():
	global senddata
	capture = cv2.VideoCapture(0)

	while True:
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		
		ret, frame = capture.read()
		frame=np.array(frame)
		frame = imutils.resize(frame, width=300)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# yield (b'--frame\r\n'b'Content-Type: image/png\r\n\r\n' + jpeg.tobytes() + b'\r\n')
		# Displays the current frame
		# cv2.imshow('Current', frame)

		# Converts image to grayscale.
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
		image = Image.fromarray(gray)
		width, height = image.size
		zbar_image = zbar.Image(width, height, 'Y800', image.tobytes())

		# # Scans the zbar image.
		scanner = zbar.ImageScanner()
		scanner.scan(zbar_image)
		#asdsa
		# Prints data from image.
		for decoded in zbar_image:
			senddata = str(decoded.data)

		for symbol in zbar_image:
			min_x=None
			min_y=None
			max_x=None
			max_y=None
			for point in symbol.location:
				x,y=point
				if(min_x==None):
					min_x=x
				if(min_y==None):
					min_y=y
				if(max_x==None):
					max_x=x
				if(max_y==None):
					max_y=y
				if x < min_x:
					min_x = x
				if x > max_x:
					max_x = x
				if y < min_y:
					min_y = y
				if y > max_y:
					max_y = y
			cv2.rectangle(frame,(int(min_x),int(max_y)),(int(max_x),int(min_y)),(0,255,0),3)
		ret, jpeg = cv2.imencode('.jpg', frame)
		yield (b'--frame\r\n'b'Content-Type: image/png\r\n\r\n' + jpeg.tobytes() + b'\r\n')


if __name__ == "__main__":
	app.run(debug=True)
