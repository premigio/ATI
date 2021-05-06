from Algorithms.Noises import *
from Algorithms.Filters.DiffusionFilters import *
from Algorithms.Filters.Filters import bilateral_filter
from GUI.main_window import *


def show_rayleigh(image: MyImage, window):
    if image is None or window is None:
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage('You must select an image first')
        error_dialog.show()
        return
    epsilon = window.ask_for_float('Choose an Epsilon Value',
                                   default=0.5, min_value=0.0, text='epsilon')
    percentage = window.ask_for_float('Choose a percentage Value',
                                      default=30.0, min_value=0.0, max_value=100.0, text='Percentage')
    new_image = rayleigh_multiplicative(image, percentage / 100.0, epsilon)
    new_image.image.show()
    return new_image


def show_gaussian_noise(image: MyImage, window):
    if image is None or window is None:
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage('You must select an image first')
        error_dialog.show()
        return
    mean = window.ask_for_float('Choose a mean',
                                default=20.0, min_value=0.0, text='Mean')
    deviation = window.ask_for_float('Choose a standard deviation',
                                     default=0.5, min_value=0.0, text='Deviation')
    percentage = window.ask_for_float('Choose a percentage Value',
                                      default=30.0, min_value=0.0, max_value=100.0, text='Percentage')
    new_image = gaussian_additive(image, percentage / 100.0, mean, deviation)
    new_image.image.show()
    return new_image


def show_exponential_noise(image: MyImage, window):
    if image is None or window is None:
        return
    lambda_param = window.ask_for_float('Choose a lambda value',
                                        default=20.0, min_value=0.0, text='Lambda')
    percentage = window.ask_for_float('Choose a percentage value',
                                      default=30.0, min_value=0.0, max_value=100.0, text='Percentage')
    new_image = exponential_multiplicative(image, percentage=percentage / 100.0, lambda_param=lambda_param)
    new_image.image.show()
    return new_image


def show_salt_n_pepper_noise(image: MyImage, window):
    if image is None or window is None:
        return
    density = window.ask_for_float('Choose a density value',
                                   default=20.0, min_value=0.0, max_value=100.0, text='Density')
    p0 = window.ask_for_float('Choose a threshold value',
                              default=20.0, min_value=0.0, max_value=100.0, text='p0')
    new_image = salt_n_pepper(image, density / 100.0, p0 / 100.0)
    new_image.image.show()
    return new_image


def show_bilateral_filter(image: MyImage, window):
    if image is None or window is None:
        return
    mask = 0
    while mask % 2 == 0:
        mask = window.ask_for_int('Choose a mask size', default=5, text="mask")

    o_s = window.ask_for_float('Choose a sigma s value',
                               default=2.0, min_value=0.0, max_value=100.0, text='o_s')

    o_r = window.ask_for_float('Choose a sigma r value',
                               default=30.0, min_value=0.0, max_value=100.0, text='o_r')

    new_image = bilateral_filter(image, mask, o_s, o_r)
    new_image.image.show()
    return new_image


def __diffusion_filter_aux(image: MyImage, window, which):
    if image is None or window is None:
        return

    iterations = window.ask_for_int('Choose the number of iterations', default=50, text='iterations')  # 50
    sigma = window.ask_for_float('Choose a sigma value',
                                 default=5.0, min_value=0.0, max_value=100.0, text='iterations')

    func_detec = FunctionDiff.LECLERC if which else FunctionDiff.ISOTROPIC

    fin = anisotropic(image, func_detec, sigma, iterations)
    fin.show()
    return fin


def show_anisotropic_filter(image: MyImage, window):
    return __diffusion_filter_aux(image, window, True)


def show_isotropic_filter(image: MyImage, window):
    return __diffusion_filter_aux(image, window, False)
