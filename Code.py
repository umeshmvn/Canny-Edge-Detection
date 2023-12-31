# -*- coding: utf-8 -*-
"""VenkataNagaUmeshMunagala_CV_projAssig1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1duFxK6HEzLoGavrYBMKqdpqRxBfr4MZi
"""

# Computer Vision Programming Assignment -I #
                                 # ''''''''''''''''''''''''''''''''''''''''''''''''#
# Name : Venkata Naga Umesh Munagala
# UCF ID: 5574972

import numpy as np
import math
from PIL import Image
import requests as req
from urllib.request import urlopen
import matplotlib.pyplot as plt
import cv2
from io import BytesIO

#------------------------------------------------------------------------------------------------
#Read input image

# Function to load an image from URL
def load_image_from_url(url):
    response = urlopen(url)
    img = Image.open(BytesIO(response.read()))
    return np.asarray(img)

# Function to apply convolution and other operations
def process_image(image):
    # Convert the image to a NumPy array
   # I = np.asarray(image)

    # Your image processing code here
    # For example, displaying the image

    plt.imshow(I, cmap='gray')
    plt.title("Processed Image")
    plt.show()

image_urls = [

    "https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/BSDS300/html/images/plain/normal/gray/24063.jpg",

]

'''# URLs of the images
image_urls = [
    "https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/BSDS300/html/images/plain/normal/gray/372047.jpg",
    "https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/BSDS300/html/images/plain/normal/gray/388016.jpg",
    "https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/BSDS300/html/images/plain/normal/gray/24063.jpg",
]'''

# Loop through each URL
I = None

# Loop through each URL
for url in image_urls:
    # Load image from URL
    img = load_image_from_url(url)

    # Display the original image
    plt.imshow(img, cmap='gray')
    plt.title("Original Image")
    plt.show()

    # Assign the value to I
    I = np.asarray(img)

    # Process the image
    process_image(I)

# Now you can print I outside the loop
print(I)

#------------------------------------------------------------------------------------------------
#creating 1D gaussian mask

def gauss_filter(std_deviation, x_dir):
    """
    Calculate the value of a 1D Gaussian filter at a specific position.

    Parameters:
    - std_deviation (float): The standard deviation of the Gaussian distribution.
    - x_dir (float): The position along the x-direction where the filter is evaluated.

    Returns:
    - float: The value of the Gaussian filter at the specified position.
    """
    # Calculate the square root of 2 * pi
    sqrt_val = math.sqrt(2 * math.pi)

    # Calculate the exponent of the Gaussian function
    exp_val = math.exp(-((x_dir ** 2)) / (2 * (std_deviation ** 2)))

    # Calculate the Gaussian filter value
    filter_value = (1 / (sqrt_val * std_deviation)) * exp_val

    return filter_value

#defining static kernel which is used to create a Gaussian filter
kernel = [-3,-2,-1,0,1,2,3]
std_deviation_values = [0.5, 2, 4]

# List to store Gaussian kernels for different standard deviations
gauss_kernels = []

# Iterate through standard deviation values
for std_deviation in std_deviation_values:
    # Calculate Gaussian filter values for the current standard deviation
    gauss_kernel = [gauss_filter(std_deviation, i) for i in kernel]
    gauss_kernels.append(gauss_kernel)

# Print the resulting Gaussian kernels
for i, gauss_kernel in enumerate(gauss_kernels):
    print(f"Gaussian Kernel for std_deviation={std_deviation_values[i]}: {gauss_kernel}")

#convolution function
#1st parameter-->2 dimensional image
#2nd parameter-->gaussian kernel
def convoluted_function(I, gauss_kernel):
    result = []
# Iterate through each row in the image
    for row in I:
        new_row = []
        # Slide the kernel over the row and perform convolution
        for i in range(len(row) - len(gauss_kernel) + 1):
            convolution = sum(row[i + j] * gauss_kernel[j] for j in range(len(gauss_kernel)))
            new_row.append(convolution)
        result.append(new_row)

    return np.array(result)

# convoluted in the X & Y-direction
Ix = convoluted_function(I, gauss_kernel)
Iy = np.transpose(convoluted_function(np.transpose(I), gauss_kernel))

print("Ix:\n", Ix, "\n\nIy:\n", Iy)
# Save the resulting image 'Ix','Iy' as a JPEG file
cv2.imwrite("Ix.jpg", Ix), cv2.imwrite("Iy.jpg", Iy)

#------------------------------------------------------------------------------------------------
#calculating gaussian derivative
def gauss_derivative(std_deviation, direction):
  #Calculate the value of a 1D Gaussian derivative filter at a specific position.

    const_value = (math.sqrt(2 * math.pi))
    exp_value = np.exp(-(direction ** 2) / (2 * (std_deviation ** 2)))
    result = -direction / (const_value * (std_deviation ** 3)) * exp_value

    return result

print(kernel)

gkderivative_x = []  # List to store Gaussian derivative values for x-direction
i = 0
while i < len(kernel): # Calculate Gaussian derivative values for x-direction and append to the list
    gkderivative_x.append(gauss_derivative(0.5, kernel[i]))
    i += 1

print(gkderivative_x)

# Gaussian derivative of y-direction
gkderivative_y = np.transpose(gkderivative_x)

#------------------------------------------------------------------------------------------------
#performing convolution to get derivative of Ix
I_X = np.array(convoluted_function(I, gkderivative_x))

cv2.imwrite("IxPrime.jpg",cv2.normalize(I_X,None,0,255,norm_type=cv2.NORM_MINMAX))

I_Y = np.array(np.transpose(convoluted_function(np.transpose(I), gkderivative_x)))

cv2.imwrite("IyPrime.jpg",cv2.normalize(I_Y,None,0,255,norm_type=cv2.NORM_MINMAX))


#------------------------------------------------------------------------------------------------
#Performing padding
Ix_prime = I_X
Iy_prime = I_Y
img_size = I

# padding with zeros
# The padding is applied symmetrically on both sides
pad_x = np.zeros((img_size.shape[0],(img_size.shape[1]-Ix_prime.shape[1])//2))

row = np.insert(I_X,0,np.transpose(pad_x),axis=1)
# This completes the symmetric zero-padding for 'Ix_prime' and appended in row
row = np.append(pad_x,row,axis=1)

print(row.shape)

trans = np.transpose(I_Y)
# Create a zero-padded array 'pad_y' for the Y-direction convolution result
pad_y = np.zeros((img_size.shape[1],(img_size.shape[0]-Iy_prime.shape[0])//2))
# This completes the symmetric zero-padding for 'Ix_prime' and appended in col
col = np.insert(trans,0,np.transpose(pad_y),axis=1)
col = np.append(pad_y,col,axis=1)
col = np.transpose(col)

#col = np.insert(I_Y,trans.shape[0],pad_y,axis=0)

#------------------------------------------------------------------------------------------
#calculating magnitude
if row.shape != col.shape:
    col = np.transpose(col)

# Calculated magnitude
magnitude = np.sqrt(row**2 + col**2)
print(magnitude)
#normalized the image

normal = cv2.normalize(Ix_prime,  None, 0, 255, cv2.NORM_MINMAX)

#performing tan inverse to get the angles
tan_inv = np.arctan(col/row)
# Converted the angles from radians to degrees
tan_inv_deg = np.rad2deg(tan_inv)

# parameter->angle
def nonMax(tan_inv_deg, magnitude):
    tan_deg = np.nan_to_num(tan_inv_deg, nan=90)
    tan_deg_mag = magnitude.copy()

    # Shift the magnitude matrix in all directions
    mag_above = np.roll(magnitude, shift=-1, axis=0)
    mag_below = np.roll(magnitude, shift=1, axis=0)
    mag_left = np.roll(magnitude, shift=-1, axis=1)
    mag_right = np.roll(magnitude, shift=1, axis=1)

    # Shift the magnitude matrix in diagonal directions
    mag_above_left = np.roll(mag_left, shift=-1, axis=0)
    mag_above_right = np.roll(mag_right, shift=-1, axis=0)
    mag_below_left = np.roll(mag_left, shift=1, axis=0)
    mag_below_right = np.roll(mag_right, shift=1, axis=0)

    # Mask for each condition
    condition_1 = np.logical_or((90 - 22.5 <= tan_deg), (tan_deg <= 90 + 22.5)) | np.logical_or((-90 - 22.5 <= tan_deg), (tan_deg <= -90 + 22.5))
    condition_2 = np.logical_or((45 - 22.5 <= tan_deg), (tan_deg <= 45 + 22.5)) | np.logical_or((-45 - 22.5 <= tan_deg), (tan_deg <= -45 + 22.5))
    condition_3 = np.logical_or((-22.5 <= tan_deg), (tan_deg <= 22.5)) | np.logical_or((180 - 22.5 <= tan_deg), (tan_deg <= 180))
    condition_4 = np.logical_or((135 - 22.5 <= tan_deg), (tan_deg <= 135 + 22.5)) | np.logical_or((-135 - 22.5 <= tan_deg), (tan_deg <= -135 + 22.5))

    # Apply non-maximum suppression conditions
    tan_deg_mag[condition_1 & (magnitude < mag_above) & (magnitude < mag_below)] = 0
    tan_deg_mag[condition_2 & (magnitude < mag_above_right) & (magnitude < mag_below_left)] = 0
    tan_deg_mag[condition_3 & (magnitude < mag_left) & (magnitude < mag_right)] = 0
    tan_deg_mag[condition_4 & (magnitude < mag_above_left) & (magnitude < mag_below_right)] = 0

    return tan_deg_mag

# Applied NMS to the gradient magnitude image using the calculated gradient directions
nonMaxImg = nonMax(tan_inv_deg, magnitude)
img_X= nonMaxImg.copy()
#For number of rows and columns in an image
img_Row= img_X.shape[0]
img_Col= img_X.shape[1]
#an array is created for visited pixels
visited= np.zeros_like(img_X)
cv2.imwrite("nonMaxImg.jpg", cv2.normalize(nonMaxImg, None, 0, 255, norm_type=cv2.NORM_MINMAX))

def thresholding(nonMaxImg):
    img_max = nonMaxImg.max()
    highVal = img_max * 0.2
    lowVal = img_max * 0.07

    # Set pixels below the low value to zero
    nonMaxImg[nonMaxImg <= lowVal] = 0

    # Identify strong edges and mark them as visited
    strong_edges = nonMaxImg >= highVal
    visited = np.zeros_like(nonMaxImg)
    visited[strong_edges] = 1

    # Recursive function to trace weak edges
    def hyst(i, j):
        if 0 <= i < img_Row and 0 <= j < img_Col and visited[i][j] != 1 and nonMaxImg[i][j] >= lowVal:
            visited[i][j] = 1
            nonMaxImg[i][j] = img_max  # You can set a different value here if needed
            hyst(i - 1, j - 1)
            hyst(i - 1, j)
            hyst(i - 1, j + 1)
            hyst(i, j - 1)
            hyst(i, j + 1)
            hyst(i + 1, j - 1)
            hyst(i + 1, j)
            hyst(i + 1, j + 1)

    # Apply the recursive function to trace weak edges
    for i in range(img_Row):
        for j in range(img_Col):
            if visited[i][j] != 1 and nonMaxImg[i][j] >= highVal:
                hyst(i, j)

    # Set remaining weak edges to zero
    nonMaxImg[visited != 1] = 0

    return nonMaxImg

result = thresholding(img_X)
cv2.imwrite("thresholded_img.jpg", cv2.normalize(result, None, 0, 255, norm_type=cv2.NORM_MINMAX))
cv2.imwrite("Magnitude.jpg",cv2.normalize(magnitude,None,0,255,norm_type=cv2.NORM_MINMAX))
cv2.imwrite("HystThresholding.jpg",cv2.normalize(thresholding(nonMax(tan_inv_deg,magnitude)),None,0,255,norm_type=cv2.NORM_MINMAX))

