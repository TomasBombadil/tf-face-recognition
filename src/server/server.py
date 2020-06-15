import json
from time import time
import base64

from PIL import Image, ImageDraw
from flask import Flask, request, Response, send_file, flash, redirect, url_for, session
from flask_session import Session

# assuming that script is run from `server` dir
import sys, os, glob
sys.path.append(os.path.realpath('..'))

from tensorface import detection
from tensorface.recognition import recognize, learn_from_examples
from searchengines.download_images_google import getImagesFromGoogle

from werkzeug.utils import secure_filename



# For test examples acquisition
SAVE_DETECT_FILES = False
SAVE_TRAIN_FILES = False
PORT = 5000

app = Flask(__name__)
sess = Session()

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

sess.init_app(app)
UPLOAD_FOLDER = app.root_path + "/../images/to-recognize/"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


Image.MAX_IMAGE_PIXELS = None

def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file: #and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

# for CORS
@app.after_request
def after_request(response):
    #response.headers.add('Access-Control-Allow-Origin', '*')
    #response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    #response.headers.add('Access-Control-Allow-Methods', 'GET,POST')  # Put any other methods you need here
    return response


@app.route('/')
def index():
    indexPath = 'server/static/index.html' #get_script_path() + '/static/index.html'
    html = Response(open(indexPath).read(), mimetype="text/html")
    print("html:")
    print(html)
    return html


@app.route('/detect', methods=['POST'])
def detect():
    try:
        searchFolder = app.root_path + '/images/search-in/'
        getImagesFromGoogle("banderas", searchFolder, app.root_path + "/../searchengines")
        
        images=glob.glob(searchFolder + "/*")
        
        # Set an image confidence threshold value to limit returned data
        threshold = request.form.get('threshold')
        if threshold is None:
            threshold = 0.5
        else:
            threshold = float(threshold)

        for image in images:
            img = Image.open(image)
            #faces = recognize(detection.get_faces(img, threshold))
            
            faces = detection.get_faces(img, threshold)

            if faces:
                for f in faces:
                    x0 = faces[0].x
                    y0 = faces[0].y
                    x1 = faces[0].x + faces[0].w
                    y1 = faces[0].y + faces[0].h
                    print(img)
                    print("x0: %f, y0: %f, x1: %f, y1: %f" % (x0,y0,x1,y1))
                    draw = ImageDraw.Draw(img)
                    draw.rectangle(((x0 , y0), (x1, y1)))
                    img.save(image)
                    print("Image with detected face saved.")
                    img = Image.open(image)
            else:
                print("Face not detected")

        response=""
        for image in images:
            with open(image, "rb") as imageFile:
                imgB64 = base64.b64encode(imageFile.read()) 
            response = response + "," + imgB64.decode("utf-8") 

        return Response(response, mimetype='image/jpeg; charset=utf-8"')

    except Exception as e:
        import traceback
        traceback.print_exc()
        print('POST /detect error:', e)
        return e


@app.route('/train', methods=['POST'])
def train():
    try:
        name = "Model1"
        upload_file()
        images=glob.glob(app.root_path + "/../images/to-recognize/*")
        response=""
        num=1
        for image in images:
            image_sprite = Image.open(image)
            image_sprite = image_sprite.convert('RGB')
            size = 160, 160
            image_sprite = image_sprite.resize(size)
            #image_sprite.thumbnail(size, Image.ANTIALIAS)
            im_resized = image + ".resized"
            image_sprite.save(im_resized, "JPEG")
            size = os.stat(im_resized).st_size
            info = learn_from_examples(name, image_sprite, num, size)
            with open(image, "rb") as imageFile:
                imgB64 = base64.b64encode(imageFile.read())
            response = response + "," + imgB64.decode("utf-8") 
            num=num+1

        return Response(response, mimetype='image/jpeg; charset=utf-8"') 

    except Exception as e:
        import traceback
        traceback.print_exc()
        print('POST /image error: ', e)
        return e


'''if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True) 
    start_debugger()
    #, ssl_context='adhoc')
    # app.run(host='0.0.0.0')
'''
