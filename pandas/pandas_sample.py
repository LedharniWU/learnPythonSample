#pandasを読み込む
import pandas as pd
#input file name
input_file_name = '20221019_monthly.xlsx'
#xls book Open (xls, xlsxのどちらでも可能)
input_book = pd.ExcelFile(input_file_name)
#sheet_namesメソッドでExcelブック内の各シートの名前をリストで取得できる
input_sheet_name = input_book.sheet_names
#lenでシートの総数を確認
num_sheet = len(input_sheet_name)
#シートの数とシートの名前のリストの表示
# print ("Sheet の数:", num_sheet)
# print (input_sheet_name)

input_sheet_df = input_book.parse(input_sheet_name[1],
skiprows = 3,
skipfooter = 2,
parse_cols = "A:B,D,F,H,J,L,N,P,R,T,V,X")

input_sheet_df = input_sheet_df.head(10)

print(input_sheet_df)