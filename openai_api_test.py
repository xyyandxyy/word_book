import openai
from openai import OpenAI
client = OpenAI(api_key='sk-3Cesgcjbtyjdr5IX4e9f49B596A1428383Af4f42A85fD978', base_url="https://www.gptapi.us/v1/")

def generate_sentence(word, meaning):
    # 调用API生成文本
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"给你一个英文单词(同时包含对应的中文意思, 请避免因为一词多义造成误解), 请你生成一句包含这个单词的简单英文句子(注意其他涉及的单词能让词汇量不超过500的孩子看懂), 同时在这句话之后输出对应中文翻译. 例如输入 employ(),你输出(注意不要换行): They employ force to enter the building. 他们不得不强行进入大楼. 现在我给你的单词是{word}\({meaning}\)"}
    ]
    )

    # 打印生成的文本
    return(response.choices[0].message.content.strip())

print(generate_sentence('born', 'v. 出世（bear的过去分词）'))