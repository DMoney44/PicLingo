# PicLingo

 PicLingo is an AI application that allows people to visually learn another language by using their surroundings. It uses **detectnet** in the 
 **jetson-inference** library and translates them into the specified languages.

Examples:

![Before code.](https://i.imgur.com/1ZMmiGh.jpg)
![After code.](https://i.imgur.com/0LmBMh2.jpg)
![Before code.](https://i.imgur.com/fWfoa4l.jpg)
![After code.](https://i.imgur.com/wjapAd1.jpg)
## The Algorithm

The Algorithm is a modified version of the detect net sample code. It uses argument parsers to get what the user wants the base language to be (1) and then what
the user wants to translate that language into (2). It then uses **cudaFont()** to display overlay text onto the detected objects and displays the languages
involved in the translation. PicLingo uses the **googletrans** library and the **unidecode** library. (In the command terminal type:

pip3 install setuptools

pip3 install googletrans

pip3 install Unidecode

which is necessary for the code to run properly. 

The algorithm:

![Algorithm pic](https://i.imgur.com/ZfCKDov.jpg)

## Running this project

1. Add steps for running this project.
2. Make sure to include any required libraries that need to be installed for your project to run.

[View a video explanation here](video link)
