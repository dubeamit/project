import pandas as pd
import pickle
from sklearn import linear_model, preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import sys


# Load data
df = pd.read_csv('model_data/working_data.csv')

# drop NaN
df = df.dropna()

X = df[['height', 'length', 'width']].to_numpy()

# print(df['type'].unique())

# label_encoder object knows how to understand word labels.
label_encoder = preprocessing.LabelEncoder()
# encode label type
df['type']= label_encoder.fit_transform(df['type'])
# print(df['type'].unique())
y = df['type'].to_numpy()

# print(X)
# print(Y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

# Fit (train) the Logistic Regression classifier
model = linear_model.LogisticRegression(C=1e40, solver='newton-cg')
fitted_model = model.fit(X_train, y_train)

filename = 'model.sav'
pickle.dump(model, open(filename, 'wb'))

# threshold = 0.5
# print(X_test)
# print(y_test)
y_pred = model.predict(X_test)
print('predictions', y_pred)

print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(model.score(X_test, y_test)))

print(classification_report(y_test, y_pred))


