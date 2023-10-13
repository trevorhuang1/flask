from PIL import Image
import base64
from io import BytesIO

def imageToBase64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    ## returns bytes, do on frontend is better
    ## print(img_str.decode('utf-8'))
    return img_str

def getTestPixel(image, size):
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
    imageToBase64(getTestPixel(image, 8))
    print("~~~Debug~~~")