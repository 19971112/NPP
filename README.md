# NPP

## 環境構築
```
# brew 
# https://qiita.com/thermes/items/926b478ff6e3758ecfea
sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"

```

### install QIIME2
```
wget https://data.qiime2.org/distro/core/qiime2-2019.10-py36-linux-conda.yml
conda env create -n qiime2-2019.10 --file qiime2-2019.10-py36-linux-conda.yml
wget ftp://greengenes.microbio.me/greengenes_release/gg_13_5/gg_13_8_otus.tar.gz
```
### test data
```
# https://docs.qiime2.org/2019.10/data-resources/
wget ftp://greengenes.microbio.me/greengenes_release/gg_13_5/gg_13_8_otus.tar.gz
```
