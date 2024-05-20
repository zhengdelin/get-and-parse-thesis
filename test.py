import pandas as pd

df = pd.DataFrame({}, columns=['year', 'title', 'content'])
df.loc[0] = [2022, 'title', 'content']

s = pd.Series([1, 2])

a = []
print(not a)
