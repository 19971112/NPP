#import sys

f1 = open ("countrypart.txt","r")
f2 = open ("abbreviation.txt","r")

dic = {}

# 読み込んだリストのファイルを一行づづ辞書に登録

line = f1.readline()
while line:
    key = line[:line.find(",")]
    value = line[line.find(","):].lstrip(",").strip("\n")
    dic[key] = value
    line = f1.readline()
f1.close()

#　ファイルの読み込み
mystr = f2.read()
for k, v in dic.items():
    mystr = mystr.replace(k, v)

print(mystr)
