import requests
from pathlib import Path
import zipfile
import os, sys

model_dict = {
    'lfw-subset': '1B5BQUZuJO-paxdN8UclxeHAR1WnR_Tzi',
    '20170131-234652': '0B5MzpY9kBtDVSGM0RmVET2EwVEk',
    '20170216-091149': '0B5MzpY9kBtDVTGZjcWkzT3pldDA',
    '20170512-110547': '0B5MzpY9kBtDVZ2RpVDYwWmxoSUk',
    '20180402-114759': '1EXPBSXwTaqrSC0OhUdXNmKSh9qJUQ55-'
}
CHUNK_SIZE = 32768

model_folder = "./pretrained_models/"
searchengine_folder = "./searchengines/"

if not os.path.exists(model_folder):
    os.makedirs(model_folder)
if not os.path.exists(searchengine_folder):
    os.makedirs(searchengine_folder)

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def download_and_extract_file(model_name, data_dir):
    file_id = model_dict[model_name]
    destination = os.path.join(data_dir, model_name)
    if not os.path.exists(destination):
        destination = destination + '.zip'
        print('Downloading file to %s' % destination)
        download_file_from_google_drive(file_id, destination)
        with zipfile.ZipFile(destination, 'r') as zip_ref:
            print('Extracting file to %s' % data_dir)
            zip_ref.extractall(data_dir)
    else:
        print("%s present" % destination)


def download_file_from_google_drive(file_id, destination):
    URL = "https://drive.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

if __name__ == '__main__':

    print("Downloading pretrained model for MTCNN...")

    for i in range(1, 4):
        f_name = model_folder + '/det{}.npy'.format(i)
        f_path = Path(f_name)
        
        if f_path.is_file():
            print("%s present" % f_name)
        else:
            print("Downloading: ", f_name)
            url = "https://github.com/davidsandberg/facenet/raw/" \
                "e9d4e8eca95829e5607236fa30a0556b40813f62/src/align/det{}.npy".format(i)
            session = requests.Session()
            response = session.get(url, stream=True)

            with open(f_name, "wb") as f:
                for chunk in response.iter_content(CHUNK_SIZE):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)

    download_and_extract_file('20180402-114759', model_folder)

    # Download chromedriver
    dataDir = searchengine_folder 
    filename = dataDir + "/chromedriver_linux64"
    f_path = Path(filename)
    if f_path.is_file():
            print("%s present" % filename)
    else:
        print("Downloading chromedriver")
        url = "https://chromedriver.storage.googleapis.com/81.0.4044.138/chromedriver_linux64.zip"
        session = requests.Session()
        response = session.get(url, stream=True)
        with open(filename + ".zip", "wb") as f:
                for chunk in response.iter_content(CHUNK_SIZE):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
        zippedFile = dataDir + "chromedriver_linux64.zip"       
        with zipfile.ZipFile(zippedFile, 'r') as zip_ref:
            print('Extracting file to %s' % dataDir)
            zip_ref.extractall(dataDir)