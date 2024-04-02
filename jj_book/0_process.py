import openai
from openai import OpenAI
from pathlib import Path
# client = OpenAI(api_key='sk-3Cesgcjbtyjdr5IX4e9f49B596A1428383Af4f42A85fD978', base_url="https://www.gptapi.us/v1/")
client = OpenAI(api_key='sk-B2worTGwvGi3Te0e39A596Fe7747430e9451Cf343b3fD29d', base_url="https://burn.hair/v1/")


def refine_sentence(input):
    # 调用API生成文本
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"给你一些OCR识别的文本, 请你对输入进行修复(删除多的空格, 修复有语病的话, 换行应保留), 要求修改尽量少的内容, 最后只要返回修复好的内容即可. 例如给你: 这个只需要-点 钱. 你只需要返回: 这个只需要一点钱, 现在我给你需要修复的句子是: {input}"}
    ]
    )

    # 打印生成的文本
    return(response.choices[0].message.content.strip())


error_words = ["修改", "修复"]

collected_text = ""  # 用于收集文本的变量

boundary_line = "■ 第20页 \n"   # 用于保存包含■的行
print(f"注意设置第一个文件的名称, 目前是{boundary_line}")

if __name__ == "__main__":
    with open('/remote-home/xujunhao/en_ai_learn/jj_book/book.txt', 'r') as file:
        for idx, line in enumerate(file):
            # if idx <= 271:
            #     continue
            if "■" in line:
                page_num = line[3:-2]
                formatted_number = f"{int(page_num):04}"
                if Path(f'/remote-home/xujunhao/en_ai_learn/jj_book/patch/第{formatted_number}页.txt').exists():
                    boundary_line = line
                    continue
                attempt = 0
                if collected_text == "":
                    print(f"在第{idx}行, collected_text 是空的, 跳")
                    continue
                result = collected_text
                output_ok = False
                while attempt < 3:
                    try:
                        result = refine_sentence(collected_text)
                        if not any(error_word in result for error_word in error_words):
                            output_ok = True
                            break  # 成功处理文本，跳出循环
                    except Exception as e:
                        print(f"在处理位于第{idx}行的文本块时第{attempt + 1}次尝试中出错")
                        print(e)
                    
                    attempt += 1
                    print("尝试了一次")
                    if attempt >= 3:
                        print(f"在处理位于第{idx}行的文本块时尝试了三次但失败了")
                        result = collected_text  # 如果处理失败，使用原始文本

                if output_ok:
                    with open(f'/remote-home/xujunhao/en_ai_learn/jj_book/patch/第{formatted_number}页.txt', 'w') as new_file:
                        new_file.write(boundary_line + "\n"+result + "\n")  # 保存边界行和处理过的文本

                collected_text = ""  # 重置文本收集器
                boundary_line = line  # 重置边界行
            else:
                collected_text += (line+"\n")  # 继续收集文本

            print(f"完成第 {idx} 行")

print("好了")