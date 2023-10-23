from PIL import Image
import base64
from io import BytesIO

def imageToBase64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    img_str = img_str.decode('utf-8')
    return img_str

def base64toImage(base64string):
    img_str = base64.b64decode(base64string)
    image = Image.open(BytesIO(img_str))
    return image

def pixelate(image, size):
    org_size = image.size
    pixelate_lvl = size

    image = image.resize(
        size=(org_size[0] // pixelate_lvl, org_size[1] // pixelate_lvl),
        resample=0)
    image = image.resize(org_size, resample=0)

    return image

def combine(b641, b642, direction, resample=Image.BICUBIC, resize_big_image=True):
    im1 = base64toImage(b641)
    im2 = base64toImage(b642)
    if direction == "Horizontal":
        if im1.height == im2.height:
            _im1 = im1
            _im2 = im2
        elif (((im1.height > im2.height) and resize_big_image) or
            ((im1.height < im2.height) and not resize_big_image)):
            _im1 = im1.resize((int(im1.width * im2.height / im1.height), im2.height), resample=resample)
            _im2 = im2
        else:
            _im1 = im1
            _im2 = im2.resize((int(im2.width * im1.height / im2.height), im1.height), resample=resample)
        dst = Image.new('RGB', (_im1.width + _im2.width, _im1.height))
        dst.paste(_im1, (0, 0))
        dst.paste(_im2, (_im1.width, 0))
    else:
        if im1.width == im2.width:
            _im1 = im1
            _im2 = im2
        elif (((im1.width > im2.width) and resize_big_image) or
            ((im1.width < im2.width) and not resize_big_image)):
            _im1 = im1.resize((im2.width, int(im1.height * im2.width / im1.width)), resample=resample)
            _im2 = im2
        else:
            _im1 = im1
            _im2 = im2.resize((im1.width, int(im2.height * im1.width / im2.width)), resample=resample)
        dst = Image.new('RGB', (_im1.width, _im1.height + _im2.height))
        dst.paste(_im1, (0, 0))
        dst.paste(_im2, (0, _im1.height))
        dst.paste(_im2, (0, _im1.height))
    return imageToBase64(dst)


# Test Pixel Model
if __name__ == "__main__": 
    print("~~~Debug~~~")