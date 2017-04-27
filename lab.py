# The code below seems to have some problems.
# Fix it before implementing the rest of your lab

def ncols(image):
    return image["width"]

def nrows(image):
    return image["height"]

def get_pixel(image, x, y, default=0):
  index = x + ncols(image)*y
  if x >= 0 and x < ncols(image) and y >= 0 and y < nrows(image): 
    pxl = image["pixels"][index]
  else:
    pxl = default
  return pxl  

def set_pixel(image, x, y, color):
  index = x + ncols(image)*y
  image["pixels"][index] = color

def make_image(ncols, nrows):
  return {"width": ncols, "height": nrows, "pixels": ([0]*ncols*nrows)}

def legalize_range(image):
  result = make_image(ncols(image),nrows(image))
  for x in range(ncols(image)):
    for y in range(nrows(image)):
      pxl = int(round(get_pixel(image, x, y)))
      pxl = min(255,pxl) #clip pxl at 255 max
      set_pixel(result,x,y,pxl)
  return result

# return a new image by applying function f to each pixel of the input image
def apply_per_pixel(image, f):
    result = make_image(ncols(image),nrows(image))
    for x in range(ncols(result)):
        for y in range(nrows(result)):
            color = get_pixel(image, x, y)
            set_pixel(result, x, y, f(color))
    return result
  
def invert(c):
    return abs(255-c)

def convolve2d(image, kernel):
  #kernel is a 3x3 list of lists
  #returns convolution of image with kernel
  result = make_image(ncols(image),nrows(image))	#start with empty image
  #iterate over every pixel in image
  for x in range(ncols(image)):
    for y in range(nrows(image)):
      conv = 0
      for kx in range(len(kernel[0])):
        for ky in range(len(kernel)):
          pxl = get_pixel(image, x-1+kx, y-1+ky)
          inc = pxl * kernel[ky][kx]
          conv += inc
      set_pixel(result, x,y,conv)
  return result    

def combine_images(image1, image2, f):
  #image1 is the same size as image2
  w = ncols(image1)
  h = nrows(image1)
  result = make_image(w,h)
  for x in range(w):
    for y in range(h):
      set_pixel(result, x, y, f(get_pixel(image1, x, y),get_pixel(image2, x, y)))
  return result

def combine_pyth(pixel1,pixel2):
  return (pixel1**2+pixel2**2)**0.5

Kx=[
[-1,0,1],
[-2,0,2],
[-1,0,1]]

Ky=[
[-1,-2,-1],
[0,0,0],
[1,2,1]]

GAUSSIAN_KERNEL=[
[1/16,2/16,1/16],
[2/16,4/16,2/16],
[1/16,2/16,1/16]]

def filter_invert(image):
    return apply_per_pixel(image, invert)

def filter_gaussian_blur(image):
  return legalize_range(convolve2d(image, GAUSSIAN_KERNEL))

def filter_edge_detect(image):
  Ox = convolve2d(image,Kx)
  Oy = convolve2d(image,Ky)
  sobel = combine_images(Ox,Oy,combine_pyth)
#  print('Ox=',Ox,'Oy=',Oy,'sobel=',sobel)
  return legalize_range(combine_images(Ox,Oy,combine_pyth))
# any function of the form "filter_X( image ):", where X denotes the name of
# the filter, can be applied via test.py and the web UI!
# Feel free to go wild and implement your favorite filters once you are done.
# Here are some to inspire you: [GIMP filters](https://docs.gimp.org/en/filters.html)
