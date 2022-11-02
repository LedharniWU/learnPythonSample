from tkinter.tix import COLUMN
import pandas as pd

df = pd.read_excel('data.xlsx')

# print(df['日付'])

print(df.query('日付 == "2020-04-01"'))
# columns = list(df.columns)

# for i in list(df.columns):
#     print(i)



# print(list(df.columns))