# alpha多様性
```
import numpy as np
import skbio
from skbio import diversity


df = pd.read_table('merged_abundance_table_species_sort 2.txt', header=0)

counts = df['PT_001'].values
counts = counts * 10000000
counts = np.array(counts, dtype='int')
skbio.diversity.alpha.shannon(counts)
```
## 全てのサンプルを一括で処理
```
import numpy as np
import skbio
from skbio import diversity


df = pd.read_table('merged_abundance_table_species_sort 2.txt', header=0, index_col=0)
l_columns = list(df.columns)

for i in l_columns:
    print(i)
    counts = df[i].values
    counts = counts * 10000000
    counts = np.array(counts, dtype='int')
    print(skbio.diversity.alpha.shannon(counts))

```
