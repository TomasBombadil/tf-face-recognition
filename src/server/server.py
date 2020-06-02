import json
from time import time
import base64

from PIL import Image
from flask import Flask, request, Response, send_file

# assuming that script is run from `server` dir
import sys, os
sys.path.append(os.path.realpath('..'))

from tensorface import detection
from tensorface.recognition import recognize, learn_from_examples
from searchengines import download_images_google

# For test examples acquisition
SAVE_DETECT_FILES = False
SAVE_TRAIN_FILES = False
PORT = 5000

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

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
        searchFolder = get_script_path() + '/images/search-in/'
        getImagesFromGoogle("banderas", searchFolder)
        
        images=glob.glob(searchFolder + "/*")
        for image in images:
            img = Image.open(image)
            imgB64 = base64.b64encode(img.read())
            return Response(imgB64.decode("utf-8"), mimetype='image/jpeg; charset=utf-8"') 

    except Exception as e:
        import traceback
        traceback.print_exc()
        print('POST /detect error: %e' % e)
        return e


@app.route('/train', methods=['POST'])
def train():
    try:
        filepath = "./images/to-recognize/Antonio-Banderas-1.jpg"
        with open(filepath, "rb") as imageFile:
            imgB64 = base64.b64encode(imageFile.read())

        return Response(imgB64.decode("utf-8"), mimetype='image/jpeg; charset=utf-8"') 
        #return send_file(imgB64.decode("utf-8") , mimetype='image/jpeg')

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
