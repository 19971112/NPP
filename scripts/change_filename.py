import os
import sys
import glob
import re


LIST = sys.argv[1]
FILE = sys.argv[2]

# LIST = "rename.txt"
# FILE = "*.txt"

#　対象のファイルを
l = glob.glob(FILE)

# 読み込んだリストのファイルを一行づづ辞書に登録
mydict = {"Wz|ZNt2&|pw$":"Wz|ZNt2&|pw$"}
f = open(LIST)
line = f.readline()
while line:
    before = line[:line.find("\t")]
    after = line[line.find("\t"):]
    after = after.lstrip("\t")
    after = after.strip("\n")
    mydict[before] = after
    line = f.readline()
f.close()

# ファイル名を置換する
for i in l:
    if (i in mydict) == True:
        print(mydict[i])
        os.rename( i, mydict[i])
    else:
        print("\"" + i + "\" is not exist")
    #os.rename( i, mydict[i])
