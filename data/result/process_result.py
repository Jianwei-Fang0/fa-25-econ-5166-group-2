import pandas as pd

df_result = pd.read_csv("data\\result\\df_result.csv")

df_obvious = df_result[(df_result['total']-abs(df_result['net_borrow_pred'] ) <= 10)]
df_obvious['difference_in_restock'] = df_obvious['total'] - abs(df_obvious['net_borrow_pred'])
df_obvious_sorted = df_obvious.sort_values(by='difference_in_restock', ascending=True)
print(df_obvious_sorted)