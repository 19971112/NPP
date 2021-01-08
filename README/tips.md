# 便利なコマンド一覧


## shell系

### ターミナル の出力結果を一行づつ処理

例えば、特定の条件でひっかけたidを処理するとか  

```
#　（例）リストに記載されているidのファイルを移動させる
cat SraRunTable.txt | grep "Fukushima" | cut -d "," -f 1 | sed -e 's/"\'\n'//g' | while read line; do cp $line* dataset; done
```
