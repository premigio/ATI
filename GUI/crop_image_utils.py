from PIL import Image


def get_cropped_image(image: Image, crop_area):
    img = image

    img_left_area = get_area(crop_area)
    img_left = img.crop(img_left_area)

    return img_left


def get_area(crop_area):

    crop_start, crop_end = crop_area

    higher_x, lower_x, higher_y, lower_y = 0, 0, 0, 0

    if crop_start.x() >= crop_end.x():
        higher_x = crop_start.x()
        lower_x = crop_end.x()
    else:
        higher_x = crop_end.x()
        lower_x = crop_start.x()

    if crop_start.y() >= crop_end.y():
        higher_y = crop_start.y()
        lower_y = crop_end.y()
    else:
        higher_y = crop_end.y()
        lower_y = crop_start.y()

    return lower_x, lower_y, higher_x, higher_y
