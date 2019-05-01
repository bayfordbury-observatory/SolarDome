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

blank_image = np.zeros((1280,960,3), np.uint8)


#debayer = cv2.resize(cv2.cvtColor(np.uint8(np.clip(pre/256,0,255)), cv2.COLOR_BayerRG2RGB ), (0,0), fx=0.5, fy=0.5) 
debayer = cv2.imread('Capture_00001.tif',1)

gray_image = cv2.cvtColor(debayer, cv2.COLOR_RGB2GRAY)

#gray_image= cv2.GaussianBlur(gray_image,(5,5),0)

#gray_image = cv2.medianBlur(gray_image,5)
	
#gray_image=(float(gray_image - min) / (max - min))*255
#gray_image=cv2.equalizeHist(gray_image)


cimg = gray_image

canny = 50

print "detecting circles" 
circles = cv2.HoughCircles(gray_image,cv2.HOUGH_GRADIENT,1,100, param1=canny,param2=20,minRadius=200,maxRadius=250) #220 radius
print "done"
edges = cv2.Canny(gray_image,10,canny)

if circles is not None:

	circles = np.uint16(np.around(circles))
	print "detected circles"
	for i in circles[0,:]:
		# draw the outer circle
		print("circle at x: "+str(i[0])+" y: "+str(i[1])+" r: "+str(i[2]))
		
		cv2.circle(cimg,(i[0],i[1]),i[2],(255,255,255),2)
		# draw the center of the circle
		cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
		


cv2.imshow('circles',cimg)
cv2.imshow('orig',debayer)
cv2.imshow('edges',edges)

##im = Image.fromarray(cimg)

#idebayer.save("your_file2-rgb.tif")

cv2.waitKey(0)
cv2.destroyAllWindows()
	
	#time.sleep(2)
#cv2.destroyAllWindows()
