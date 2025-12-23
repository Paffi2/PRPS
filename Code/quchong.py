import pandas as pd
import os

# 1. 定义文件路径
# 使用 r"" (raw string) 来避免 Windows 路径中的反斜杠转义问题
input_file_path = r"C:\Users\华硕\Desktop\新建文件夹\safebench_processed.csv"
output_file_path = r"C:\Users\华硕\Desktop\新建文件夹\safebench_processed_unique.csv"

def remove_duplicates_from_csv(input_path, output_path):
    # 检查文件是否存在
    if not os.path.exists(input_path):
        print(f"错误：找不到文件 - {input_path}")
        return

    try:
        # 2. 读取 CSV 文件
        # encoding='utf-8-sig' 可以防止中文出现乱码
        df = pd.read_csv(input_path, encoding='utf-8-sig')
        
        # 记录原始行数
        original_count = len(df)
        print(f"原始数据行数: {original_count}")

        # 3. 执行去重操作
        # drop_duplicates() 默认会保留第一条出现的数据，删除后续完全重复的行
        df_deduplicated = df.drop_duplicates()
        
        # 记录去重后行数
        new_count = len(df_deduplicated)
        print(f"去重后数据行数: {new_count}")
        print(f"共删除了 {original_count - new_count} 行重复数据")

        # 4. 保存结果
        df_deduplicated.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"成功！去重后的文件已保存至: {output_path}")

    except Exception as e:
        print(f"处理过程中发生错误: {e}")

# 运行函数
if __name__ == "__main__":
    remove_duplicates_from_csv(input_file_path, output_file_path)
