# project
## OCR on car PDF brochures to classify car

### Generating data (ocr_cars.py)
#### run `python3 ocr_cars.py` to generated data 
1. convert pdf to images
2. do OCR on images and generate text
3. write length, width, height to a csv file 

### train the model (train.py)
1. pass the working_data.csv to train.py
2. run `python3 train.py`
3. model will be saved named `model.sav`


### infer on model (infer.py)
1. pass the pdf file path and model path
2. run `python3 infer.py`
3. get predicitions 


### assignment.ipynb (use google colab for this)
In this notebook I tried to use **CascadeTabNet** [repo!](https://github.com/DevashishPrasad/CascadeTabNet) to detect tables and do ocr on it.
The purpose was to see if OCR accuracy increased. In some place it worked better than using ocr on entire image.
1. upload the data_img folder which contains few images with table in it to gdrive.
2. upload the assignment.ipynb and run all the cells
3. a csv file will be generated for each file (to generate single csv file uncomment lines 178-180, 130 & comment line 131) 


### Preprocessing 
1. **Resizing**: upscale/downscale image. Few images which were not generating data worked after upscaling
2. **Binarisation**: Thresholding the image using *Otsu's Binarization*.
3. **Blur**: smoothing the images
4. **Erosion**: erode foregroud boundaries & diminish the features of an image
5. **Dilation**: increase the object area & accentuate features


### Requirements
1. all requirements are listed in requirements.txt
2. few apt packages are include in requirements install those and remove from the requirements.txt
3. run `pip3 install -r requirements.txt`