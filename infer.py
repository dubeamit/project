# Import libraries
import argparse
import numpy as np
from scipy.sparse import data
from PDFImage import PDFImage
from ExtractData import ExtractData
import pickle
from sklearn import linear_model, preprocessing


parser = argparse.ArgumentParser()
parser.add_argument("--pdf_path",  type=str, default='dataset/car6.pdf', help="path to the pdf file")
parser.add_argument("--model_path",  type=str, default='model_data/model.sav', help="path to the model")
args = parser.parse_args()

# Path of the pdf
pdf_file = args.pdf_path
print('file', pdf_file)

model_file = args.model_path


pdf_img = PDFImage(pdf_file)
extract_data_obj = ExtractData()

no_of_images = pdf_img.pdf_to_image()

data_dict = extract_data_obj.extract_data(no_of_images)


classes = {3:'suv', 2:'sedan', 0:'hatchback', 1:'muv'}

y = data_dict['type']
del data_dict['type']

if any(np.isnan(float(val)) for val in data_dict.values()):
    print(data_dict)
    print('Data could not be parsed')

else:
    X = list(map(float,[data_dict['height'], data_dict['length'], data_dict['width']]))
    X = np.array(X).reshape(1,3)
    # load model for inference
    model = pickle.load(open(model_file, 'rb'))
    # result = model.score(X, y)
    # print(result)
    prediction = classes[model.predict(X)[0]]
    print('prediction:', prediction)











