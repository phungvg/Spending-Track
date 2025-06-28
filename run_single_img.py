import cv2
import pytesseract
"""For individual test image run, extracting all the text from the image"""

## Defining 
def ocr_core(img):
    text = pytesseract.image_to_string(img)
    return text

##Load image
img = cv2.imread('/Users/panda/Documents/Work/Work_Main/Dataset_collection/Screenshot 2025-06-25 at 14.56.31.png')
text = ocr_core(img)
print(text)

##Get grayscale image(preprocessing and since OCR only cares about black and white)
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

##Remove noise
def remove_noise(image):
    kernal_sz = 5
    return cv2.medianBlur(image, kernal_sz) 

##Thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

img = get_grayscale(img)
img = remove_noise(img)
img = thresholding(img)

## Run
text = ocr_core(img)
print("======================================")
print(text)
print("======================================")

##Display image of what is actually going on (grayscale, noise removed, thresholded)
cv2.imshow("Image", img)
cv2.waitKey(5000) ##Wait for 5000ms (5 seconds)
