
import cv2
import pytesseract
import os
import preprocessing
import matplotlib.pyplot as plt

class ExtractData:
    def __init__(self):
        self.data_dict = {}
        self.data_dict['type'] = 'NaN'
        self.data_dict['length'] = 'NaN'
        self.data_dict['width'] = 'NaN'
        self.data_dict['height'] = 'NaN'

    def get_info(self, line):
        # print(line)
        word = ''.join(e for e in line if e.isdigit())
        if word:
            word = word[:4]
            return word
        return 'NaN'

    def extract_data(self, filelimit):
        for i in range(1, filelimit):

            # Set filename to recognize text from
            # Again, these files will be:
            # page_1.jpg
            # page_2.jpg
            # ....
            # page_n.jpg
            filename = "page_"+str(i)+".jpg"
                
            #grayscale image
            img = cv2.imread(filename, 0)
            # plt.imshow(img, cmap='gray')
            # plt.show()

            img = preprocessing.get_binary(img)
            img = preprocessing.blur(img)
            img = preprocessing.erode(img)
            img = preprocessing.dilate(img)
            
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
            if self.data_dict['type'] == 'NaN':
                if 'suv' in text.lower():
                    self.data_dict['type'] = 'suv'

                elif 'sedan' in text.lower():
                    self.data_dict['type'] = 'sedan'

                elif 'hatchback' in text.lower():
                    self.data_dict['type'] = 'hatchback'

                elif 'muv' in text.lower():
                    self.data_dict['type'] = 'muv'


            for word in text.split('\n'):
                word = word.lower()
                # print(word)
                if 'length x width x height' in word: 
                    print('line', word)
                    word = word[word.find('length x width x height')+23:]
                    data = ''.join(e for e in word if e.isdigit())
                    try:
                        self.data_dict['length'] = data[:4] if data[:4] else 'NaN'
                        self.data_dict['width'] = data[4:8] if data[4:8] else 'NaN'
                        self.data_dict['height'] = data[8:12] if data[812] else 'NaN'
                    except:
                        pass

                elif ('overall length' in word or 'length' in word) and (self.data_dict['length'] == 'NaN' or len(self.data_dict['length']) < 4):
                    self.data_dict['length'] = self.get_info(word)

                elif ('overall width' in word or 'width' in word) and (self.data_dict['width'] == 'NaN' or len(self.data_dict['length']) < 4):
                    self.data_dict['width'] = self.get_info(word)

                elif ('overall height' in word or 'height' in word) and (self.data_dict['height'] == 'NaN' or len(self.data_dict['length']) < 4):
                    self.data_dict['height'] = self.get_info(word)

                elif 'l x w x h' in word:
                    print('line', word)
                    word = word[word.find('l x w x h')+9:]
                    data = ''.join(e for e in word if e.isdigit())
                    try:
                        self.data_dict['length'] = data[:4] if data[:4] else 'NaN'
                        self.data_dict['width'] = data[4:8] if data[4:8] else 'NaN'
                        self.data_dict['height'] = data[8:12] if data[812] else 'NaN'
                    except:
                        pass



        # remove all images
        os.system('rm *.jpg')
        return self.data_dict

