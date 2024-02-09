import pandas as pd
import matplotlib.pyplot as plt
from pylab import rcParams
import numpy as np
import seaborn as sns
import os

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.model_selection import cross_validate,GridSearchCV
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
#from sklearn.feature_extraction import DictVectorizer
#from sklearn.utils.multiclass import unique_labels
# import scikitplot as skplt
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from mpl_toolkits.mplot3d import Axes3D

import warnings
warnings.filterwarnings('ignore')
#%matplotlib inline

os.chdir(r'N:\STOCK ADVISOR BOT')
Stock = pd.read_csv('IBM.csv')
#best features
features_selected = ['Open','High', 'Low','QQQ_Close', 'SnP_Close', 'DJIA_Close', 'Close(t)']
df_Stock = Stock[features_selected]
df_Stock = df_Stock.iloc[:-100, :]
df_Stock = df_Stock.rename(columns={'Close(t)':'Close'})

df_Stock['Diff'] = df_Stock['Close'] - df_Stock['Open']
df_Stock['High-low'] = df_Stock['High'] - df_Stock['Low']

df_Stock.head()
######

def prepare_lagged_features(df_Stock, lag_stock, lag_index):
    print('Preparing Lagged Features for Stock, Index Funds.....')
    lags = range(1, lag_stock + 1)
    lag_cols = ['Close']
    df_Stock = df_Stock.assign(**{
        '{}(t-{})'.format(col, l): df_Stock[col].shift(l)
        for l in lags
        for col in lag_cols
    })

    lags = range(1, lag_index + 1)
    lag_cols = ['QQQ_Close', 'SnP_Close', 'DJIA_Close']
    df_Stock = df_Stock.assign(**{
        '{}(t-{})'.format(col, l): df_Stock[col].shift(l)
        for l in lags
        for col in lag_cols
    })

    df_Stock = df_Stock.drop(columns=lag_cols)

    remove_lags_na = max(lag_stock, lag_index) + 1
    print('Removing NAN rows - ', str(remove_lags_na))
    df_Stock = df_Stock.iloc[remove_lags_na:, ]
    return df_Stock