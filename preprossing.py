import pandas as pd
import numpy as np 
import missingno as msno
import seaborn as sns
import matplotlib.pyplot as plt
import re
from sklearn.preprocessing import Imputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import neighbors


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


	max_min_scaler = lambda x : (x-np.min(x))/(np.max(x)-np.min(x))
	df['Size'] = df[['Size']].apply(max_min_scaler)
	#print(df['Genres'].head(5))
	#see the NULL data
	# msno.matrix(df)
	# plt.show()

	#To see the relationship
	# sns.pairplot(df, x_vars='Size', y_vars='User Rating Count', height=7, aspect=0.8,kind='reg')
	# plt.show()
	df['Genres'] = df['Genres'].str.replace(r"Games,", "")
	for i in range(len(df)):
		df.at[i,'Genres'] = df.iloc[i]['Genres'].split(',')[0]
	
	#for index,row in df.iterrows():
		# print(index)
	#	row['Genres']= re.findall(r"^(.+?),",row['Genres'])
		# print(row['Genres'])
# 处理类别数据 one-hot encoder
#1.类别 Primart Genre

	gen = pd.DataFrame()
	gen = pd.get_dummies(df['Genres'],prefix='Genre')
	df = pd.concat([df,gen],axis=1)
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