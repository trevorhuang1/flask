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


# Test Joke Model
if __name__ == "__main__": 
    image = Image.open('../hacks/images/clouds-impression.png')
    imageToBase64(pixelate(image, 8))
    print("~~~Debug~~~")