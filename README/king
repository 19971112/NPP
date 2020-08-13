### king
$ `ssh king`
~ 16:46$ `qsub -I[ｱｲ] -l[ｴﾙ] nodes=1:ppn=32`

- kingに入った後に
    - `qsub -I -l nodes=1:ppn=32 -q all.q` ってやればノードにログインできる
- kings使用方法リンク
    - [冨田研 king使用法ページ](https://rg.bioinfo.ttck.keio.ac.jp/pukiwiki.php?King)
- キュー設定は以下の二つ
    1. all.q: プライオリティ：20　最大実行時間：24h　ユーザあたりの最大同時実行数：無制限
    2. low.q: プライオリティ：10　最大実行時間：336h　ユーザあたりの最大同時実行数：1

$ `qsub -S usr/bin/bash [シェルスクリプト名]` (デフォルトは/bin/csh
もしくはスクリプト先頭に #$ -S /usr/bin/bash

- オプション
-o [パスA] -e [パスB] 標準出力と標準エラー出力
-N [グループ名] (グループ単位指定)
-cwd

> $ qsub -N job1 [スクリプト名]
$ qsub -N job2 -hold_jid job1 [スクリプト名]
$ qsub -N job3 -hold_jid job1,job2 [スクリプト名]
<br>
$ qstat
$ qstat -f (詳細)
$ qstat -n (実行しているノードが分かる)
$ qstar -f -u ‘*’ (ジョブの実行優先順位) 
$ qdel [ジョブID] or [グループ名]
`/home/yuki.yoshida/scripts/king_status.sh`

`pbsnodes | grep -e "^k" -e "jobs" | grep -v "status" | less`
