# La idea: una esquina puede reconocerse observando los puntos en un entorno (observando la variación de un entorno)
# Haciendo un corrimiento en cualquier dirección, debería ocurrir un cambio abrupto
# Siempre en un punto de borde la variación se da en la dirección ortogonal al borde, pero con una esquina hay cambios
# en todas las direcciones.
# Región flat --> no hay cambios en ninguna dirección
# Borde --> no hay cambios en algunas de las direcciones
# Esquina --> hay cambios significativos en todas las direcciones
# Aporte de Harris: calcular los autovalores y autovectores de la matrix 2x2 para cada píxel tiene un costo
# computacional muy alto (sobre t0do para la época, 1980), entonces se dio cuenta que, como el determinante es el
# producto de los autovalores, y la traza es la suma de los autovalores, se pueden calcular mucho más fácilmente
# la traza y el determinante de la matriz. Entonces, la energía de Moravec la escribe como:
# R = det(M) - k * traza(M)^2
# R = λ1 * λ2 - k * (λ1 + λ2)^2
# Mirando las curvas de nivel:
# Si R < 0 ---> punto de borde
# Si R > umbral ---> punto de esquina (cuanto mayor es el umbral, más marcada está la esquina)
# Si R = 0 ---> región flat
# Algoritmo:
# En los primeros 3 pasos calculamos la energía del corrimiento, utilizando la traza y el determinante.
# El corrimiento lo calculamos con las derivadas (diferencias finitas) respecto de x y de y con Prewitt o Sobel.
# 1.    Calcular Ix e Iy usando las máscaras de Prewitt o Sobel para cada pixel de la imagen.
# 2.    Calcular Ix2 elevando Ix^2 elemento a elemento y aplicar un filtro gaussiano para suavizar,
#       por ejemplo, de 7x7 con σ = 2. Lo mismo Iy2.
# 3.    Calcular Ixy multiplicando elemento a elemento también suavizando con el mismo filtro gaussiano.
# Ya tengo Ix2, Iy2 e Ixy --> tengo la matriz M
# 4. k = 0,04. Calcular R:
#   R1 = (Ix2 ∗ Iy2 − Ixy^2) − k ∗ (Ix2 + Iy2)2
#   R2 = (Ix2 ∗ Iy2 − Ixy^2)/(Ix2 + Iy2 + eps) --> (eps como parámetro)
#   R3 = (Ix2 ∗ Iy2 − Ixy^4) − k ∗ (Ix2 + Iy2)2
# 5. Encontrar los máximos o  umbralizar: R > umbral
# Primero probar con el cuadrado blanco, luego con cualquier imagen como test
# Es invariante a transformaciones como rotaciones 2D o iluminación, pero NO es invariante a escalas.
# Porque? Como usamos la matriz de autovalores, tanto para una rotación como para una mayor iluminación (que es igual
# en toda la foto, mayor intensidad en las escalas de grises) esta matriz se mantiene igual, no se ve afectada.
import numpy as np
from PIL import Image

from Algorithms.Classes.MyImage import MyImage
from Algorithms.EdgeDetection.Canny import mask_h, mask_v
from Algorithms.EdgeDetection.EdgeDetection import get_directional_derivatives
from Algorithms.Filters.Filters import get_pixels_around


def gaussian_filter(pixels, sigma: int):

    w, h = pixels.shape
    mask = 2 * sigma + 1
    full_mask = np.zeros(shape=(mask, mask))
    pixel_array2 = pixels.copy()

    for x in range(mask):
        for y in range(mask):
            full_mask[x][y] = np.exp(-(x ** 2 + y ** 2) / (sigma ** 2)) / (
                    2 * np.pi * (sigma ** 2))

    full_mask = np.divide(full_mask, np.sum(full_mask))

    for i in range(w):
        for j in range(h):
            pixel_array2[j][i] = np.sum(get_pixels_around(pixels, j, i, full_mask))

    return pixel_array2


def harris_detector(my_image: MyImage, gauss_sigma: int, k: float, percentile: float):

    if my_image is None:
        return

    img = my_image.image

    ix2 = np.ndarray(shape=my_image.dimensions)
    iy2 = np.ndarray(shape=my_image.dimensions)
    ixy = np.ndarray(shape=my_image.dimensions)
    w, h = my_image.dimensions
    pixel_array = np.array(img, dtype=np.float64)

    # Calcular Ix e Iy usando las máscaras de Prewitt o Sobel para cada pixel de la imagen.
    gx, gy = get_directional_derivatives(pixel_array, w, h, mask_h, mask_v)

    # Calcular Ix2 elevando Ix^2 elemento a elemento. Lo mismo Iy2.
    # Calcular Ixy multiplicando elemento a elemento
    for x in range(w):
        for y in range(h):
            ix2[x, y] = np.power(gx[x, y], 2)
            iy2[x, y] = np.power(gy[x, y], 2)
            ixy[x, y] = gx[x, y] * gy[x, y]

    # y aplicar un filtro gaussiano para suavizar, por ejemplo, de 7x7 con σ = 2.
    ix2 = gaussian_filter(ix2, gauss_sigma)
    iy2 = gaussian_filter(iy2, gauss_sigma)
    ixy = gaussian_filter(ixy, gauss_sigma)

    # Ya tengo Ix2, Iy2 e Ixy --> tengo la matriz M --> Calcular R (usamos R1)
    r = np.ndarray(shape=my_image.dimensions)
    for x in range(w):
        for y in range(h):
            r[x, y] = (ix2[x, y] * iy2[x, y] - np.power(ixy[x, y], 2)) - k * np.power(ix2[x, y] + iy2[x, y], 2)

    # Encontrar los máximos o  umbralizar: R > umbral
    # Primero normalizamos
    # norm_r = np.ndarray(shape=img.shape)
    # r_max = r.max()
    # r_min = r.min()
    # for x in range(w):
    #     for y in range(h):
    #         norm_r[x, y] = (r[x, y]-r_min)/(r_max-r_min) * 255

    # el valor bajo el cual se encuentran el @percentile por ciento de las observaciones
    threshold = np.percentile(r, percentile)
    print(threshold)

    # Mostramos los corners
    drawn_img = Image.new('RGB', my_image.dimensions)
    for x in range(w):
        for y in range(h):
            if r[x, y] >= threshold:
                drawn_img.putpixel((y, x), (255, 0, 0))
            else:
                pixel = int(pixel_array[x, y])
                drawn_img.putpixel((y, x), (pixel, pixel, pixel))

    return MyImage.from_image(drawn_img, my_image.dimensions)
