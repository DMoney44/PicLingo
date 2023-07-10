#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

import sys
import argparse
from unidecode import unidecode

from googletrans import Translator

from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, Log, cudaFont

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, 
                                 epilog=detectNet.Usage() + videoSource.Usage() + videoOutput.Usage() + Log.Usage())

parser.add_argument("input", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default= 0.8, help="minimum detection threshold to use") 
parser.add_argument("--translate", type=str, default= "en", help= "----------Translation Key----------\n\n--TOP--\nAmharic	am \nArabic	ar \nBasque	eu \nBengali	bn \nEnglish (UK)	en-GB \nPortuguese (Brazil)	pt-BR \nBulgarian	bg \nCatalan	ca \nCherokee	chr \nCroatian	hr \nCzech	cs \nDanish	da \nDutch	nl \nEnglish (US)	en \nEstonian	et \nFilipino	fil \nFinnish	fi \nFrench	fr \nGerman	de \nGreek	el \nGujarati	gu \nHebrew	iw \nHindi	hi \nHungarian	hu \nIcelandic	is \nIndonesian	id \nItalian	it \nJapanese	ja \nKannada	kn \nKorean	ko \nLatvian	lv \nLithuanian	lt \nMalay	ms \nMalayalam	ml \nMarathi	mr \nNorwegian	no \nPolish	pl \nPortuguese (Portugal)	pt-PT \nRomanian	ro \nRussian	ru \nSerbian	sr \nChinese (PRC)	zh-CN \nSlovak	sk \nSlovenian	sl \nSpanish	es \nSwahili	sw \nSwedish	sv \nTamil	ta \nTelugu	te \nThai	th \nChinese (Taiwan)	zh-TW \nTurkish	tr \nUrdu	ur \nUkrainian	uk \nVietnamese	vi \nWelsh	cy\n--BOTTOM--")
parser.add_argument("--to", type=str, default="es", help="See (^Translate^)")

try:
	args = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

# create video sources and outputs
input = videoSource(args.input, argv=sys.argv)
output = videoOutput(args.output, argv=sys.argv)
font = cudaFont(size = 26)
	
# load the object detection network
net = detectNet(args.network, sys.argv, args.threshold)

# note: to hard-code the paths to load a model, the following API can be used:
#
# net = detectNet(model="model/ssd-mobilenet.onnx", labels="model/labels.txt", 
#                 input_blob="input_0", output_cvg="scores", output_bbox="boxes", 
#                 threshold=args.threshold)

# process frames until EOS or the user exits
while True:
    # capture the next image
    img = input.Capture()

    if img is None: # timeout
        continue  
        
    # detect objects in the image (with overlay)
    detections = net.Detect(img, overlay=args.overlay)

    # print the detections
    print("detected {:d} objects in image".format(len(detections)))
    translator = Translator()
    
    if len((detections)) == 0:
        font.OverlayText(img, text="NO OBJECTS FOUND", 
                                x=5, y=-40,
                                color=font.White, background=font.Gray40)
    else:
        for detection in detections:
            stringout = net.GetClassDesc(detection.ClassID)
            leftside = detection.Left
            top = detection.Top
            translation1 = translator.translate(stringout, args.translate)
            translation2 = translator.translate(translation1.text, src= translation1.dest, dest= args.to)
            displaye1 = unidecode(translation1.text)
            displaye2 = unidecode(translation2.text)
            font.OverlayText(img, text= displaye1, 
                                x= int(leftside)+ 5, y= int(top),
                                color=font.White, background= (0, 0, 0))
            font.OverlayText(img, text= displaye2, 
                                x= int(leftside)+ 5, y= int(top) + 27,
                                color=font.White, background= (0, 0, 0))
            print(f"{translation1.text} ({translation1.dest})")
            print(f"{translation2.text} ({translation2.dest})")
        
        LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',}
        font.OverlayText(img, text= LANGUAGES[translation1.dest] + " ---> " + LANGUAGES[translation2.dest], 
                                x= 5, y=-40,
                                color=font.White, background= font.Gray40)

    # render the image
    output.Render(img)

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format(args.network, net.GetNetworkFPS()))

    # print out performance info
    net.PrintProfilerTimes()

    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        break