from PIL import Image


def get_cropped_image(image: Image, crop_area):
    img = image

    img_left_area = get_area(crop_area)
    img_left = img.crop(img_left_area)

    return img_left


def get_area(crop_area):

    crop_start, crop_end = crop_area

    bigger_x, smaller_x, bigger_y, smaller_y = 0, 0, 0, 0

    if crop_start.x() >= crop_end.x():
        bigger_x = crop_start.x()
        smaller_x = crop_end.x()
    else:
        bigger_x = crop_end.x()
        smaller_x = crop_start.x()

    if crop_start.y() >= crop_end.y():
        bigger_y = crop_start.y()
        smaller_y = crop_end.y()
    else:
        bigger_y = crop_end.y()
        smaller_y = crop_start.y()

    return smaller_x, smaller_y, bigger_x, bigger_y
