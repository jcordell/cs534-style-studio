# styleStudio (cs534-project)

We have implemented a “styleStudio” application. Our application allows the user to upload a selfie,
and then is able to customize his/her look from a list of features.
Our idea is inspired by our belief that people should be encouraged to express themselves in new, fun, and creative ways.

## Current Features: 

Glasses (-g):

- 'standard'
- 'circles'
- 'rounded'
    
Beard (-b):

- 'brown_full'
- 'black_full'

Moustache (-m):

- 'brown_curly'

Earings (-e):

- 'green_dangly'
- 'diamond_stud'

Nose Studs (-ns):

- 'blue_stud'
- 'shiny_stud'

Necklaces (-n):

- 'green_gem'
    
## Getting Started

Make sure you have Python 3.7 installed locally.

    $ git clone https://github.com/jcordell/cs534-project.git

    $ cd cs534-project

    $ python3 -m venv cs534-project

    $ pip3 install -r requirements.txt

## To run

Step 1: first add your selfie (jpg or png) into the images folder

Step 2: determine features you would like to apply

Run:

    # Using the -h flag will describe command options
    python3 main.py -h
    
    # this will add circle glasses, a full brown beard, and diamond stud earings to my selfie
    python3 main.py -i images/myselfie.jpg -g -circles -b -brown_full -e -diamond_stud
