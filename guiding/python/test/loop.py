#!/usr/bin/env python

import argparse
import os
import sys
import time

print "---------"


print "ok"

#from scipy.ndimage.filters import convolve

print "cv2"

import cv2

print "numpy"
import numpy as np

print "PIL"
from PIL import Image

#print "tstack"
#from colour.utilities import tstack

#print "CFA"
#from colour_demosaicing.bayer import masks_CFA_Bayer


print "---------"

for n in range(119, 245):

	fname = 'Capture_'+str(n).rjust(5, '0')+'.tif'

	#print(fname)

	debayer = cv2.imread(fname,1)
	
	rSum = 0
	gSum = 0
	bSum = 0
	
	for x in range(0, 1280):
		for y in range(0, 960):
			val = debayer[y,x]
			
			rSum = rSum + val[2]
			gSum = gSum + val[1]
			bSum = bSum + val[0]
	
	gray_image = cv2.cvtColor(debayer, cv2.COLOR_RGB2GRAY)


	canny = 50

	circles = cv2.HoughCircles(gray_image,cv2.HOUGH_GRADIENT,1,100, param1=canny,param2=20,minRadius=200,maxRadius=250) #220 radius
	
	if circles is not None:
	
		circles = np.uint16(np.around(circles))
	
		for i in circles[0,:]:
			# draw the outer circle
			print(str(n)+" "+str(i[0])+"  "+str(i[1])+"  "+str(i[2])+" "+str(float(rSum)/(1280*960))+" "+str(float(gSum)/(1280*960))+" "+str(float(bSum)/(1280*960)))
	
	else:
			print(str(n)+" 0 0 0 "+str(float(rSum)/(1280*960))+" "+str(float(gSum)/(1280*960))+" "+str(float(bSum)/(1280*960)))
	