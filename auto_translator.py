import openai
import os
import re
from dotenv import load_dotenv

# 设置 OpenAI API 密钥
load_dotenv()


# 输入小说文件路径和输出文件夹路径
novel_file = "./8Radish/new/腹黑总裁狂宠合约小娇妻name changed.txt"  # 中文小说文件路径
output_folder = "./8Radish/new/腹黑总裁狂宠合约小娇妻/completed"   # 输出文件夹路径

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)


prompt = (
    "This GPT is designed to role-play as a young American college graduate who has read many Chinese novels and rewrites them in English, adhering to American writing conventions and style. The GPT reimagines these stories with a casual, engaging, and sometimes humorous tone, crafting narratives that reflect the essence of the original works while making them relatable to Western readers. Key themes, characters, and plotlines are vividly described, with cultural nuances adapted or contextualized. Any mention of Chinese currency like '元 (yuan),' '角 (jiao),' or '分 (fen)' is converted into approximate equivalents in the U.S. dollar system. Chinese festivals mentioned in the stories, such as '春节 (Spring Festival)' or '中秋节 (Mid-Autumn Festival),' are replaced with comparable Western holidays like Christmas or Thanksgiving, based on the cultural and thematic context. References to family members such as '叔叔 (uncle)' or '舅妈 (aunt)' or '陈公子' or '王小姐' are replaced with the specific character names, making the narrative more personalized and immersive. Chinese slang, idioms, or internet buzzwords that might confuse readers or disrupt understanding are omitted unless essential to the plot and explained. Descriptions of character violence or violent actions are modified or omitted as appropriate to maintain a tone that is engaging without unnecessary explicit content. Real-world countries, cities, or place names are replaced with fictional names to create a universal and imaginative setting. Traditional Chinese foods such as '饺子 (dumplings),' '包子 (steamed buns),' or '粥 (porridge)' are replaced with familiar Western foods like sandwiches, burgers, or pizza for relatability. Mentions of Chinese social media platforms like '微信 (WeChat),' 'QQ,' '抖音 (Douyin),' '快手 (Kuaishou),' 'B站 (Bilibili),' '小红书 (Xiaohongshu),' '微博 (Weibo),' '知乎 (Zhihu),' and '朋友圈 (WeChat Moments)' are replaced with commonly used American platforms such as TikTok, WhatsApp, Facebook, Instagram, or Reddit, aligning the storytelling with Western norms and preferences."
)



# 分割章节的正则表达式（匹配“第X章”形式的标题）
chapter_pattern = r"(\d+章.*?)"

def split_into_chapters(content):
    """
    根据章节分隔符拆分文本。
    """
    # print(f"File content with escape characters:\n{repr(content[:500])}")
    
    chapters = re.split(chapter_pattern, content)
    
    matches = re.findall(chapter_pattern, content)
    print(f"Matched chapters: {matches}")
    
    
    result = []
    for i in range(1, len(chapters), 2):  # 章节标题和内容交替
        title = chapters[i].strip()
        text = chapters[i + 1].strip()
        result.append((title, text))
    return result

def translate_text(text):
    """
    调用 OpenAI API 翻译文本。
    """
    
    # from openai import OpenAI
    # client = OpenAI()
    from openai import OpenAI
    client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)
    # print(os.environ.get("OPENAI_API_KEY"))
    
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                "role": "system",                 
                "content": [
                    {
                    "type": "text",
                    "text":prompt
                    }
                ]
                },             
                {
                "role": "user", 
                "content":[
                    {
                        "type": "text",
                        "text":text                        
                    }                    
                ]                    
                }
            ],
            temperature=0.7
        )
        # print(chat_completion.choices[0].message.content)
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error during translation: {e}")
        return None

def save_chapter(title, content, folder):
    """
    将翻译的章节内容保存为单独的文件。
    """
    filename = f"{title}.txt"
    # 去除文件名中的非法字符
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filepath = os.path.join(folder, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    # 读取小说内容
    with open(novel_file, "r", encoding="utf-8") as file:
        content = file.read()

    # 分割小说成章节
    # print("changdu:" ,len(content))
    chapters = split_into_chapters(content)
    print(f"Detected {len(chapters)} chapters.")

    # 翻译并保存每个章节
    for i, (title, text) in enumerate(chapters, 1):
        print(f"Translating chapter {i}: {title}")
        translated_text = translate_text(text)
        if translated_text:
            save_chapter(title, translated_text, output_folder)
            print(f"Chapter {i} saved successfully.")
        else:
            print(f"Failed to translate chapter {i}. Skipping.")

if __name__ == "__main__":
    main()
