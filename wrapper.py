import lab, json, inspect, traceback
## Force lab code to be re-loaded when wrapper is re-loaded.
from importlib import reload
reload(lab) # this forces the student code to be reloaded when page is refreshed

## Required wrapper methods for autograder
# this is used by test.py and funprog analyzer
def run_test( input_data ):
  result = {"width": 1, "height": 1, "pixels": [0]} # default
  try:
    f = getattr(lab, input_data["function"])
    img = None
    with open("resources/images/" + input_data["image_file"], "r") as file:
      img = json.load(file)
    return f(img)
  except:
    print(traceback.format_exc())
  return result

## Methods pertaining to the UI
# list all functions of the form "filter_*" in the lab
def list_filters( input_data ):
  filters = []
  for f_name in dir(lab):
    # non-functions are ignored
    f = getattr(lab, f_name)
    if not inspect.isfunction(f):
      continue
    # things that begin with "filter_" are of interest
    if f_name.startswith('filter_'):
      filters.append(f_name[7:])
  return filters

# apply a named filter to an image
def apply_filter( input_data ):
  result = {"width": 1, "height": 1, "pixels": [0]} # default
  try:
    filter = getattr(lab, "filter_%s" % input_data["filter"])
    result = filter(input_data["image"])
  except:
    print(traceback.format_exc())
  return result

## TODO ITEMS:
# TODO: What happens in the UI when things crash?
# TODO: TRY THIS!

# TODO: Export list of images (implement ls and cat in the server!)

# UI:
# TODO: name images, and show input and output side by side
# TODO: show boat -- (filter) --> filter(boat)
#       filter(boat) -- filter2 --> filter2(filter(boat))

## Initialization
def init():
  # nothing to do!
  return

init()
