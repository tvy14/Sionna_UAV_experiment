import cv2
import numpy as np
import sys
from PIL import Image  
import time
def calculate_psnr(img1, img2):
    # Read the images
    #img1 = cv2.imread(img1)
    #img2 = cv2.imread(img2)
    #print(img1.shape)
    #print(img2.shape)
    height, width, channels = img1.shape
    height2, width2, channels = img2.shape
    if height!=height2 or width!=width2:
        img2= cv2.resize(img2, (width, height))
    # Calculate the MSE (Mean Squared Error)
    #img1=np.asarray(img1)
    #img2=np.asarray(img2)
    mse = np.mean((img1 - img2) ** 2)
    #print((img1-img2).shape)
    
    # Calculate the maximum pixel value
    max_pixel = 255.0

    # Calculate the PSNR using the MSE and maximum pixel value
    psnr = 10 * np.log10(max_pixel**2 / mse)

    return psnr

def calculate_file_size(image):
    # Convert the image to bytes
    image_bytes = cv2.imencode('.jpg', image)[1].tobytes()

    # Get the size of the image data in bytes
    file_size = sys.getsizeof(image_bytes)
    
    # Convert bytes to kilobytes (KB)
    file_size_kb = file_size / 1024
    
    return file_size_kb

# Path to the two images you want to compare
image_path1 = 'IMG_4335.jpeg'
#image_path2 = 'resized_kumamoto.jpg'

origin_image=cv2.imread(image_path1)
height, width, channels = origin_image.shape
img_size=calculate_file_size(origin_image)
print("original image size:{} KB".format(img_size))
current_time=time.time()
for i in range (0,9):
    #--------------------------
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90-i*10]
    result, new_image = cv2.imencode('.jpg', origin_image, encode_param)
    #new_image = np.fromstring(new_image, dtype='uint8')
    new_image = np.frombuffer(new_image, np.uint8)
    new_image=cv2.imdecode(new_image,1)
    
    #--------------------------

    #--------------------------
    # ratio=1+i
    # new_width = int(width/ratio)
    # new_height = int(height/ratio)
    # new_image = cv2.resize(origin_image, (new_width, new_height))
    #---------------------------

    # Calculate the PSNR
    psnr_value = calculate_psnr(origin_image, new_image)
    image_size=calculate_file_size(new_image)
    #print("Compress ratio:{}, PSNR:{} dB, Size:{} KB".format(ratio, psnr_value, image_size))
    print("Qiality:{}, PSNR:{} dB, Size:{} KB".format(encode_param[1], psnr_value, image_size))


    # 讓視窗可以自由縮放大小
    cv2.namedWindow('My Image', cv2.WINDOW_NORMAL)

    # 文字
    text = "{:.2f} dB".format(psnr_value)
    # 使用各種字體
    # cv2.putText(影像, 文字, 座標, 字型, 大小, 顏色, 線條寬度, 線條種類)
    cv2.putText(new_image, text, (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3, cv2.LINE_AA)

    
    cv2.imshow('My Image', new_image)
    cv2.resizeWindow('My Image',int(width/4),int(height/4))
    ##cv2.resizeWindow('My Image',width,height)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
end_time=time.time()
used_time=end_time-current_time
print("used_time:{}s".format(used_time))
print("time per frame:{}s".format(used_time/9))

