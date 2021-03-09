from PIL import Image


def load_image(path: str, raw_prop: (int, int) = (256, 256)):
    if path is None:
        return
    extension = path.split('.')[-1]
    if extension.lower() == 'raw':
        file = open(path, "rb")
        img = Image.frombytes(mode="L", size=raw_prop, data=file.read())  # mode=L es 8-bit pixels, black and white
    else:
        img = Image.open(path)
    return img


def save_image(image: Image, path: str):
    if image is None:
        print("image is None")
        return
    image.save(path)


def get_pixel(image: Image, pos: (int, int)):
    pass


def modify_pixel(image, pos, new_pixel):
    pass


def copy(image1, image2):
    pass


sizeDict = {
    'LENA': (256, 256),
    'GIRL': (389, 164),
    'GIRL2': (256, 256),
    'BARCO': (290, 207),
    'FRACTAL': (389, 164),
}

# TP0
# Ejercicio 1.1
load_image('/Users/pedroremigiopingarilho/Desktop/ITBA/ATI/ATI/Photos/LENA.RAW', sizeDict['LENA']).show()
load_image('/Users/pedroremigiopingarilho/Desktop/ITBA/ATI/ATI/Photos/Lenaclor.pbm').show()
