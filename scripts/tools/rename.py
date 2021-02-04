import sys

LIST = sys.argv[1]
IN = sys.argv[2]

mydict = {"BJBU01000001-BJBU01000045.txt":"Geobacter_sp._SbR"}
mydict["BJBV01000001-BJBV01000076.txt"] = "Shewanella_sp._M-Br"

# 読み込んだリストのファイルを一行づづ辞書に登録
f = open(LIST)
line = f.readline()
while line:
    fname = line[:line.find("\t")]
    difinition = line[line.find("\t"):]
    difinition = difinition.lstrip("\t")
    difinition = difinition.strip("\n")
    mydict[fname] = difinition
    line = f.readline()
f.close()

#　ファイルの読み込み
TXT = open(IN, "r")
mystr = TXT.read()


for k, v in mydict.items():
    mystr = mystr.replace(k, v)

print(mystr)
