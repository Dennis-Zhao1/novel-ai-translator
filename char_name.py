import jieba
import jieba.posseg as pseg
import pandas as pd
import os

# 读取文本文件
novel_file = "./8Radish/new/"  # 中文小说文件路径
output_folder = "./8Radish/new/name_table/"  # 输出文件夹路径
os.makedirs(output_folder)
for filename in os.listdir(novel_file):
    if filename.endswith(".txt"):  # 检查是否是 txt 文件
        file_path = os.path.join(novel_file, filename)  # 构建完整路径        
        print(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # 使用 jieba 分词并提取人名
        words = jieba.lcut(text)
        names = []
        for w, pos in pseg.cut(text):
            if pos == 'nr':
                names.append(w)

        # 转换为 DataFrame
        name_df = pd.DataFrame({'name': names})

        # 统计名字的频率
        name_count = name_df['name'].value_counts()

        # 将统计结果转换为 DataFrame 并过滤掉 count <= 2 的名字
        name_count = name_count[name_count > 2]

        # 保存到 CSV 文件
        output_path = os.path.join(output_folder,filename.replace('txt','csv'))
        name_count.to_csv(output_path, encoding='utf-8', header=['count'])

