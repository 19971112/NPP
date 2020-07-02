# alpha多様性
```
import numpy as np
from skbio import
skbio.diversity.alpha.shannon(counts, base=2)
df = pd.read_table('merged_abundance_table_species_sort 2.txt', header=0)
counts = df['PT_001'].values
skbio.diversity.alpha.shannon(counts, base=2)
```
