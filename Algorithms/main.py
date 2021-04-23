from Algorithms.Umbralization import global_thresholding, otsu_thresholding
from Algorithms.Utils import *
from Algorithms.DiffusionFilters import *
from Algorithms.BorderDetection import *
from Classes.MyImage import MyImage

sizeDict = {
    'LENA': (256, 256),
    'GIRL': (389, 164),
    'GIRL2': (256, 256),
    'BARCO': (290, 207),
    'FRACTAL': (389, 164),
}

if __name__ == '__main__':
    lena_photo = MyImage('../Photos/LENA.RAW', sizeDict['LENA'])
    lena_color = MyImage('../Photos/Lenaclor.pbm')
    yo = MyImage('/Users/jimenalozano/Desktop/yo.jpg', (340, 256))

    # laplacian_mask = [[0, -1, 0],
    #                   [-1, 4, -1],
    #                   [0, -1, 0]]
    #
    # laplacian_mask = np.array(laplacian_mask)
    #
    # sigma = 1
    # log_mask = log_mask(sigma, sigma * 6 + 1)
    #
    # a = laplacian_edge_detector(lena_photo, log_mask)
    # a.image.show()

    # image, curr_t, iterations = global_thresholding(lena_photo, 1)
    # print(iterations)
    # print(curr_t)
    # image.image.show()

    image, t = otsu_thresholding(lena_color)
    print(t)
    image.image.show()
