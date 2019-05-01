#!/usr/bin/env python

import argparse
import os
import sys
import time

print("---------")
print("importing zwo")
import zwoasi as asi

from time import gmtime, strftime

print("ok")

#from scipy.ndimage.filters import convolve

print("cv2")

import cv2

print("numpy")
import numpy as np

print("PIL")
from PIL import Image

#print("tstack"
#from colour.utilities import tstack

#print("CFA"
#from colour_demosaicing.bayer import masks_CFA_Bayer

#print("read flat")
#flat = cv2.imread('flat16sun.tif',-1)

#print(type(flat))
#print(flat)

##Favg = np.average(flat)

#print(Favg)

#flat=Favg/flat

#print(flat)



print("---------")

__author__ = 'Steve Marple'
__version__ = '0.0.22'
__license__ = 'MIT'


env_filename = os.getenv('ZWO_ASI_LIB')

parser = argparse.ArgumentParser(description='Process and save images from a camera')
parser.add_argument('filename',
                    nargs='?',
                    help='SDK library filename')
args = parser.parse_args()

# Initialize zwoasi with the name of the SDK library
if args.filename:
    asi.init(args.filename)
elif env_filename:
    asi.init(env_filename)
else:
    print('The filename of the SDK library is required (or set ZWO_ASI_LIB environment variable with the filename)')
    sys.exit(1)

num_cameras = asi.get_num_cameras()
if num_cameras == 0:
    print('No cameras found')
    sys.exit(0)

cameras_found = asi.list_cameras()  # Models names of the connected cameras

if num_cameras == 1:
    camera_id = 0
    print('Found one camera: %s' % cameras_found[0])
else:
    print('Found %d cameras' % num_cameras)
    for n in range(num_cameras):
        print('    %d: %s' % (n, cameras_found[n]))
    # TO DO: allow user to select a camera
    camera_id = 0
    print('Using #%d: %s' % (camera_id, cameras_found[camera_id]))

camera = asi.Camera(camera_id)
camera_info = camera.get_camera_property()


controls = camera.get_controls()


# Use minimum USB bandwidth permitted

camera.set_control_value(asi.ASI_BANDWIDTHOVERLOAD, camera.get_controls()['BandWidth']['MaxValue'])

camera.disable_dark_subtract()

print('Enabling stills mode')
try:
    # Force any single exposure to be halted
    camera.stop_video_capture()
    camera.stop_exposure()
except (KeyboardInterrupt, SystemExit):
    raise
except:
    pass
	
gain=0
exp=418

camera.set_control_value(asi.ASI_GAIN, gain)

#camera.set_image_type(asi.ASI_IMG_RAW8)
#camera.set_image_type(asi.ASI_IMG_RGB24)
camera.set_image_type(asi.ASI_IMG_RAW16)

#camera.set_control_value(asi.ASI_WB_B, 78)#solar guider
camera.set_control_value(asi.ASI_WB_B, 78)#gantry
camera.set_control_value(asi.ASI_WB_R, 77)#gantry
#camera.set_control_value(asi.ASI_WB_R, 55)#solar guider
camera.set_control_value(asi.ASI_GAMMA, 150)
camera.set_control_value(asi.ASI_BRIGHTNESS, 50)
camera.set_control_value(asi.ASI_FLIP, 0)

camera.set_control_value(controls['AutoExpMaxExpMS']['ControlType'], 20000)
#camera.set_control_value(controls['HardwareBin']['ControlType'], controls['HardwareBin']['MinValue'])

#time.sleep(0.1)



camera.set_control_value(asi.ASI_EXPOSURE, exp)
print('Capturing a single 16-bit mono image')
filename = 'image_mono16.tiff'

imagey = camera.capture()

#pre = 45000 * ((imagey*flat)/65535)**(1/1.5)
#pre = 45000 * ((imagey*flat)/65535)**(1/1.5)
#print(flat
#pre = imagey#65535 * (imagey/65535)**(1/1.5)

debayer = cv2.cvtColor(np.uint16(np.clip(imagey,0,65535)), cv2.COLOR_BayerRG2RGB )
#debayer = cv2.cvtColor(np.uint16(np.clip(pre,0,65535)), cv2.COLOR_BayerGR2RGB ) #120

fname = strftime("%Y-%m-%d %H%M%S", gmtime())+" "+str(exp)+"ms g"+str(gain)+".tif"

print(fname)

cv2.imwrite(fname, debayer)

##im = Image.fromarray(debayer)

#idebayer.save("your_file2-rgb.tif")


