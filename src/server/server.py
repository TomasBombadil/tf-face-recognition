import json
from time import time
import base64

from PIL import Image
from flask import Flask, request, Response, send_file

from tensorface import detection
from tensorface.recognition import recognize, learn_from_examples

# assuming that script is run from `server` dir
import sys, os
sys.path.append(os.path.realpath('..'))


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
    indexPath = 'static/index.html' #get_script_path() + '/static/index.html'
    html = Response(open(indexPath).read(), mimetype="text/html")
    print("html:")
    print(html)
    return html


@app.route('/detect', methods=['POST'])
def detect():
    try:
        image_stream = request.files['image']  # get the image
        image = Image.open(image_stream)

        # Set an image confidence threshold value to limit returned data
        threshold = request.form.get('threshold')
        if threshold is None:
            threshold = 0.5
        else:
            threshold = float(threshold)

        faces = recognize(detection.get_faces(image, threshold))

        j = json.dumps([f.data() for f in faces])
        print("Result:", j)

        # save files
        if SAVE_DETECT_FILES and len(faces):
            id = time()
            with open('test_{}.json'.format(id), 'w') as f:
                f.write(j)

            image.save('test_{}.png'.format(id))
            for i, f in enumerate(faces):
                f.img.save('face_{}_{}.png'.format(id, i))

        return j

    except Exception as e:
        import traceback
        traceback.print_exc()
        print('POST /detect error: %e' % e)
        return e


@app.route('/train', methods=['POST'])
def train():
    try:
        # image with sprites
        #image_stream = request.files['image']  # get the image
        #image_sprite = Image.open(image_stream)
        '''
        image_sprite = Image.open(filepath)

        # forms data
        name = request.form.get('name')
        num = int(request.form.get('num'))
        size = int(request.form.get('size'))

        # save for debug purposes
        if SAVE_TRAIN_FILES:
            image_sprite.save('train_{}_{}_{}.png'.format(name, size, num))

        info = learn_from_examples(name, image_sprite, num, size)
        #return json.dumps([{'name': n, 'train_examples': s} for n, s in info.items()])
        '''
        filepath = "./images/to-recognize/Antonio-Banderas-1.jpg"
        with open(filepath, "rb") as imageFile:
            imgB64 = base64.b64encode(imageFile.read())

        return send_file(imgB64.decode("utf-8") , mimetype='image/jpeg')

    except Exception as x:
        import traceback
        traceback.print_exc()
        print('POST /image error: %e' % e)
        return e


'''if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True) 
    start_debugger()
    #, ssl_context='adhoc')
    # app.run(host='0.0.0.0')
'''
