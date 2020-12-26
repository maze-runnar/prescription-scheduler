from flask import Flask, render_template,request, url_for
from flask import jsonify
import os
import requests
from bs4 import BeautifulSoup

from PIL import Image
import pytesseract
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class



app = Flask(__name__)

#print(os.chdir("static"))

app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + "/extra/ocr/static/"
app.config['UPLOADED_FILES_ALLOW'] = {"png", "jpg", "jpeg"}
app.config['UPLOADED_FILES_DENY'] = {"pdf"}


photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>Photo Upload</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=photo>
         <input type=submit value=Upload>
    </form>
    '''





@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST' and 'photo' in request.files:
		filename = photos.save(request.files['photo'])
		file_url = photos.url(filename)
		print(file_url)
		print(os.getcwd() + "/extra/ocr/static/" + filename)
		im = Image.open(os.getcwd() + "/extra/ocr/static/" + filename)
		text = pytesseract.image_to_string(im, lang = 'eng')
		print(text)
		return html + '<br><img src=' + file_url + '>' + '<br><br>' + '<textarea rows="10" cols="50">' + text + '</textarea>' 
	return html

if __name__ == "__main__":
    app.run(debug=True)
