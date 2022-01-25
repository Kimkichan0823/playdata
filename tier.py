import numpy as np
import pandas as pd

def tier():
    df=pd.read_csv('725700.csv')
    tmp=df[['CHAMPIONNAME','WIN','KILLS','DEATHS','ASSISTS','TOTALDAMAGEDEALTTOCHAMPIONS',
             'TOTALDAMAGETAKEN','TOTALDAMAGESHIELDEDONTEAMMATES','TOTALHEALSONTEAMMATES',
                    'SELFMITIGATEDDAMAGE','TOTALTIMECCDEALT','LARGESTKILLINGSPREE','GOLDEARNED']]
    tmp['TOTALDAMETAKENS']=tmp.TOTALDAMAGETAKEN+tmp.SELFMITIGATEDDAMAGE
    tmp['WIN']=tmp.apply(lambda x:1 if x['WIN']=='True' else 0,axis=1)
    cnt=tmp.groupby('CHAMPIONNAME').sum()
    cnt=cnt.reset_index()
    cnt=cnt[['CHAMPIONNAME','WIN']]
    cnt=cnt.rename({'WIN':'CNT'},axis='columns')
    cnt['PICK']=round((cnt.CNT/sum(cnt['CNT'])*100),2)
    #해당 챔피언이 플레이 할 확률인 'PICK' 컬럼을 만듬
    
    tmp=tmp.groupby('CHAMPIONNAME').mean().round(4)
    tmp['WIN']=tmp.WIN*100
    tmp=tmp.drop(['TOTALDAMAGETAKEN','TOTALHEALSONTEAMMATES','TOTALDAMAGESHIELDEDONTEAMMATES','SELFMITIGATEDDAMAGE'],axis=1)
    tmp['KDA']=round((tmp.KILLS+tmp.ASSISTS)/tmp.DEATHS,2)
    tmp=tmp.drop(['KILLS','DEATHS','ASSISTS'],axis=1)
    tmp=tmp.reset_index()
    tmp=pd.merge(tmp,cnt,on='CHAMPIONNAME')
    #해당 챔피언의 킬,데스,어시스트의 비율인 'KDA' 컬럼을 만듬
    
    x_data=tmp[['PICK','WIN','KDA']]
    data=x_data.values
    kmeans=KMeans(n_clusters=5,random_state=10).fit(data)
    result=tmp[['CHAMPIONNAME','PICK','WIN','KDA']]
    result['cluster']=kmeans.labels_
    #비지도학습으로 훈련시킨뒤 한눈에 보기 좋게 result 데이터프레임에 컬럼을 넣어 비교함
    
    result.loc[result.cluster==0,'cluster']='2티어'
    result.loc[result.cluster==1,'cluster']='4티어'
    result.loc[result.cluster==2,'cluster']='3티어'
    result.loc[result.cluster==3,'cluster']='1티어'
    result.loc[result.cluster==4,'cluster']='5티어'

    result.loc[result.cluster=='1티어','cluster']=1
    result.loc[result.cluster=='2티어','cluster']=2
    result.loc[result.cluster=='3티어','cluster']=3
    result.loc[result.cluster=='4티어','cluster']=4
    result.loc[result.cluster=='5티어','cluster']=5
    
    return result