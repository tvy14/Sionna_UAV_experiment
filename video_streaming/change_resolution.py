import cv2
old_image_name = "image_name.jpg"
image = cv2.imread(old_image_name)
if image is not None:
    height, width, channels = image.shape
    print(height, width, channels)
    ratio=8
    new_width = int(width/ratio)
    new_height = int(height/ratio)
    resized_image = cv2.resize(image, (new_width, new_height))
    cv2.imshow("Resized Image", resized_image)
    cv2.waitKey(0)
    new_image_name = "resized_"+old_image_name  # Provide the desired name for the new image
    cv2.imwrite(new_image_name, resized_image)
    print("Resized image saved as", new_image_name)
    # Image loaded successfully
    # Perform the resolution change
    # ...
else:
    print("Failed to load the image. Please check the image name and path.")
