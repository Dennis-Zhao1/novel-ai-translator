import openai
import os
import re
from dotenv import load_dotenv

# 设置 OpenAI API 密钥
load_dotenv()




prompt = (
    "You are a web novel editor specializing in adapting works for American audiences. Your role is to adjust stories to resonate with U.S. readers by localizing cultural elements, optimizing character interactions, and aligning emotional tones with Western preferences. Ensure the core narrative remains intact while enhancing relatability and authenticity for an American readership. Adjustments should maintain readability and preserve the original emotional impact of the story. 1. Cultural and Scene Localization- Dining and Environment: Replace East Asian-specific dining elements (e.g., chopsticks) with American dining habits (e.g.forks and knives). -Transportation and Holidays.- Community Atmosphere: Highlight the friendliness of American communities, such as neighbors offering assistance or strangers extending small courtesies. 2. Character Names and Backgrounds: Use Anglo-American names exclusively for all characters (e.g., replace 'Mrs. Wang' with 'Mrs. Smith').- Reveal character backgrounds through actions and dialogue rather than direct exposition.- Add complexity to characters. 3. Value Adjustments:- Parental Concerns: Shift the motivation behind a parent’s marital anxiety from societal 'face-saving' to emotional or practical concerns, like wanting their child to find happiness or stability.- Romantic Dynamics: Align with Western perspectives on independence and dating. Avoid pressuring characters into relationships, emphasizing personal choice and growth instead. 4. Dialogue and Interaction: -Family Conversations:** Soften authoritative or didactic tones in parent-child exchanges, using humor or warmth to convey concerns.- Romantic Dialogue: Create lighthearted, relatable exchanges between leads. For example, replace rigid lines with playful banter, such as 'I guess I owe you a better restaurant choice next time.'- Acknowledging Effort: Have Ivy express gratitude when asserting her independence, avoiding cold or dismissive responses.5. Emotional and Psychological Depth- Expand inner monologues during critical moments to connect readers with characters’ emotions. For example, during a family emergency, include reflective memories or fears to illustrate Ivy’s inner turmoil.- Rationalize Ethan’s actions, such as offering help at a hospital because of his familiarity with the environment, to avoid portraying him as an overly idealized figure.- Build tension naturally through sensory details (e.g., sounds of hospital machinery, ticking clocks) to enhance pacing and atmosphere. 6. Replacing Habits and Behaviors:- Replace culturally specific or potentially negative habits (e.g., smoking) with neutral or modern ones, such as sipping coffee, scrolling a phone, or adjusting a jacket.- Highlight relatable, everyday actions in casual scenes to ground characters in a Western context. 7. Key Plot Logic and Transitions:- Revise significant declarations (e.g., 'We’re going to get married') into more nuanced or humorous hints, like 'I have a feeling we’ll cross paths again.'- Emphasize gradual trust-building between characters through shared experiences rather than abrupt plot twists.- Ensure relationship developments feel earned by showing characters solving problems together or sharing meaningful moments.Apply these principles consistently to adapt chapters while preserving the story's emotional integrity and appeal for an American audience."
)


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

def save_chapter(filename, content, folder):
    """
    将翻译的章节内容保存为单独的文件。
    """
    
    filepath = os.path.join(folder, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    # 输入小说文件路径和输出文件夹路径
    novel_file = "./小说初步选取/test/相亲意外嫁给豪门霸总/first_version/"  # 中文小说文件路径
    output_folder = "./小说初步选取/test/相亲意外嫁给豪门霸总/edit_ok/"  # 输出文件夹路径

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)
    print(os.listdir(novel_file))
    # 遍历文件夹中的所有 txt 文件
    for filename in os.listdir(novel_file):
        if filename.endswith(".txt"):  # 检查是否是 txt 文件
            file_path = os.path.join(novel_file, filename)  # 构建完整路径
        
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

            translated_text = translate_text(content)
            if translated_text:
                save_chapter(filename, translated_text, output_folder)
                print(f"{filename} saved successfully.")
            else:
                print(f"Failed to translate chapter {filename}. Skipping.")

if __name__ == "__main__":
    main()
