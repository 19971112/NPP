import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
#%matplotlib inline
import seaborn as sns
import sys

PREFIX = sys.argv[1]
File1 = sys.argv[2]
File2 = sys.argv[3]


# ファイルの読み込み
df = pd.read_table(File1, header=None)
print(df.duplicated().value_counts())

# 処理1　類似性が85%以上のものを抽出
identity = 85
df_hit = df[df[2] > identity]
df_hit = df_hit.loc[:,[1,0]]
df_hit = df_hit[~df_hit.duplicated()]
df_hit.columns = ['query', '#OTU ID']
print(df_hit.duplicated().value_counts())

df2 = pd.read_table(File2, usecols=[0], header=None)
df2.columns = ['query']
print(df2.duplicated().value_counts())


df_marge = pd.merge(df_hit, df2, on='query', how='right')
df_marge = df_marge.fillna("Unknown;Unknown;Unknown;Unknown;Unknown;Unknown;Unknown")
print(df_marge.duplicated().value_counts())


df_barplot = df_marge.loc[:,["#OTU ID"]]
# df_barplot['LEVEL'] = df_barplot['anote'].str.split(pat=';', expand=True)[5]
df_barplot[PREFIX] = 1
df_barplot = df_barplot.set_index('#OTU ID')
# df_barplot.drop('anote', axis=1)
# #df_barplot = df_barplot.set_index('LEVEL')
df_barplot = df_barplot.groupby(level=0).sum()

# 書き出し
file_name = PREFIX + '_tax.tsv'
df_barplot.to_csv(file_name, sep='\t')

# 各レベルのfigを一括で描画する

def make_barplot(FILE, ID, LEVEL):

    # ファイルの読み込みと対象列の抽出
    dataset =  pd.read_table(FILE, header=0)
    dataset = dataset[['#OTU ID',ID]]

    #任意のレベルでソートする
    dataset['LEVEL']  = dataset['#OTU ID'].str.split(pat=';', expand=True)[ LEVEL]
    dataset = dataset.drop('#OTU ID', axis=1)
    dataset = dataset.set_index('LEVEL')
    dataset = dataset[dataset[ID] != 0]

    # インデックスでリード数を合計して，降順に並べる
    dataset = dataset.groupby(level=0).sum()
    dataset = pd.concat([dataset, pd.DataFrame(dataset.sum(axis=1),columns=['Total'])],axis=1)
    dataset = dataset.sort_values('Total', ascending=False)
    dataset = dataset.drop('Total', axis=1)

    # Unknownのリストを一番最後に持ってくる
    col = list(dataset.index)
    col.remove('Unknown')
    col.append('Unknown')
    dataset = dataset.loc[col]
    # d__Unknown; p__Unknown; c__Unknown; o__Unknown; f__Unknown; g__Unknown; s__Unknown

    # 長いリストを短くする
    up20 = dataset[:21]
    under20 =  dataset[22:]
    series_mean = under20.sum()
    series_mean.name = "Other"
    under20 = under20.append(series_mean)
    under20 = under20['Other':]
    dataset = pd.concat([up20, under20])
    dataset = dataset[dataset[ID] != 0]

    # データセットを100%積み上げ棒グラフ用に変換
    plot_dataset = pd.DataFrame(index = dataset.index)
    for col in dataset.columns:
        plot_dataset[col] = round(100 * dataset[col] / dataset[col].sum(), 1)

    # LEVEL番号と対応する階級を置換する
    dic = {0:"domain", 1:"phylum", 2:"class", 3:"order", 4:"family", 5:"genus", 6:"species"}
    LEVEL_name = dic[LEVEL]

    # グラフのプロット
    fig, ax = plt.subplots(figsize=(2.5, 3), dpi=300)
    for i in range(len(plot_dataset)):
        ax.bar(plot_dataset.columns,
        plot_dataset.iloc[i],
        bottom=plot_dataset.iloc[:i].sum()
        )
    plt.title(LEVEL_name)
    plt.ylim(0, 100)
    plt.subplots_adjust(left=0.2, right=0.3, bottom=0.1, top=0.9)
    ax.legend(plot_dataset.index,bbox_to_anchor=(1, 0, 0.5, 1), ncol=1, fontsize=4)
    # ファイルの保存
    NAME = (ID+"_"+str(LEVEL)+LEVEL_name+'.png')
    plt.savefig(NAME)

    return print( 'Output file:   ' + NAME)

dataset =  pd.read_table(file_name, header=0, index_col=0)
l_columns = list(dataset.columns)

# 全てのリストを作成する
for ii in l_columns:
    for iii in range(6):
        make_barplot(file_name, ii , iii)
