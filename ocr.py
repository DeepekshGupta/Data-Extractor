import pytesseract as tess
# tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image
import sys

path = sys.argv[1]

img = Image.open(path)
text = tess.image_to_string(img, config=' --psm 1')
# print(type(img))
print(text)
