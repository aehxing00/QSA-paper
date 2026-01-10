import pandas as pd
import numpy as np
import re

# 读取Excel文件
df = pd.read_excel('a1.xlsx')

# 获取第一列列名
first_col_name = df.columns[0]

# 提取小类别
def extract_category(question_id):
    if isinstance(question_id, str):
        match = re.match(r'(\d+[A-Za-z])', question_id)
        if match:
            return match.group(1)
    return str(question_id)

# 添加小类别列
df['Category'] = df[first_col_name].apply(extract_category)

# 获取模型名称（排除第一列和Category列）
model_names = [col for col in df.columns if col not in [first_col_name, 'Category']]

print("原始数据统计信息:")
print("=" * 50)
for model in model_names:
    print(f"\n模型 {model}:")
    print(f"  数据类型: {df[model].dtype}")
    print(f"  非空值数量: {df[model].count()}")
    print(f"  数值范围: {df[model].min()} ~ {df[model].max()}")
    print(f"  平均值: {df[model].mean():.4f}")
    print(f"  前5个值: {df[model].head().tolist()}")

# 检查每个小类别的数据
print("\n\n小类别详细分析:")
print("=" * 50)
categories = sorted(df['Category'].unique())

for category in categories:
    category_data = df[df['Category'] == category]
    print(f"\n小类别 {category} (共{len(category_data)}条数据):")
    
    for model in model_names:
        values = category_data[model]
        print(f"  {model}: {len(values)}个值, 范围: {values.min():.4f}~{values.max():.4f}, 平均值: {values.mean():.4f}")

# 重新计算平均值（确保方法正确）
print("\n\n重新计算分组平均值:")
print("=" * 50)

# 方法1：使用groupby
result_groupby = df.groupby('Category')[model_names].mean().reset_index()
print("Groupby方法结果:")
print(result_groupby)

# 方法2：手动计算验证
result_manual = []
for category in categories:
    category_data = df[df['Category'] == category]
    row_data = {'Category': category}
    
    for model in model_names:
        values = category_data[model]
        mean_value = values.mean()
        row_data[model] = mean_value
        print(f"  {category}-{model}: {len(values)}个值的平均值 = {mean_value:.4f}")
    
    result_manual.append(row_data)

result_manual_df = pd.DataFrame(result_manual)

print("\n手动计算方法结果:")
print(result_manual_df)

# 检查两种方法结果是否一致
print("\n两种方法结果比较:")
print("差异:", (result_groupby[model_names] - result_manual_df[model_names]).abs().sum().sum())

# 保存结果
result_groupby.to_excel('a2.xlsx', index=False)
print(f"\n结果已保存到 a2.xlsx")

# 额外检查：是否有异常值或数据重复
print("\n数据质量检查:")
print("=" * 50)
print(f"总行数: {len(df)}")
print(f"唯一Question_ID数量: {df[first_col_name].nunique()}")
print(f"重复的Question_ID: {df[df.duplicated(subset=[first_col_name])][first_col_name].tolist()}")

# 检查每个小类别的样本数量
category_counts = df['Category'].value_counts()
print(f"\n各小类别样本数量:")
for category, count in category_counts.items():
    print(f"  {category}: {count}个样本")