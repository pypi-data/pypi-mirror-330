import cv2
import numpy as np
from scipy import ndimage as n
import os
import sys
if "google.colab" in sys.modules:
    from google.colab.patches import cv2_imshow

def circle(input_image:str, output_image:str=None, alpha:int=190, beta:int=550):
	
    if not os.path.exists(input_image):
        raise FileNotFoundError(f"Error: The file '{input_image}' does not exist.")
    
    if not output_image:
        output_dir = "results"  # Save all images in 'results' folder
        os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
        output_image = os.path.join(output_dir, "output.jpg")
        print(f"⚠ No output path provided. Saving to default: {output_image}")
        
    # Read the image
    data = cv2.imread(input_image, cv2.IMREAD_COLOR)
    
    # Validate
    if data is None:
        raise ValueError(f"Error: '{input_image}' is not a valid image file or cannot be opened.")
        
    #===================================================TEST
    # #Gaussian filter
    # gauss=n.gaussian_filter(data,sigma=3)
    # cv2_imshow(gauss)
    
    # #median filter
    # median=n.median_filter(data,size=3)
    # cv2_imshow(median)
    
    # #Denoised image
    # denoised_img=cv2.fastNlMeansDenoising(data,None,h=10,templateWindowSize=7,searchWindowSize=21)
    # cv2.imwrite('denoised_image.png',denoised_img),
    # cv2_imshow(denoised_img)
    #==================================================
    
    gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
    
    # Add Gaussian noise to the image
    mean = 0
    stddev =0.8  # Adjust the standard deviation to control the intensity of the noise
    gaussian_noise = np.random.normal(mean, stddev, gray.shape).astype(np.uint8)
    noisy_gray=cv2.add(gray, gaussian_noise)
    noise2=np.random.normal(mean, stddev, data.shape).astype(np.uint8)
    noisy_rgb = cv2.add(data, noise2)   
    
    #Applying median filter of up-noised image
    up_median=n.median_filter(noisy_gray,size=4)
    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(data, kernel, iterations=1)
    den_img=cv2.fastNlMeansDenoising(erosion,None,h=10,templateWindowSize=7,searchWindowSize=21)
    
    #Gray scaling image
    gray = cv2.cvtColor(den_img, cv2.COLOR_BGR2GRAY)
    
    #Canny edging
    threshold1 = alpha
    threshold2 = beta
    edges = cv2.Canny(gray, threshold1, threshold2)
    
    image_blur = cv2.GaussianBlur(edges, (5, 5), 0)
    
    # Apply Hough Circle Transform
    circles = cv2.HoughCircles(image_blur, cv2.HOUGH_GRADIENT, dp=1, minDist=50,
                             param1=50, param2=30, minRadius=10, maxRadius=100)
  
  # Check if any circles were detected
    if circles is not None:
        # Convert the coordinates and radius to integers
        circles = np.round(circles[0, :]).astype(int)
    
        # Count the number of circles
        num_circles = len(circles)
        print("Number of metastatic cells detected:", num_circles)
    else:
        print("No circles detected.")

    print('Cells - x-coor,y-coor,radius')
    print(circles)
        
    cv2.imwrite(output_image,image_blur)
    cv2.imshow('Transormed image',image_blur)  # Display the image with detected circles
    cv2.waitKey(0)
    cv2.destroyAllWindows() 
    
    return circles
    
    '''Median filter applied on up-noised image gives smoother and clearer edges of the lesion circles.'''
