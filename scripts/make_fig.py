import pandas as pd

File1='file_join_1.txt'
File2='SILVA_138_Taxonomy.txt'
File3='table.tsv'



df = pd.read_table(File1, header=None)
df = df[df[2] > 90]
File4 = df.loc[:,[0,1]]
File4


df2 = pd.read_table(File2, header=None)
File5 = pd.merge(File4, df2, on=0)
File5 = File5.loc[:,['1_x','1_y']]
dic = File5.set_index('1_x')['1_y'].to_dict()
File5


df3 = pd.read_table(File3, header=0, skiprows=1)
df3 = df3.replace({'#OTU ID': dic})
#df3 = df3.replace(dic)
df3


hit_otu = df3[df3['#OTU ID'].str.contains('d__')]
hit_otu = pd.concat([hit_otu,pd.DataFrame(hit_otu.sum(axis=1),columns=['Total'])],axis=1)
hit_otu = hit_otu.sort_values(by='Total', ascending=False)
hit_otu = hit_otu.set_index('#OTU ID')

nohit_otu = df3[~df3['#OTU ID'].str.contains('d__', na = False)]
nohit_otu = nohit_otu.set_index('#OTU ID')
series_mean = nohit_otu.sum()
series_mean.name = "Unknown"
nohit_otu = nohit_otu.append(series_mean)
nohit_otu = nohit_otu['Unknown':]
nohit_otu = pd.concat([nohit_otu,pd.DataFrame(nohit_otu.sum(axis=1),columns=['Total'])],axis=1)

df_all = pd.concat([hit_otu, nohit_otu])
df_all.to_csv("table-tax.txt", sep='\t')


########################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
matplotlib.use('Agg') 
%matplotlib inline


dataset =  pd.read_table('table-tax.txt', header=0)


l_columns = list(dataset.columns)
l_columns.remove('#OTU ID')
l_columns.remove('Total')


mydict = {"domain":"; p__","phylum":"; c__", "class":"; o__", "order":"; f__", "family":"; g__", "genus":"; s__"}
list_dic = list(mydict.keys())


for iii in l_columns:
    Level_num = 0

    for ODER in list_dic:
        
        Level_num = (Level_num+ 1)
        
        df_oder = dataset.loc[:,['#OTU ID',iii]]
        KYE= mydict[ODER]
        
        df_oder[ODER]  = df_oder['#OTU ID'].str.split(pat=KYE, expand=True)[0]
        df_oder = df_oder.drop('#OTU ID', axis=1)
        df_oder = df_oder.set_index(ODER)
        df_oder = df_oder.groupby(level=0).sum()
        df_oder = df_oder.sort_values(by=iii, ascending=False)
        
        if len(df_oder) > 21:
            
            #up20 = df_oder.groupby(level=0).sum()
            up20 = df_oder[:21]
            up20 = up20.sort_values(by=iii, ascending=False)

            under20 =  df_oder[21:]
            series_mean = under20.sum()
            series_mean.name = "Other"
            under20 = under20.append(series_mean)
            under20 = under20['Other':]

            df_all = pd.concat([up20, under20])
            
            
            # データセットを100%積み上げ棒グラフように変換
            plot_dataset = pd.DataFrame(index = df_all.index)

            for col in df_all.columns:
                plot_dataset[col] = round(100 * df_all[col] / df_all[col].sum(), 1)
            
            # 積み上げ棒グラフように変換
            fig, ax = plt.subplots(figsize=(6.5, 3), dpi=300)
            for i in range(len(plot_dataset)):
                ax.bar(plot_dataset.columns, 
                plot_dataset.iloc[i], 
                bottom=plot_dataset.iloc[:i].sum()
                )
            plt.title(ODER)
            plt.subplots_adjust(left=0.1, right=0.2, bottom=0.1, top=0.9)
            ax.legend(plot_dataset.index,bbox_to_anchor=(1, 0, 0.5, 1), ncol=1, fontsize=4.8)
            
            NAME = (iii+"_"+str(Level_num)+ODER+'.png')
            plt.savefig(NAME)

        else:
            df_all = df_oder
            
             # データセットを100%積み上げ棒グラフように変換
            plot_dataset = pd.DataFrame(index = df_all.index)

            for col in df_all.columns:
                plot_dataset[col] = round(100 * df_all[col] / df_all[col].sum(), 1)
            
            # 積み上げ棒グラフように変換
            fig, ax = plt.subplots(figsize=(6.5, 3), dpi=300)
            for i in range(len(plot_dataset)):
                ax.bar(plot_dataset.columns, 
                plot_dataset.iloc[i], 
                bottom=plot_dataset.iloc[:i].sum()
                )
            plt.title(ODER)
            plt.subplots_adjust(left=0.1, right=0.2, bottom=0.1, top=0.9)
            ax.legend(plot_dataset.index,bbox_to_anchor=(1, 0, 0.5, 1), ncol=1, fontsize=4.8)
            
            NAME = (iii+"_"+str(Level_num)+ODER+'.png')
            plt.savefig(NAME)
    
