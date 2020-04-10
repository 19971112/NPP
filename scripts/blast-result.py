import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# sns.set(font='Helvetica')
l = []

# 対象ファイルの読み込み
FILE1 = "exported-feature-table.biom/table.tsv"
FILE2 = ["blast-result_Domain.tsv","blast-result_Phylum.tsv","blast-result_Class.tsv","blast-result_Order.tsv"]

#  インデックスのリストを作成
df1 = pd.read_table(FILE1,skiprows=1)
CS = list(df1.columns)
CS.remove('#OTU ID')

# blast-resultを処理
for BlastResult in FILE2:

    # 新しいデータフレームの作成
    df_new = pd.DataFrame(index=[], columns=list(df1.columns))
    df_new['#OTU ID'] = ['other']

    # 各カラムのヒット数をカウントする
    for ColumIndex in CS:

        # 各サンプルの全てのOUT数をカウント
        df1 = pd.read_table(FILE1,skiprows=1)
        df_bool1 = (df1[ColumIndex] > 0)

        # 各サンプルのアノテーションのついたOUT数をカウント
        df2 = pd.read_table(BlastResult)
        df_bool2 = (df2[ColumIndex] > 0)

        # アノテーションがつかなかったOUT数をotherとして登録
        OTHER = df_bool1.sum()-df_bool2.sum()
        df_new[ColumIndex] = [OTHER]

    # データのマージ
    df_base = pd.read_table(BlastResult)
    df_base = df_base.set_index('#OTU ID')
    df_new = df_new.set_index('#OTU ID')
    df_marge = pd.concat([df_base, df_new])

    # ファイルへ書き出し
    NAME = BlastResult + ".other.txt"
    df_marge.to_csv(NAME, sep='\t')

    # リストの定義
    l.append(NAME)
