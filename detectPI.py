'''
Version 1
Designed by Ansh Shah, Thomas Hale, and Karthik Pullela
'''

import cv2
import pytesseract
from googletrans import Translator
from time import sleep
from picamera import PiCamera

pytesseract.pytesseract.tesseract_cmd = 'Path/To/Tesseract' # TODO: Change to path

# Declaring translator and Camera objects
translator = Translator()
camera = PiCamera()

# Using picamera, take and store a jpg for use later
camera.start_preview()
sleep(2)
camera.capture('/home/pi/Desktop/input.jpg')
camera.stop_preview()

# Open previously mentioned image for text detection
img = cv2.imread('/home/pi/Desktop/input.jpg')

# Converting image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# OTSU threshold
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)


rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (70, 70))

# Applying dilation
dilation = cv2.dilate(thresh1, rect_kernel, iterations = 3)

# Finding contours
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
												cv2.CHAIN_APPROX_NONE)
im2 = img.copy()

# A blank text file is made
file = open("recognized.txt", "w+")
file.write("")
file.close()

# Looping through the identified contours
# Then rectangular part is cropped and passed on
# to pytesseract for extracting text from it
# Extracted text is then written into the text file
for cnt in contours:
	x, y, w, h = cv2.boundingRect(cnt)
	
	# Drawing a rectangle on image
	rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
	
	# Cropping the text block for giving input to OCR
	cropped = im2[y:y + h, x:x + w]
	
	# Open the file to append
	file = open("recognized.txt", "a")
	
	# Apply OCR on the cropped image
	text = pytesseract.image_to_string(cropped)
	
	# Translating and appending the text into file
	file.write(translator.translate(text, dest='en', src='es').text)
	file.write("\n")
	file.close
