import re
from chinese_to_number import cvt_num

def normalize_chapters(file_path):
    """
    读取txt文件,统一章节名字格式为“第1章”。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 正则表达式匹配各种章节格式
    patterns = [
        r'第\s*(\d+)\s*章',      # 匹配“第1章”或“第 1章”等
        r'\b(\d+)\s*章',         # 匹配“1章”
        r'第\s*([一二三四五六七八九十百千万零]+)\s*章',  # 匹配“第一章”等中文数字        
        r'\b([一二三四五六七八九十百千万零]+)\s*章'     # 匹配“二章”等中文数字
    ]

    def chinese_to_arabic(chinese):
        print("find ",chinese)
        
        result = cvt_num(chinese)
        print(result)
        return result

    def replace_match(match):
        """
        将匹配的章节名转换为“第X章”格式。
        """
        group = match.group()
        # 提取章节数字
        if re.match(r'第\s*([一二三四五六七八九十百千万零]+)\s*章', group):
            number = chinese_to_arabic(group.replace('第', '').replace('章', '').strip())
        elif re.match(r'\b([一二三四五六七八九十百千万零]+)\s*章', group):
            number = chinese_to_arabic(group.replace('章', '').strip())
        elif re.match(r'第\s*(\d+)\s*章', group):
            number = int(re.search(r'\d+', group).group())
        else:
            number = int(re.search(r'\d+', group).group())
        return f"第{number}章"

    # 按顺序依次应用每个正则表达式进行替换
    for pattern in patterns:
        # 检查是否有匹配
        if re.search(pattern, content):  # 如果找到匹配项
            content = re.sub(pattern, replace_match, content)
            # break  # 退出循环


    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

    print("章节名字已统一！")

# 使用示例
file_name = "./webnovel/修真聊天群/修真聊天群.txt"
normalize_chapters(file_name)

#十五不行，要写成一十五