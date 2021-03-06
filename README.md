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

    $ git clone https://github.com/jcordell/cs534-style-studio.git

Change directories into the project directory

    $ cd cs534-style-studio
    
Create a new virtual environment for this project

    $ virtualenv venv
    note: You may need to run: pip3 install virtualenv

Activate this virtual environment (You should see a (venv) appear at the beginning of your terminal prompt indicating that you are working inside the virtualenv)
    
    $ source venv/bin/activate

Install all requirements from our requirements.txt file (This may take a few minutes)

    $ pip3 install -r requirements.txt

## To Run

Step 1: Add your selfie (jpg or png) into the images folder
        OR
        you may use an image that is already in the images folder
        

Step 2: Determine features you would like to apply



Examples:

    # Using the -h flag will list descriptions of all command options
    python3 main.py -h
    
    # this will add circle glasses, a full brown beard, and diamond stud earings to myselfie.jpg
    python3 main.py -i images/myselfie.jpg -g -circles -b -brown_full -e -diamond_stud
    
