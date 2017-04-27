# The code below seems to have some problems.
# Fix it before implementing the rest of your lab

def width(image):
    return image["width"]

def height(image):
    return image["height"]

def get_pixel(image, x, y, default=0):
  index = x + width(image)*y
  if x >= 0 and x < width(image) and y >= 0 and y < height(image): 
    pxl = image["pixels"][index]
  else:
    pxl = default
  return pxl  

def set_pixel(image, x, y, color):
  index = x + width(image)*y
  image["pixels"][index] = color

def make_image(width, height):
  return {"width": width, "height": height, "pixels": ([0]*width*height)}

def legalize_range(image):
  result = make_image(width(image),height(image))
  for x in range(width(image)):
    for y in range(height(image)):
      pxl = int(round(get_pixel(image, x, y)))
      if pxl > 255:
        pxl = 255
      set_pixel(result,x,y,pxl)
  return result

# return a new image by applying function f to each pixel of the input image
def apply_per_pixel(image, f):
    result = make_image(width(image),height(image))
    for x in range(width(result)):
        for y in range(height(result)):
            color = get_pixel(image, x, y)
            set_pixel(result, x, y, f(color))
    return result
  
def invert(c):
    return abs(255-c)

def convolve2d(image, kernel):
  #kernel is a 3x3 list of lists
  #returns convolution of image with kernel
  result = make_image(width(image),height(image))	#start with empty image
  #iterate over every pixel in image
  for x in range(width(image)):
    for y in range(height(image)):
      conv = 0
      for kx in range(len(kernel[0])):
        for ky in range(len(kernel)):
          pxl = get_pixel(image, x-1+kx, y-1+ky)
          inc = pxl * kernel[ky][kx]
          conv += inc
      set_pixel(result, x,y,conv)
  return result    

GAUSSIAN_KERNEL=[
[1/16,2/16,1/16],
[2/16,4/16,2/16],
[1/16,2/16,1/16]]

def filter_invert(image):
    return apply_per_pixel(image, invert)

def filter_gaussian_blur(image):
  return legalize_range(convolve2d(image, GAUSSIAN_KERNEL))
# any function of the form "filter_X( image ):", where X denotes the name of
# the filter, can be applied via test.py and the web UI!
# Feel free to go wild and implement your favorite filters once you are done.
# Here are some to inspire you: [GIMP filters](https://docs.gimp.org/en/filters.html)
