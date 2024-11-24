import re

def load_name_mapping(file_path):
    
    name_mapping = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        print("open name_mapping file")
        for line in f:
            print("start for")
            # 假设文件格式是: 中文名,英文名
            print('line:',line)
            parts = line.strip().split(',')
            print('parts: ',parts)
            if len(parts) == 2:  # 确保每行都有中英文对
                chinese_name, english_name = parts
                name_mapping[chinese_name.strip()] = english_name.strip()
    print(name_mapping)
    return name_mapping

def replace_names_in_text(input_text, name_mapping):
    """
    替换文本中的中文名字为英文名字
    :param input_text: 原始文本
    :param name_mapping: {中文名: 英文名} 的字典
    :return: 替换后的文本
    """
    # 构建正则表达式模式，匹配所有名字
    name_pattern = re.compile('|'.join(re.escape(name) for name in name_mapping.keys()))
    print(f"正则表达式模式: {name_pattern.pattern}")  # 打印调试用的正则表达式

    # 替换名字
    def replace_name(match):
        chinese_name = match.group(0)
        return name_mapping.get(chinese_name, chinese_name)

    replaced_text = name_pattern.sub(replace_name, input_text)
    return replaced_text

def process_file(input_file, output_file, name_mapping):
    """
    处理输入文件，生成替换后的文件
    :param input_file: 输入的 TXT 文件路径
    :param output_file: 输出的 TXT 文件路径
    :param name_mapping: {中文名: 英文名} 的字典
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        input_text = f.read()

    # 打印原始内容的前100字符用于调试
    print("原始内容预览:", input_text[:100])

    # 替换文本中的名字
    replaced_text = replace_names_in_text(input_text, name_mapping)

    # 打印替换后的内容前100字符
    print("替换后的内容预览:", replaced_text[:100])

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(replaced_text)

    print(f"文件处理完成，结果已保存到 {output_file}")

# 示例运行
if __name__ == "__main__":
    # 中英文对应表文件路径
    name_mapping_file = "./name_mapping.txt"  # 假设文件格式是中文,英文
    # 输入和输出的文本文件
    input_txt_file = "./小说初步选取/test/test.txt"
    output_txt_file = "./小说初步选取/test/test_namechanged.txt"

    # 加载名字映射表
    name_mapping = load_name_mapping(name_mapping_file)
    print("名字映射表:", name_mapping)  # 打印名字映射表调试

    # 处理文件
    process_file(input_txt_file, output_txt_file, name_mapping)
