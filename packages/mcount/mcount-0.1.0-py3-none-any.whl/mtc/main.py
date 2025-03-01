import cv2
import numpy as np
from scipy import ndimage as n
import sys
if "google.colab" in sys.modules:
    from google.colab.patches import cv2_imshow

def circle(input_image, output_image):
	# Read data
    data=cv2.imread(input_image, cv2.IMREAD_COLOR)
    
    # Data check
    if data is None:
        print(f"Error: Could not load image from '{input_image}'. Please check the file path and format")
        sys.exit(1) 
    
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
    threshold1 = 190
    threshold2 = 550
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
        print("Number of circles detected:", num_circles)
    else:
        print("No circles detected.")

    print('Cells - xcoor,ycoor,radius')
    print(circles)
        
    cv2.imwrite(output_image,image_blur)
    cv2.imshow('Transormed image',image_blur)  # Display the image with detected circles
    cv2.waitKey(0)

    
    '''Median filter applied on up-noised image gives smoother and clearer edges of the lesion circles.'''


def count():
    # Check for faulty command
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_image> <output_image>")
        return
    
    # Read command-line arguments
    input_image = sys.argv[1]  #Input image path
    output_image = sys.argv[2] if len(sys.argv) > 2 else "output.jpg"  #Output image path

    # Call the function to process the image
    circle(input_image, output_image)

if __name__ == "__main__":
    count()
