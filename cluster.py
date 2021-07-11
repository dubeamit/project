import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans



'''
use Kmeans to cluster data of different cars
helpful to generate more data since "type" column is missed during data extraction
'''

df = pd.read_csv('model_data/working_data.csv', index_col=0) # not considering type column
df = df.dropna()
# print(df)


ax = plt.axes(projection='3d')
ax.scatter3D(df['height'], df['length'], df['width'], cmap='Greens')
plt.show()

X = df[['height', 'length', 'width']].to_numpy()

Kmean = KMeans(n_clusters=4)
Kmean.fit(X)

print('centroids', Kmean.cluster_centers_)
print('labels', Kmean.labels_)

test = np.array([[1680, 4530, 1820]])
prediction = Kmean.predict(test)

print('prediction', prediction)