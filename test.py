import zbar
import numpy as np
import imutils
from PIL import Image
import cv2





if __name__ == "__main__":
	im=cv2.imread('static/images/bc.jpg')


	cam=0
	cap=cv2.VideoCapture(cam)

	while True:
		ret,frame=cap.read()
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
		for symbol in zbar_image:
			print str(symbol.data)
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
		cv2.imshow("Result",frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	cap.release()
	cv2.destroyAllWindows()