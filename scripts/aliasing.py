import cv2 as cv

img = cv.imread(r'C:\Users\rodri\OneDrive\Development\ArcApple\files\bad_apple_is\image_sequence\bad_apple_233.png', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
ret, thresh1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)

cv.imwrite(r'C:\Users\rodri\OneDrive\Development\ArcApple\files\bad_apple_is\image_sequence\filter\bad_apple_test.png', thresh1)