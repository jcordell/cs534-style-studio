import numpy as np
import cv2
from lib.FaceDetector import FaceDetector
from lib.Makeover import Makeover
from PIL import Image
import argparse
import imutils
from math import tan, degrees


def load_image(path, flag=1):
    # -1 flag opens image with transparent background
    return cv2.imread(path, flag)


def save_image(path, image):
    cv2.imwrite(path, image)


def pil_load_image(path):
    return Image.open(path)


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser(description='styleStudio will apply selected filters to your uploaded head-shot.',
                             epilog="Enjoy your new look!")

# image path to face is required each time
ap.add_argument("-i", "--image", required=True,
                help="path to input image")

# flags for glasses options
ap.add_argument('-g', action='store_true', required=False, help="Glasses Flag")
ap.add_argument('-standard', action='store_true',
                required=False, help="Standard Framed Glasses")
ap.add_argument('-circles', action='store_true',
                required=False, help="Circular Framed Glasses")
ap.add_argument('-rounded', action='store_true',
                required=False, help="Round Framed Glasses")

# flags for beard options
ap.add_argument('-b', action='store_true', required=False, help="Beard Flag")
ap.add_argument('-brown_full', action='store_true',
                required=False, help="Full Brown Beard")
ap.add_argument('-black_full', action='store_true',
                required=False, help="Full Black Beard")

# flags for moustache options
ap.add_argument('-m', action='store_true',
                required=False, help="Moustache Flag")
ap.add_argument('-brown_curly', action='store_true',
                required=False, help="Brown Curly Moustache")

# flags for earings options
ap.add_argument('-e', action='store_true', required=False, help="Earing Flag")
ap.add_argument('-green_dangly', action='store_true',
                required=False, help="Green Dangly Earings")
ap.add_argument('-diamond_stud', action='store_true',
                required=False, help="Diamond Stud Earings")

# flags for nose stud options
ap.add_argument('-ns', action="store_true",
                required=False, help="Nose Stud Flag")
ap.add_argument('-blue_stud', action='store_true',
                required=False, help="Blue Nose Stud")
ap.add_argument('-shiny_stud', action='store_true',
                required=False, help="Shiny Nose Stud")

# flags for necklace options
ap.add_argument('-n', action="store_true",
                required=False, help="Necklace Flag")
ap.add_argument('-green_gem', action='store_true',
                required=False, help="Green Gem Necklace")

options = vars(ap.parse_args())

# initiates the parsing of arguments
args = ap.parse_args()


# image = load_image('images/face.jpeg')
# image = load_image('images/professor.jpg')

image = cv2.imread(options["image"])
image = imutils.resize(image, width=500)

face = FaceDetector(image)

# use resized image
image = face.image

save_image('generated_images/saved_face.png', image)
background = pil_load_image('generated_images/saved_face.png')
makeover = Makeover(background, face.feature_map)

# program controller based on flags from command line

# glasses flags for different styles
if args.g:
    if args.standard:
        makeover.add_glasses('glasses1')
    if args.circles:
        makeover.add_glasses('glasses2')
    if args.rounded:
        makeover.add_glasses('glasses3')

# beard flags for different styles
if args.b:
    if args.brown_full:
        makeover.add_beard('beard1')
    if args.black_full:
        makeover.add_beard('beard2')

# moustache flags for different styles
if args.m:
    if args.brown_curly:
        makeover.add_mustache('mustache1')

# earings flags for different styles
if args.e:
    if args.green_dangly:
        makeover.add_earings('earing1')
    if args.diamond_stud:
        makeover.add_earings('earing2')

# nose stud flags for different styles
if args.ns:
    if args.blue_stud:
        makeover.add_nose_stud('nose_stud1')
    if args.shiny_stud:
        makeover.add_nose_stud('nose_stud2')

if args.n:
    if args.green_gem:
        makeover.add_necklace('green_gem')

makeover_image = makeover.get_makeover()
makeover_image.show()
