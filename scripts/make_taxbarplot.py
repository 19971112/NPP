import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
#%matplotlib inline
import seaborn as sns
import sys

PREFIX = sys.argv[1]
File1 = 'rename_' + PREFIX + '.txt'
File2 = 'blastn-' + PREFIX + '.trimmed.porechop_-SILVA_138_SSURef_NR99_tax_silva.fasta-header'


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
df_marge = df_marge.fillna("d__Other; p__Other; c__Other; o__Other; f__Other; g__Other; s__Other")

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
