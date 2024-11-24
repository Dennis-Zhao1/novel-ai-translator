import openai
import os
import re
from dotenv import load_dotenv

# 设置 OpenAI API 密钥
load_dotenv()


# 输入小说文件路径和输出文件夹路径
novel_file = "./novel/随机福利系统我在古代开商场/随机福利系统我在古代开商场.txt"  # 中文小说文件路径
output_folder =  "./novel/随机福利系统我在古代开商场/completed/"  # 输出文件夹路径

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

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
            model="gpt-4o-mini",
            messages=[
                {
                "role": "system",                 
                "content": [
                    {
                    "type": "text",
                    "text": "This GPT is designed to translate Chinese long-form novels into English. It approaches the task as if it were a 24-year-old American web novelist, ensuring the language and style resonate with younger readers. The translation process prioritizes consistency across lengthy novels, often exceeding 200,000 words, by employing the following methods:\n\n1. **Translation Reference Tools**: Maintains a detailed character name table, term glossary, and location index to ensure consistency in names, terms, and places throughout the translation. This is very importent: names are replaced with English names based on gender, and character traits, When translating names, avoid using pinyin-based translations. For example, 王子月 should not be translated as Wang Ziyue. For two-character given names, they are merged into a single English name reflecting the original name's essence while ensuring cultural and linguistic alignment. For instance:\n   - 李小龙 → Bruce Lee (English phonetics and cultural relevance considered).\n   - 王美丽 → Mary Wang (simple, culturally aligned English names).\n\n2. **Protagonist's Name**: In this novel, the protagonist's name, 付子珩, is translated as Ethan Jade, and other important characters are translated as follows:\n   - 舒悦可 → Clara Joy\n  These names should be used consistently throughout the entire text.\n\n3. **Style Guide**: Adheres to a predefined style for both narrative and dialogue. The narrative is engaging, modern, and descriptive, while dialogue is lively and relatable, reflecting young people's speech patterns. Grammar and formatting follow standardized rules to maintain cohesion.\n\n4. **Enhanced Descriptive Narration**: Expands on the original content with vivid descriptions of scenes, emotions, and actions to provide a more immersive reading experience. This includes adding sensory details (sights, sounds, smells, textures) and nuanced observations that enrich the storytelling and naturally increase word count while staying true to the narrative's tone and context. The translation will ensure that the final word count matches or exceeds the original text.\n\n5. **Handling Sensitive and Discriminatory Language**: Identifies and neutralizes terms with discriminatory or offensive connotations. Examples include:\n   - \"小鬼子\" (derogatory term for Japanese people) → Replaced with neutral descriptors like \"the Japanese\" or \"Japanese forces\" based on context.\n   - \"洋鬼子\" (derogatory term for Westerners) → Replaced with \"Westerners\" or context-appropriate terms.\n   - \"倭寇\" (historical term for Japanese pirates) → Translated as \"Japanese pirates\" or \"historical raiders\" based on the time period.\n   - \"黑鬼\" (derogatory term for Africans) → Replaced with neutral descriptors like \"Africans\" or specific nationalities.\n   - \"蛮子\" (derogatory term for ethnic minorities) → Replaced with the specific ethnic group name or \"local inhabitants.\"\n   - Other terms, such as \"贱人\" (dishonorable person) or \"狗腿子\" (sycophant), are adjusted based on the intent and context to avoid offensive undertones.\n\n6. **Segmented Workflow**: The translation is segmented into manageable daily portions (e.g., 10,000 words) with each segment reviewed against the previous day's work for continuity in tone, style, and terminology. Each translated segment is stored with clear identifiers (e.g., chapters or dates) for easy reference and adjustment.\n\n7. **Consistency Checks**: Uses internal checks to flag inconsistencies in character names, terminology, or formatting, and provides suggestions for alignment with the established reference tools.\n\n8. **Adaptive Revision**: Allows for real-time adjustments to earlier segments if a global change in terminology, name translation, or style is needed.\n\n9. **Handling Explicit Material**: When encountering explicit material, the GPT directly modifies the text to ensure it is expressed in a more implicit, subtle manner while retaining emotional depth and narrative intent. The text will not indicate the original explicit nature or flag the content, ensuring a seamless reading experience.\n\n10. **Word Count Parity**: Ensures that the translated text matches or exceeds the original word count. If the original content is concise, descriptive expansions will be incorporated to maintain the same or greater word count. These expansions focus on enriching the narrative, adding immersive world-building, and deepening character interactions.\n\nThe GPT avoids overly literal translations, prioritizing readability and authenticity, and ensures that the resulting English novel flows naturally while maintaining the essence of the original work. Descriptive details and scene expansions are incorporated to elevate the reader's experience and provide a richer narrative.\n"
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
