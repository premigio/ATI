from Algorithms.Thresholding import otsu_thresholding, global_thresholding
from Algorithms.Classes.MyImage import MyImage


def show_global_threshold(my_image: MyImage, window):
    delta_t = window.ask_for_float('Choose a delta value',
                                   default=1.0, min_value=0.0, text='Delta T')
    image, curr_t, iterations = global_thresholding(my_image, delta_t)
    image.image.show()
    return image


def show_otsu_threshold(my_image: MyImage, window):
    image, t = otsu_thresholding(my_image)
    image.image.show()
    return image
