from PIL.Image import open as open_image
import pkg_resources
from os import listdir as os_listdir
images_dir = pkg_resources.resource_filename(__name__, 'images')
allchar = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+,.-? \n"
images = {i.removesuffix(".png"):open_image(images_dir+"/"+i) for i in os_listdir(images_dir)}

def handwrite(text: str):
    img = images['background']
    width,height = 50,0
    for letter in text:
        if letter in allchar:
            if letter == " ":
                letter = "_"
            if letter.isupper():
                letter = "_"+letter
            if letter == "?":
                letter = "que"
            if width + 150 >= img.width:
                height = height + 227
                width = 50
            if letter == "\n":
                height += 227
                width = 50
                continue
            cases = images[letter]
            img.paste(cases,(width,height))
            width += cases.width
    return img
