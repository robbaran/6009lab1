# The code below seems to have some problems.
# Fix it before implementing the rest of your lab

def width(image):
    return image["width"]

def height(image):
    return image["height"]

def pixel(image, x, y):
    index = x + width(image)*y
    return image["pixels"][index]

def set_pixel(image, x, y, color):
    index = x + width(image)*y
    image["pixels"][index] = color

def make_image(width, height):
    return {"width": width, "height": height, "pixels": ([0]*width*height)}

# return a new image by applying function f to each pixel of the input image
def apply_per_pixel(image, f):
    result = make_image(width(image),height(image))
    for x in range(width(result)):
        for y in range(height(result)):
            color = pixel(image, x, y)
            set_pixel(result, x, y, f(color))
    return result
  
def invert(c):
    return abs(255-c)
    
def filter_invert(image):
    return apply_per_pixel(image, invert)

# any function of the form "filter_X( image ):", where X denotes the name of
# the filter, can be applied via test.py and the web UI!
# Feel free to go wild and implement your favorite filters once you are done.
# Here are some to inspire you: [GIMP filters](https://docs.gimp.org/en/filters.html)
