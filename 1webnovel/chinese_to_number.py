def cvt_num(src):
    """
    将中文数字转换为阿拉伯数字。
    """
    # 定义权重和基数的映射
    multi = {
        "亿": int(1e8),
        "万": int(1e4),
        "千": int(1e3),
        "百": int(1e2),
        "十": int(1e1)
    }

    base = {
        "零": 0,
        "一": 1,
        "二": 2,
        "三": 3,
        "四": 4,
        "五": 5,
        "六": 6,
        "七": 7,
        "八": 8,
        "九": 9
    }

    print(f"current src: {src}")

    dst = 0
    yi_dst = 0
    wan_dst = 0
    currval = 0

    for char in src:
        if char in multi:
            # 处理 "亿" 和 "万" 的特殊分区
            if char == "亿":
                yi_dst = (dst + currval) * multi[char]
                dst = 0
            elif char == "万":
                wan_dst = (dst + currval) * multi[char]
                dst = 0
            else:
                dst += currval * multi[char]
            currval = 0
        elif char in base:
            currval = base[char]

    # 累加不同部分的值
    dst += yi_dst + wan_dst + currval
    return dst

if __name__ == "__main__":
    # 示例输入
    examples = [
        "五十六万七千九百零一",
        "五千四百二十八万九千三百二十一",
        "五千四百二十八万零二十一",
        "五亿零一十万零八十",
        "九千万零一十二",
        "九千万",
        "九千零五",
        "二十万",
        "十",
        "十五",
        "一百一十",
        "一十",
        "一十五"
    ]

    for example in examples:
        result = cvt_num(example)
        print(f"{example} -> {result}")
