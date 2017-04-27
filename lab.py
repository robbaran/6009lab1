# The code below seems to have some problems.
# Fix it before implementing the rest of your lab

def ncols(image):
    return image["width"]

def nrows(image):
    return image["height"]

def get_pixel(image, col, row, default=0):
  index = col + ncols(image)*row
  if col >= 0 and col < ncols(image) and row >= 0 and row < nrows(image): 
    pxl = image["pixels"][index]
  else:
    pxl = default
  return pxl  

def set_pixel(image, col, row, color):
  index = col + ncols(image)*row
  image["pixels"][index] = color

def make_image(ref_image):
  return {"width": ref_image['width'], "height": ref_image['height'], "pixels": ([0]*len(ref_image['pixels']))}

def legalize_range(image):
  result = make_image(image)
  for col in range(ncols(image)):
    for row in range(nrows(image)):
      pxl = int(round(get_pixel(image, col, row)))
      pxl = min(255,pxl) #clip pxl at 255 max
      set_pixel(result,col,row,pxl)
  return result

# return a new image by applying function f to each pixel of the input image
def apply_per_pixel(image, f):
    result = make_image(image)
    for col in range(ncols(result)):
        for row in range(nrows(result)):
            color = get_pixel(image, col, row)
            set_pixel(result, col, row, f(color))
    return result
  
def invert(c):
    return abs(255-c)

def convolve2d(image, kernel):
  #kernel is a 3x3 list of lists
  #returns convolution of image with kernel
  result = make_image(image)	#start with empty image
  #iterate over every pixel in image
  for col in range(ncols(image)):
    for row in range(nrows(image)):
      conv = 0
      for kx in range(len(kernel[0])):
        for ky in range(len(kernel)):
          pxl = get_pixel(image, col-1+kx, row-1+ky)
          inc = pxl * kernel[ky][kx]
          conv += inc
      set_pixel(result, col,row,conv)
  return result    

def combine_images(image1, image2, f):
  #image1 is the same size as image2
  w = ncols(image1)
  h = nrows(image1)
  result = make_image(image1)
  for col in range(w):
    for row in range(h):
      set_pixel(result, col, row, f(get_pixel(image1, col, row),get_pixel(image2, col, row)))
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
  return legalize_range(combine_images(Ox,Oy,combine_pyth))
# any function of the form "filter_X( image ):", where X denotes the name of
# the filter, can be applied via test.py and the web UI!
# Feel free to go wild and implement your favorite filters once you are done.
# Here are some to inspire you: [GIMP filters](https://docs.gimp.org/en/filters.html)
