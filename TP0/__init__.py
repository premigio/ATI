from TP0.image import MyImage

sizeDict = {
    'LENA': (256, 256),
    'GIRL': (389, 164),
    'GIRL2': (256, 256),
    'BARCO': (290, 207),
    'FRACTAL': (389, 164),
}

# lena = MyImage.load_image('/Users/pedroremigiopingarilho/Desktop/ITBA/ATI/ATI/Photos/LENA.RAW', sizeDict['LENA'])
# lena2 = MyImage.load_image('/Users/pedroremigiopingarilho/Desktop/ITBA/ATI/ATI/Photos/Lenaclor.pbm')  # .show()
#
# print(MyImage.get_pixel(lena2, (100, 200)))

photo = MyImage('../Photos/LENA.RAW', sizeDict['LENA'])
photo2 = MyImage('../Photos/GIRL.RAW', sizeDict['GIRL'])

a = MyImage.create_circle_image(sizeDict['GIRL'])

photo.copy(photo2.image, (0, 0), a.resize(sizeDict['GIRL'])).show()