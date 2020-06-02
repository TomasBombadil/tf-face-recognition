from pathlib import Path
import os, sys

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

# this size is required for embedding
FACE_PIC_SIZE = 160

EMBEDDING_SIZE = 512

#PRETREINED_MODEL_DIR = os.path.join(str(Path.home()), 'pretrained_models')

PRETREINED_MODEL_DIR = "/workspace/pretrained_models"

UNKNOWN_CLASS = "unknown"