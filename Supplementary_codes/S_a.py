import pandas as pd

# 读取Excel文件，第一列作为索引（评价方法）
file_path = '2E1.xlsx'
data = pd.read_excel(file_path, index_col=0)  # 评价方法为行索引

# 计算行之间的Pearson相关系数（转置后计算列之间的相关性）
corr_matrix = data.T.corr(method='pearson')  # 关键：转置后再计算

# 输出相关系数矩阵
output_path = '2E2.xlsx'
corr_matrix.to_excel(output_path)

print("评价方法之间的Pearson相关系数矩阵已成功输出到", output_path)