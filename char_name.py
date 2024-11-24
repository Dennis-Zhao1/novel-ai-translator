import jieba
import jieba.posseg as pseg
import pandas as pd

# 读取文本文件
with open('./小说初步选取/test/相亲意外嫁给豪门霸总.txt', 'r', encoding='utf-8') as f:
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
name_count.to_csv('name_count.csv', encoding='utf-8', header=['count'])
