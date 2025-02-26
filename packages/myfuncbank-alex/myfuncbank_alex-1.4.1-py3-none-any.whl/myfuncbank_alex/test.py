import pandas as pd

# 创建一个简单的 DataFrame
data = {
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9],
    'D': [10, 11, 12]
}

df = pd.DataFrame(data)

# 指定目标列名
target_column = 'A'

# 获取目标列的索引位置
col_index = df.columns.get_loc(target_column)

# 获取该列前面的所有列名
columns_before_target = df.columns[:col_index]

# 对指定列进行求和
sum_result = df[columns_before_target].sum(axis=1)  # axis=1 表示按行求和

# 将结果存储到新的 DataFrame 中
new_df = pd.DataFrame(sum_result, columns=['Sum'])

# 打印新的 DataFrame
print(new_df)
