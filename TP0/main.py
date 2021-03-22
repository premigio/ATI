from TP0.image import MyImage

sizeDict = {
    'LENA': (256, 256),
    'GIRL': (389, 164),
    'GIRL2': (256, 256),
    'BARCO': (290, 207),
    'FRACTAL': (389, 164),
}

if __name__ == '__main__':
    photo = MyImage('../Photos/LENA.RAW', sizeDict['LENA'])
    photo.image.show()
    new_img = MyImage.threshold(photo.image, 100)
    new_img.show()
