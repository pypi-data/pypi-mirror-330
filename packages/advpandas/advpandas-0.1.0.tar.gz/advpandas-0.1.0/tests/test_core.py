import pandas as pd
from advpandas import advanced_head

df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
advanced_head(df, n=2)