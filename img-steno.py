#!/usr/bin/env python2

# packages:
# pip2 install pwntools
# pip2 install Pillow
# pip2 install matplotlib

from pwn import *
from matplotlib import pyplot
import PIL
import argparse
import numpy as np

def show_histogram(img):
	max_value = max(
		img.getextrema()[0][1],
		img.getextrema()[1][1],
		img.getextrema()[2][1]
	)
	values = np.zeros((max_value + 1, 3))
	
	pyplot.figure(0)
	(w,h) = img.size
	for y in range(h):
		for x in range(w):
			pix = img.getpixel((x,y))
			values[pix[0],0] += 1
			values[pix[1],1] += 1
			values[pix[2],2] += 1

	pyplot.step(values[:,0], 'r-')
	pyplot.step(values[:,1], 'g-')
	pyplot.step(values[:,2], 'b-')

def show_bitplanes(img):
	(w,h) = img.size
	max_value = max(
		img.getextrema()[0][1],
		img.getextrema()[1][1],
		img.getextrema()[2][1]
	)
	i = 1
	while i < max_value:
		print("create bitplane ",i)
		pyplot.figure(i)
		plane = np.zeros((h,w,3))
		for y in range(h):
			for x in range(w):
				pix = img.getpixel((x,y))
				if (pix[0] & i) > 0:
					plane[y,x,0] = 255
				if (pix[1] & i) > 0:
					plane[y,x,1] = 255
				if (pix[2] & i) > 0:
					plane[y,x,2] = 255

		pyplot.imshow(plane)
		i = i * 2

parser = argparse.ArgumentParser(description='Analyze images an decode simple bit-encodings')

parser.add_argument('-g','--histogram', action='store_true', help='show a histogram of RGB values')
parser.add_argument('-b','--bitplanes', action='store_true', help='showo all bitplanes from RGB channels')

parser.add_argument('filename', help='The Image to analyze')



args = parser.parse_args()
print(args)

img = PIL.Image.open(args.filename)

if args.histogram:
	show_histogram(img)
if args.bitplanes:
	show_bitplanes(img)

pyplot.show()
