import pandas as pd
cols = ['code', 'date', 'sz', 'pgs','pgj','fh']
df = pd.read_csv('d:\\full.csv', names=cols, index_col=[0,1])

fqraw = df.ix['SZ000001'].sort_index(ascending=False)


data_df = pd.read_csv('d:\gitlocal\easydata_test\day\data\sz000001.csv',index_col='date')

dr = pd.date_range('1991-04-03', '2016-04-25',freq='D')
drstr =dr.format('YY-mm-dd')

data_df2 = data_df.reindex(drstr, method='bfill')

data_df2 = data_df2.sort_index(ascending=False)

data_df2['lastclose'] = data_df2['close'].shift(-1)

data_df2.loc[:, ['close','lastclose']]

fq_with_close = pd.merge(fqraw, data_df2.loc[:,['close','lastclose']],  how='left', left_index=True, right_index=True )

fq_with_close['factor'] = (1+fq_with_close['sz'])*(fq_with_close['lastclose']/((fq_with_close['lastclose']+fq_with_close['pgs']*fq_with_close['pgj'])/(1+fq_with_close['pgj'])) * (fq_with_close['lastclose']/(fq_with_close['lastclose']-fq_with_close['fh'])))





data_df_with_fq = pd.merge(data_df, fqraw, how='left', left_index=True, right_index=True )

data_df_with_fq['lastclose'] = data_df_with_fq['close'].shift(1)

data_df_with_fq.loc[:, ['close','lastclose']]


cacl_fq_factor(data_df_with_fq)

def cacl_fq_factor():
    pass

