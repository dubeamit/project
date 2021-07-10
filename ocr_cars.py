# Import libraries
from PIL import Image
import cv2
import pytesseract
import sys
from pdf2image import convert_from_path
import os
import csv
import preprocessing



def get_info(line):
    print(line)
    word = ''.join(e for e in line if e.isdigit())
    if word:
        word = word[:4]
        return word
    return 'NaN'


pdf_files = os.listdir('diff_format')
fields = ['type', 'height', 'length', 'width']
outfile = "data.csv"
with open(outfile, 'a') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = fields)
    writer.writeheader()

# Path of the pdf
for pdf_file in pdf_files:
    PDF_file = 'diff_format/{}'.format(pdf_file)#"dataset/car3.pdf"
    # PDF_file = "dataset/car47.pdf"
    print('file', PDF_file)


    '''
    Part #1 : Converting PDF to images
    '''

    # Store all the pages of the PDF in a variable
    pages = convert_from_path(PDF_file, 500)

    # Counter to store images of each page of PDF to image
    image_counter = 1
    # Iterate through all the pages stored above
    for page in pages:

        # Declaring filename for each page of PDF as JPG
        # For each page, filename will be:
        # PDF page 1 -> page_1.jpg
        # PDF page 2 -> page_2.jpg
        # PDF page 3 -> page_3.jpg
        # ....
        # PDF page n -> page_n.jpg
        filename = "page_"+str(image_counter)+".jpg"
        
        # Save the image of the page in system
        page.save(filename, 'JPEG')
        # im = Image.open(filename)
        # im.show()
        # sys.exit()

        # Increment the counter to update filename
        image_counter = image_counter + 1

    '''
    Part #2 - Recognizing text from the images using OCR
    '''
    del pages
    # Variable to get count of total number of pages
    filelimit = image_counter-1

    # Creating a text file to write the output
    # outfile = PDF_file.replace('.pdf', '.csv')#"out_text.txt"

    data_dict = {}
    # Open the file in append mode so that
    # All contents of all images are added to the same file
    # f = open(outfile, "a")
    data_dict['type'] = 'NaN'
    data_dict['length'] = 'NaN'
    data_dict['width'] = 'NaN'
    data_dict['height'] = 'NaN'
    
    # Iterate from 1 to total number of pages
    for i in range(1, filelimit + 1):
        # write_text = []

        # Set filename to recognize text from
        # Again, these files will be:
        # page_1.jpg
        # page_2.jpg
        # ....
        # page_n.jpg
        filename = "page_"+str(i)+".jpg"
            
        # Recognize the text as string in image using pytesserct
        # text = str(((pytesseract.image_to_string(Image.open(filename)))))
        #grayscale image
        img = cv2.imread(filename, 0)
        img = preprocessing.get_binary(img)
        img = preprocessing.blur(img)
        img = preprocessing.erode(img)
        img = preprocessing.dilate(img)
        # img = preprocessing.opening(img)
        text = str((pytesseract.image_to_string(img)))

        # The recognized text is stored in variable text
        # Any string processing may be applied on text
        # Here, basic formatting has been done:
        # In many PDFs, at line ending, if a word can't
        # be written fully, a 'hyphen' is added.
        # The rest of the word is written in the next line
        # Eg: This is a sample text this word here GeeksF-
        # orGeeks is half on first line, remaining on next.
        # To remove this, we replace every '-\n' to ''.
        text = text.replace('-\n', '')	
        if data_dict['type'] == 'NaN':
            if 'suv' in text.lower():
                data_dict['type'] = 'suv'

            elif 'sedan' in text.lower():
                data_dict['type'] = 'sedan'

            elif 'hatchback' in text.lower():
                data_dict['type'] = 'hatchback'

            elif 'muv' in text.lower():
                data_dict['type'] = 'muv'


        for word in text.split('\n'):
            word = word.lower()
            # print(word)
            if 'length x width x height' in word: 
                print('line', word)
                word = word[word.find('length x width x height')+23:]
                data = ''.join(e for e in word if e.isdigit())
                try:
                    data_dict['length'] = data[:4]
                    data_dict['width'] = data[4:8]
                    data_dict['height'] = data[8:12]
                except:
                    pass

            elif ('overall length' in word or 'length' in word) and (data_dict['length'] == 'NaN' or len(data_dict['length']) < 4):
                data_dict['length'] = get_info(word)

            elif ('overall width' in word or 'width' in word) and (data_dict['width'] == 'NaN' or len(data_dict['length']) < 4):
                data_dict['width'] = get_info(word)

            elif ('overall height' in word or 'height' in word) and (data_dict['height'] == 'NaN' or len(data_dict['length']) < 4):
                data_dict['height'] = get_info(word)

            elif 'l x w x h' in word:
                print('line', word)
                word = word[word.find('l x w x h')+9:]
                data = ''.join(e for e in word if e.isdigit())
                try:
                    data_dict['length'] = data[:4]
                    data_dict['width'] = data[4:8]
                    data_dict['height'] = data[8:12]
                except:
                    pass


    print('data_dict', data_dict)
    with open(outfile, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        writer.writerow(data_dict) 


    del text
    os.system('rm *.jpg')
    # sys.exit()

