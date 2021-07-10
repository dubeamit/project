import pytesseract
import re
import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def replace_chars(text):
    """
    Replaces all characters instead of numbers from 'text'.
    
    :param text: Text string to be filtered
    :return: Resulting number
    """
    list_of_numbers = re.findall(r'\d+', text)
    result_number = ''.join(list_of_numbers)
    return result_number


def get_binary(image):

    _, img_bin = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # if np.mean(img_bin) > 127:
    #     img_bin = cv2.bitwise_not(img_bin)
    img_bin = cv2.bitwise_not(img_bin)
    return img_bin
    
def detect(cropped_frame, is_number = False):
    if (is_number):
        text = pytesseract.image_to_string(cropped_frame, config='digits')
                                        #    config ='-c tessedit_char_whitelist=0123456789 --psm 10 --oem 2')
    else:
        text = pytesseract.image_to_string(cropped_frame)        
        
    return text


#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def erode(image):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    img_erode = cv2.erode(image, kernel, iterations = 2)
    return img_erode

def dilate(image):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    img_dilate = cv2.dilate(image, kernel, iterations = 2)
    return img_dilate


def blur(img, blur_weight=1):
    img_blurred = cv2.medianBlur(img, blur_weight)
    return img_blurred


def opening(image):
    kernel = cv2.getStructuringElement(cv2.MORPH_OPEN, (2, 2))
    img_open = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    return img_open

def show_image(image, cmap='gray'):
    plt.imshow(image, cmap=cmap)
    plt.show()



if __name__ == '__main__':
    image = cv2.imread('Images/page_4.jpg', 0)
    bin_img = get_binary(image)
    # show_image(bin_img)
    blur_img = blur(bin_img)
    # show_image(blur_img)
    erode_img = erode(blur_img)
    # show_image(erode_img)
    dilate_img = dilate(erode_img)
    # show_image(dilate_img)

    text = detect(dilate_img)
    word = ''
    for line in text.split('\n'):
        line = line.lower()
        # print('line', line)
        if ('overall length' in line or 'length' in line):
                word = ''.join(e for e in line if e.isdigit())
                print('line', line)
                print(word)

        elif ('overall width' in line or 'width' in line):
            word = ''.join(e for e in line if e.isdigit())
            print('line', line)
            print(word)

        elif ('overall height' in line or 'height' in line):
            word = ''.join(e for e in line if e.isdigit())
            print('line', line)
            print(word)




    # open_img = opening(dilate_img)
    # show_image(open_img)

