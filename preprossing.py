import pandas as pd
import numpy as np 
import missingno as msno
import matplotlib.pyplot as plt
import re
from sklearn.preprocessing import Imputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import neighbors

def f(x):
    aa = x.index(",")
    return x[:aa]
def y(x):
	return str(x)+','

def pre():
	df = pd.read_csv('appstore_games.csv',thousands = ',')
	df.drop(['URL','User Rating Count','Name','In-app Purchases',\
		'Description','Subtitle','Icon URL','Original Release Date',\
		'Current Version Release Date','Languages','Primary Genre'], axis=1, inplace=True)

	#delete NULL rating
	a=[]
	for index,row in df.iterrows():
		if np.isnan(row['Average User Rating'])==True:
			a.append(index)
	b=a[::-1]
	df = df.drop(df.index[b],axis=0)


	max_min_scaler = lambda x : x/1000000
	df['Size'] = df[['Size']].apply(max_min_scaler)
	#print(df['Genres'].head(5))
	#see the NULL data
	# msno.matrix(df)
	# plt.show()

	df['Genres'] = df['Genres'].str.replace(r"Games,", "")
	df["Genres"] = df["Genres"].apply(y)
	df["Genres"] = df["Genres"].apply(f)


# 处理类别数据 one-hot encoder
#1.类别 Genres

	gen = pd.DataFrame()
	gen = pd.get_dummies(df['Genres'],prefix='Genre')
	# print(gen.to_string())
	df = pd.concat([df,gen],axis=1)
	# print(df.head().to_string())
#2.Age rating
	age = pd.DataFrame()
	age = pd.get_dummies(df['Age Rating'],prefix='Age')
	df = pd.concat([df,age],axis=1)

	df.to_csv(r'./newdata.csv',index=False,sep=',')	
def ml():
	feature_cols = ['User Rating Count', 'Price', 'Size']
	x = df[feature_cols]
	y = df['Average User Rating']
	# print(y.shape)

	x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)
	print(type(x_test))
	linreg = neighbors.KNeighborsRegressor()
	linreg.fit(x_train, y_train)
	my_test = np.array([[float(284),float(1.99),float(12328960)]])
	y_pred = linreg.predict(my_test)
	print(y_pred)


if __name__ == "__main__":
	pre()
    # ml()
