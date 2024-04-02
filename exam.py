import pandas as pd
import random

def sample_verb_book(start_idx, end_idx, num):
    # 替换这里的'your_file.csv'为你的CSV文件路径
    csv_file = '/remote-home/xujunhao/en_ai_learn/words/verb_book_v0.csv'
    # 替换这里的a为你给定的数字
    a = end_idx

    # 读取CSV文件
    df = pd.read_csv(csv_file)

    # 检查a是否足够大
    if a < 1:
        print("给定的数字太小，无法从中抽取20行。")
        return None
    else:
        # 确保索引不会超出范围
        a = min(a, len(df))

        # 从第0行到第a行抽取数据
        subset = df.iloc[start_idx:a]

        # 从这些行中随机选择20行
        selected_rows = subset.sample(n=num, random_state=1)

        # 抽取这20行中每一行的第一个元素
        result = selected_rows.iloc[:, 1]

        # 打印结果
        result_list = result.to_list()

        return result_list
        

def sample_other_words(num):
    with open("/remote-home/xujunhao/en_ai_learn/words/other_words", 'r', encoding='utf-8') as file:
        # 使用列表推导式读取每一行并去除换行符
        lines = [line.strip() for line in file]
    lines = random.sample(lines, num)
    return lines

def sample_enhancement(num):
    with open("/remote-home/xujunhao/en_ai_learn/words/enhancement", 'r', encoding='utf-8') as file:
        # 使用列表推导式读取每一行并去除换行符
        lines = [line.strip() for line in file]
    lines = random.sample(lines, num)
    return lines

words_verb_book = sample_verb_book(start_idx=0, end_idx=259,num=20)
enhancement = sample_enhancement(5)
other_words = sample_other_words(5)
result_list = other_words+enhancement+words_verb_book
# result_list = enhancement

output = "康康今天的单词, 看看你忘了多少 (不会的标记一下, 然后再去查查):\n"
for idx, w in enumerate(result_list):
    output += f"{idx+1}. {w}\n"

print(output)
