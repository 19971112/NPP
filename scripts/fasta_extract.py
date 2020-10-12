#!/usr/bin/env python
# -*- coding: utf-8 -*-

#fasta_id項目をkeyにして、hitした配列を標準出力へ

import sys
from Bio import SeqIO


fasta_in = sys.argv[1]                            #１番目の引数には、変更したいfastaファイルを指定する。
query = sys.argv[2]                          #２番目の引数に 1行毎に　keyIDを記述したファイルを指定


for record in SeqIO.parse(fasta_in, 'fasta'): #fastaファイルを開くSeqIOを使ってパースする(1項目づつ読み込む）
    id_part = record.id                       #fastaのID部分を読み込む
    m_part = id_part.rstrip()        #chompしてm_partにいれる
    description_part = record.description
    seq = record.seq                          #fastanの配列部分を読み込む
    for q in open(query, "r"):                     #アノテーション情報ファイルを開く
        if m_part == q.rstrip():            #fastaファイルのidとchanger項目のid部分が一致したら。。
            fasta_seq = '>' + description_part + '\n' + seq      #fasta形式に整えて
            print(fasta_seq)                  #標準出力にfastaを出力
