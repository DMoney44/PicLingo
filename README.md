# PicLingo

 PicLingo is an AI application that allows people to visually learn another language by using their surroundings. It uses **detectnet** in the 
 **jetson-inference** library and translates them into the specified languages.

Examples:

![Before code.](https://i.imgur.com/1ZMmiGh.jpg)
![After code.](https://i.imgur.com/0LmBMh2.jpg)
![Before code.](https://i.imgur.com/fWfoa4l.jpg)
![After code.](https://i.imgur.com/wjapAd1.jpg)
## The Algorithm

The Algorithm is a modified version of the detectnet sample code. It uses argument parsers to get what the user wants the base language to be (1) and then what
the user wants to translate that language into (2). It then uses **cudaFont()** to display overlay text onto the detected objects and displays the languages
involved in the translation. PicLingo uses the **googletrans** library and the **unidecode** library which is necessary for the code to run properly. This
program's main and only limitation is that it is not able to display accented letters. If I had more time to work on this project, I could have changed the font
file from which **cudaFont()** gets its letters but I did not have enough time.

This is the algorithm:

![Algorithm pic](https://i.imgur.com/ZfCKDov.jpg)

## Running this project

First, you must install the required libraries in the command terminal type:

pip3 install setuptools

pip3 install googletrans

pip3 install Unidecode

Once the libraries, project file, and the **jetson-inference** library are installed move into the directory where you saved the project file. In the terminal call
the file with **python3 PicLingoV2.py** type **--translate (base language) --out (translated language)** then type the image that you want to run through the code. 
If you do not know the language codes, type **-h** or **-help** and scroll until you find the translation key.

[View a video explanation here](video link)
