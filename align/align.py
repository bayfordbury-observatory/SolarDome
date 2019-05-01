

import cv2


import numpy as np



# Read the images to be aligned

refnum = 310

reference = 'Capture_'+str(refnum).rjust(5, '0')+'.png'

ref =  cv2.imread(reference, 0)

cv2.imwrite("1/aligned_"+reference, ref)

# Find size of image1

sz = ref.shape

warp_matrix = np.eye(2, 3, dtype=np.float32)

# Specify the number of iterations.
number_of_iterations = 10000;
 
# Specify the threshold of the increment
# in the correlation coefficient between two iterations
termination_eps = 1e-10;
 
# Define termination criteria
criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations,  termination_eps)

for n in range(1, 327):

	if n!=refnum:
	
		print(n)

		toalign = 'Capture_'+str(n).rjust(5, '0')+'.png'

		#im2 =  cv2.imread("Capture_00553.png", 0);
		im2 =  cv2.imread(toalign, 0);
		 		 
		# Run the ECC algorithm. The results are stored in warp_matrix.
		(cc, warp_matrix) = cv2.findTransformECC (ref,im2,warp_matrix, cv2.MOTION_TRANSLATION, criteria)
		
		#print (cc)
		#print(warp_matrix)
		 
		# Use warpAffine for Translation, Euclidean and Affine
		im2_aligned = cv2.warpAffine(im2, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP);
		 
		# Show final results
		#cv2.imshow("Image 1", im1)
		#cv2.imshow("Image 2", im2)
		#cv2.imshow("Aligned Image 2", im2_aligned)

		cv2.imwrite("1/aligned_"+toalign, im2_aligned)

cv2.waitKey(0)