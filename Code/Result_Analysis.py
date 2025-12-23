
import pandas as pd
import matplotlib.pyplot as plt
import os

import matplotlib.pyplot as plt

# 设置中文字体（Windows 优先用 SimHei）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取Excel文件
file_path = 'CrimeTrace-500-Result.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

# 确保当前路径下存在 Chart 文件夹，用于保存图像
chart_dir = os.path.join(os.path.dirname(os.path.abspath(file_path)) or os.getcwd(), 'Chart')
os.makedirs(chart_dir, exist_ok=True)

# 查看数据的基本信息
print("数据形状:", df.shape)
print("\n前5行数据:")
print(df.head())
print("\n列名:")
print(df.columns.tolist())
print("\n数据类型:")
print(df.dtypes)

# 图表1：不同风险等级的案件数量分布（条形图）
risk_level_counts = df['Risk_Level'].value_counts()
plt.figure(figsize=(10, 6))
risk_level_counts.plot(kind='barh', color=['#ff6b6b', '#ffa726', '#66bb6a', '#42a5f5'])
plt.title('不同风险等级的案件数量分布')
plt.xlabel('案件数量')
plt.ylabel('风险等级')
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
# 保存图像到 Chart 文件夹
out_path = os.path.join(chart_dir, 'chart1.png')
plt.savefig(out_path, dpi=300)
plt.show()



# 图表2：三个评分维度的平均分对比（簇状柱形图）
score_columns = ['Score_Instruction', 'Score_Entity', 'Score_AntiForensics']
average_scores = df[score_columns].mean()

plt.figure(figsize=(10, 6))
bars = plt.bar(score_columns, average_scores.values, color=['#ff6b6b', '#ffa726', '#42a5f5'])
plt.title('各评分维度的平均分对比')
plt.ylabel('平均分')
plt.xlabel('评分维度')
plt.ylim(0, 10)

# 在柱子上添加数值标签
for bar, score in zip(bars, average_scores.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
             f'{score:.2f}', ha='center', va='bottom')

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
# 保存图像到 Chart 文件夹
out_path = os.path.join(chart_dir, 'chart2.png')
plt.savefig(out_path, dpi=300)
plt.show()


# 图表3 & 4：不同案件类型的平均总分对比（条形图）
# 计算每个案件类型的平均总分（三个评分的平均值）
df['Average_Score'] = df[['Score_Instruction', 'Score_Entity', 'Score_AntiForensics']].mean(axis=1)

# 按案件类型分组，计算平均总分
type_avg_scores = df.groupby('案件类型')['Average_Score'].mean().sort_values(ascending=False)

# 由于案件类型较多（50种），选择平均分最高和最低的各10个类型进行对比
top_10 = type_avg_scores.head(10)
bottom_10 = type_avg_scores.tail(10)

# 绘制对比条形图
plt.figure(figsize=(14, 10))

# 平均分最高的10个类型
plt.subplot(2, 1, 1)
bars1 = plt.barh(top_10.index, top_10.values, color='#66bb6a')
plt.title('平均分最高的10个案件类型')
plt.xlabel('平均分')
plt.xlim(0, 10)
plt.gca().invert_yaxis()  # 让最高分在顶部
for bar, score in zip(bars1, top_10.values):
    plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, f'{score:.2f}', ha='left', va='center')

# 平均分最低的10个类型
plt.subplot(2, 1, 2)
bars2 = plt.barh(bottom_10.index, bottom_10.values, color='#ff6b6b')
plt.title('平均分最低的10个案件类型')
plt.xlabel('平均分')
plt.xlim(0, 10)
plt.gca().invert_yaxis()  # 让最低分在底部
for bar, score in zip(bars2, bottom_10.values):
    plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, f'{score:.2f}', ha='left', va='center')

plt.tight_layout()
# 保存图像到 Chart 文件夹
out_path = os.path.join(chart_dir, 'chart3_4.png')
plt.savefig(out_path, dpi=300)
plt.show()

# 输出一些统计信息
print(f"所有案件类型的平均总分范围: {type_avg_scores.min():.2f} - {type_avg_scores.max():.2f}")
print(f"平均总分最高的案件类型: {top_10.index[0]} ({top_10.values[0]:.2f})")
print(f"平均总分最低的案件类型: {bottom_10.index[-1]} ({bottom_10.values[-1]:.2f})")



# 图表5：不同案件类型在三个评分维度上的差异（分组条形图）
# 计算每个案件类型在三个评分上的平均分
type_scores = df.groupby('案件类型')[['Score_Instruction', 'Score_Entity', 'Score_AntiForensics']].mean()

# 计算每个案件类型的平均总分，用于排序
type_scores['Average_Score'] = type_scores.mean(axis=1)
type_scores_sorted = type_scores.sort_values('Average_Score', ascending=False)

# 选择平均总分最高和最低的各5个案件类型
top_5_types = type_scores_sorted.head(5).index
bottom_5_types = type_scores_sorted.tail(5).index

# 提取这10个类型的三项评分数据
selected_types = list(top_5_types) + list(bottom_5_types)
selected_scores = type_scores.loc[selected_types]

# 绘制分组条形图
plt.figure(figsize=(14, 8))
x = range(len(selected_types))
width = 0.25

# 绘制每个评分维度的条形
plt.bar([i - width for i in x], selected_scores['Score_Instruction'], width, label='指导性评分', color='#ff6b6b')
plt.bar(x, selected_scores['Score_Entity'], width, label='实体评分', color='#ffa726')
plt.bar([i + width for i in x], selected_scores['Score_AntiForensics'], width, label='反取证评分', color='#42a5f5')

plt.xlabel('案件类型')
plt.ylabel('平均分')
plt.title('不同案件类型的评分差异（最高和最低各5个类型）')
plt.xticks(x, selected_types, rotation=45, ha='right')
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
# 保存图像到 Chart 文件夹
out_path = os.path.join(chart_dir, 'chart5.png')
plt.savefig(out_path, dpi=300)
plt.show()

# 输出最高和最低类型的详细评分
print("平均总分最高的5个案件类型评分：")
print(selected_scores.head(5))
print("\n平均总分最低的5个案件类型评分：")
print(selected_scores.tail(5))


# 图表6：技术犯罪类型的评分维度相关性分析（热力图）
# 定义技术犯罪类型列表（基于常见技术犯罪类型）
tech_crime_types = [
    '制造恶意软件与病毒', 
    '黑客攻击', 
    '网络诈骗', 
    '数据窃取', 
    'DDoS攻击', 
    '钓鱼攻击', 
    '勒索软件', 
    '加密货币盗窃', 
    '身份盗窃', 
    '网络入侵'
]
 
# 筛选技术犯罪数据
tech_crime_df = df[df['案件类型'].isin(tech_crime_types)]
 
# 检查筛选后的数据
print(f"技术犯罪记录数量: {len(tech_crime_df)}")
print(f"技术犯罪类型分布:\n{tech_crime_df['案件类型'].value_counts()}")
 
# 计算三个评分维度的相关性矩阵
correlation_matrix = tech_crime_df[['Score_Instruction', 'Score_Entity', 'Score_AntiForensics']].corr()
 
print("\n技术犯罪评分维度相关性矩阵:")
print(correlation_matrix)
 
# 可视化相关性热力图
import seaborn as sns
 
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, square=True)
plt.title('技术犯罪评分维度相关性热力图')
plt.tight_layout()
# 保存图像到 Chart 文件夹
out_path = os.path.join(chart_dir, 'chart6.png')
plt.savefig(out_path, dpi=300)
plt.show()



# 图表7：高风险案件的评分维度分析（直方图 & 箱线图 & 相关性矩阵）
# 筛选高风险案件
high_risk_df = df[df['Risk_Level'] == 'High_Critical']

# 计算高风险案件在三个评分维度上的描述性统计
high_risk_scores = high_risk_df[['Score_Instruction', 'Score_Entity', 'Score_AntiForensics']]
stats = high_risk_scores.describe()

print("高风险案件评分维度描述性统计:")
print(stats)

# 绘制高风险案件评分分布直方图
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.hist(high_risk_scores['Score_Instruction'], bins=10, color='#ff6b6b', edgecolor='black')
plt.title('指导性评分分布')
plt.xlabel('评分')
plt.ylabel('频数')

plt.subplot(1, 3, 2)
plt.hist(high_risk_scores['Score_Entity'], bins=10, color='#ffa726', edgecolor='black')
plt.title('实体评分分布')
plt.xlabel('评分')
plt.ylabel('频数')

plt.subplot(1, 3, 3)
plt.hist(high_risk_scores['Score_AntiForensics'], bins=10, color='#42a5f5', edgecolor='black')
plt.title('反取证评分分布')
plt.xlabel('评分')
plt.ylabel('频数')

plt.tight_layout()
# 保存图像到 Chart 文件夹
out_path = os.path.join(chart_dir, 'chart7_histogram.png')
plt.savefig(out_path, dpi=300)
plt.show()

# 绘制箱线图对比三个评分维度
plt.figure(figsize=(10, 6))
high_risk_scores.boxplot()
plt.title('高风险案件评分维度箱线图')
plt.ylabel('评分')

plt.xticks(rotation=45, ha='right')
plt.subplots_adjust(bottom=0.25)
plt.savefig(out_path, dpi=300, bbox_inches='tight')

plt.grid(axis='y', alpha=0.3)
# 保存图像到 Chart 文件夹
out_path = os.path.join(chart_dir, 'chart7_boxplot.png')
plt.show()

# 计算三个评分维度的相关性矩阵
correlation_matrix = high_risk_scores.corr()
print("\n高风险案件评分维度相关性矩阵:")
print(correlation_matrix)

