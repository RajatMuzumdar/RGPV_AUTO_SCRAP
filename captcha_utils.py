from PIL import Image
import os
import requests
import time
import pytesseract
import config

def clean_up(dir):
    for file in os.listdir(dir):
        fpath = os.path.join(dir, file)
        os.remove(fpath)
        print(file," removed")

def create_dir(dir):
    parentPath = '.'
    # path = os.path.join(parentPath, dir)
    path = dir
    try:
        os.mkdir(path)
    except FileExistsError:
        clean_up(path)
    except FileNotFoundError:
        print(FileNotFoundError)
    finally:
        return path


def get_string(img_path):

     pytesseract.pytesseract.tesseract_cmd = config.TESS_DRIVER
     result = pytesseract.image_to_string(Image.open(img_path))
     return result

def captcha_decode(captcha_url : str, dirpath : str = ".\\temp"):
    url = captcha_url
    r = requests.get(url)

    filename = 'captchaImage' + str(int(time.time())) + '.jpg'
    fpath = os.path.join(dirpath, filename)

    with open(fpath, 'wb') as out_file:
        out_file.write(r.content)

    return ''.join( get_string(fpath).split() ).upper()[:5]
