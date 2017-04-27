import traceback

def verify( result, input_data, gold ):
  ok, message = True, "something is odd, there is no feedback given :|"

  try:
    # Make sure the result is an image: dictionary with correct keys.
    if (type(result) is not dict) or (sorted(result.keys()) == (["width", "height", "pixels"])):
      ok, message =  "Result should be an image, but isn't."

    # Check image dimensions
    elif (gold["width"], gold["height"]) != (result["width"], result["height"]):
      ok, message = False, "Resulting image has incorrect dimensions. Your output is " + \
                    str(result["width"]) + "x" + str(result["height"])

    # Check pixel values are integers
    elif sum([1 for x in result["pixels"] if type(x) is not int]) > 0:
      ok, message = False, "Resulting image has pixels that are not integers"

    # Check pixel values are in range [0,255]
    elif sum([1 for x in result["pixels"] if ((x > 255) or (x<0))]) > 0:
      ok, message = False, "Resulting image has pixels outside the legal range of [0,255]"

    # Check pixel values are within an error margin
    else:
      distance = sum([ abs(result["pixels"][i]-gold["pixels"][i]) for i in range(len(gold["pixels"])) ])
      if distance > ((result["width"]*result["height"]*255)/100):
        ok, message = False, "Resulting image has more than 1% error from pixel values! Average distance per pixel is " + str(distance/(result["width"]*result["height"]))

    if ok:
      message = "The image is close enough, with distance of %s to the staff solution." % str(distance)

  except:
    print(traceback.format_exc())
    ok = False
    message = "your code could not be verified :(. Stack trace is printed above so you can debug."
  return ok, message
