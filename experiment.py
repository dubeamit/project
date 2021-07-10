
import sys
import numpy as np
import cv2
import os
import pytesseract
import matplotlib.pyplot as plt
import preprocessing
from pytesseract import Output


def get_string(img_path):
    # Read image using opencv
    img = cv2.imread(img_path)
    scale_percent = 200 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
  
# resize image
    # img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    # img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    # plt.imshow(img, cmap='gray')
    # plt.show()
    
   # Extract the file name without the file extension
    file_name = os.path.basename(img_path).split('.')[0]
    file_name = file_name.split()[0]
    # Create a directory for outputs
    output_path = os.path.join('output_path', "ocr")
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # Rescale the image, if needed.
    # img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    # Converting to gray scale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = preprocessing.get_binary(img)
    img = preprocessing.blur(img)
    # img = cv2.GaussianBlur(img, (3, 3), 0)
    img = preprocessing.erode(img)
    img = preprocessing.dilate(img)
    img = preprocessing.opening(img)
    # img = cv2.GaussianBlur(img, (3, 3), 0)


    #Removing Shadows
    # rgb_planes = cv2.split(img)
    # result_planes = []
    # result_norm_planes = []
    # for plane in rgb_planes:
    #     img = preprocessing.get_binary(plane)
    #     # img = preprocessing.erode(img)
    #     img = preprocessing.dilate(img)
    #     img = preprocessing.blur(img)

    #     # diff_img = 255 - cv2.absdiff(plane, bg_img)

    #     # img = preprocessing.get_binary(plane)
    #     # img = preprocessing.blur(img)
    #     # img = preprocessing.erode(img)
    #     # img = preprocessing.dilate(img)

    #     result_planes.append(img)
    # img = cv2.merge(result_planes)
    # img = (255-img)
    # plt.imshow(img, cmap='gray')
    # plt.show()
    #Apply dilation and erosion to remove some noise
    # img = preprocessing.dilate(img)
    # plt.imshow(img, cmap='gray')
    # plt.show()
    # img = preprocessing.erode(img)
    # img = cv2.GaussianBlur(img, (7, 7), 0)
    # img = preprocessing.blur(img)
    # img = preprocessing.erode(img)
    # img = preprocessing.dilate(img)
    # plt.imshow(img, cmap='gray')
    # plt.show()

    # kernel = np.ones((1, 1), np.uint8)
    # img = cv2.dilate(img, kernel, iterations=1)#increases the white region in the image 
    # img = cv2.erode(img, kernel, iterations=1) #erodes away the boundaries of foreground object
    # plt.imshow(img, cmap='gray')
    # plt.show()
    #Apply blur to smooth out the edges
    # img = cv2.GaussianBlur(img, (5, 5), 0)
    
   
    
   
    
     # Apply threshold to get image with only b&w (binarization)
    # img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # img = preprocessing.get_binary(img)
    # plt.imshow(img, cmap='gray')
    # plt.show()
    #Save the filtered image in the output directory
    # save_path = os.path.join(output_path, file_name + "_filter_" + str('as') + ".png")
    # cv2.imwrite(save_path, img)
    # Recognize text with tesseract for python

    # contours, hierarchy = cv2.findContours(
    # img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # for cnt in contours:
    #     x, y, w, h = cv2.boundingRect(cnt)
    #     # bounding the images
    #     if y < 300:
    #         table_image = cv2.rectangle(img_og, (x, y), (x + w, y + h), (0, 0, 255), 1)

    #         plt.imshow(table_image)
    #         plt.show()
    #         cv2.namedWindow('detecttable', cv2.WINDOW_NORMAL)

    data_text = str(pytesseract.image_to_string(img))
    # results = pytesseract.image_to_data(img, output_type=Output.DICT)
    # for i in range(0, len(results["text"])):
    #     # extract the bounding box coordinates of the text region from
    #     # the current result
    #     x = results["left"][i]
    #     y = results["top"][i]
    #     w = results["width"][i]
    #     h = results["height"][i]
    #     # extract the OCR text itself along with the confidence of the
    #     # text localization
    #     text = results["text"][i]
    #     conf = int(results["conf"][i])
    #     if conf > 50:
    #         # display the confidence and text to our terminal
    #         print("Confidence: {}".format(conf))
    #         print("Text: {}".format(text))
    #         print("")
    #         # strip out non-ASCII text so we can draw the text on the image
    #         # using OpenCV, then draw a bounding box around the text along
    #         # with the text itself
    #         text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
    #         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #         cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
    #            1.2, (0, 0, 255), 3)

    return data_text


text = get_string('Images/page_1.jpg')
# text = get_string('Images/page_6.jpg')

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
    
    elif 'length x width x height' in line:
        print('line', line)
        word = ''.join(e for e in line if e.isdigit())
        print('yo', word[:4],' ', word[4:8], ' ', word[8:12])


