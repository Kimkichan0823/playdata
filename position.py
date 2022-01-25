import numpy as np
import pandas as pd
import cx_Oracle
from sklearn.preprocessing import Normalizer

def position():
    df=pd.read_csv('725700.csv')
    df['TOTALTEAMMATES']=df.TOTALDAMAGESHIELDEDONTEAMMATES+df.TOTALHEALSONTEAMMATES
    df['TOTALDAMAGETAKENS']=df.TOTALDAMAGETAKEN+df.SELFMITIGATEDDAMAGE
    tmp=df.groupby('CHAMPIONNAME').mean().round(0)
    tmp=tmp[['TOTALDAMAGETAKENS','TOTALDAMAGEDEALTTOCHAMPIONS','PHYSICALDAMAGEDEALTTOCHAMPIONS','MAGICDAMAGEDEALTTOCHAMPIONS','TOTALTEAMMATES']]
    target=tmp.reset_index()['CHAMPIONNAME']
    #데이터 전처리
    nom=Normalizer()
    nom.fit(tmp)
    x_nom=nom.transform(tmp)
    #표준화처리
    labels = kmeans.labels_
    df = pd.DataFrame({'target': target, 'labels': labels})
    ct = pd.crosstab(df['target'], df['labels'])
    ct.loc[ct[0]==1,0]='AD전사'
    ct.loc[ct[1]==1,0]='AP딜러'
    ct.loc[ct[2]==1,0]='유틸서폿'
    ct.loc[ct[3]==1,0]='탱커&AP전사'
    ct.loc[ct[4]==1,0]='AD딜러'
    position=position.reset_index().rename(columns={'target':'CHAMPIONNAME',0:'POSITION'})
    return position
    
    