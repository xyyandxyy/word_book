import pandas as pd
import openai
from openai import OpenAI
client = OpenAI(api_key='sk-3Cesgcjbtyjdr5IX4e9f49B596A1428383Af4f42A85fD978', base_url="https://www.gptapi.us/v1/")

def generate_sentence(row):
    word= row[0]
    meaning= row[1]
    # 调用API生成文本
    cnt = 0
    is_ok = False
    while(not is_ok):
        is_error = False
        try:
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"给你一个英文单词(同时包含对应的中文意思, 请避免因为一词多义造成误解), 请你生成一句包含这个单词的简单英文句子(注意其他涉及的单词能让词汇量不超过500的孩子看懂), 同时在这句话之后输出对应中文翻译. 例如输入 employ(),你输出(注意不要换行): They employ force to enter the building. 他们不得不强行进入大楼. 现在我给你的单词是{word}\({meaning}\(注意只要输出一句英文和对应中文, 不要输出其他任何内容))"}
            ]
            )
            output = response.choices[0].message.content.strip()
            stop_list = ["现在我给你的", "下一个单词", "---", "这个单词是", "\n"]
            for stop_word in stop_list:
                if stop_word in output:
                    is_error = True
                    break
        except Exception as e:
            print("报错, 没有例句, 用NULL占位")
            output = "NULL"

        # 打印生成的文本
        

        if not is_error:
            is_ok = True
        elif cnt > 10:
            is_ok = True
        else:
            cnt += 1
            print(f"出现停用词, 再次尝试")
                

    print(f"{word};{meaning};{output}")
    return output

def remove_adjacent_duplicates(arr, word):
    """去掉连续两个数字的第二个数字

    Args:
        arr (_type_): _description_
        word (_type_): _description_

    Returns:
        _type_: _description_
    """
    result = []
    i = 0
    while i < len(arr):
        result.append(arr[i])
        while i + 1 < len(arr) and arr[i] + 1 == arr[i + 1]:
            i += 1
        i += 1
    return result

def divide_into_syllables(word):
    """根据输入单词划分读音

    Args:
        word (_type_): _description_

    Returns:
        _type_: _description_
    """
    vowels = "aeiouy"  # 元音字母
    array_idx = []
    for idx, letter in enumerate(word):
        if letter in vowels:
            array_idx.append(idx-1)

    # 检查两个元音连续的情况
    array_idx = remove_adjacent_duplicates(array_idx, word)
    # print(array_idx)
    word_split = []

    for idx, pos in enumerate(array_idx):
        if idx == 0:
            if idx == len(array_idx)-1:
                # 单音节词
                return word
            word_split.append(word[:array_idx[idx+1]])
        elif idx == len(array_idx)-1:
            word_split.append(word[array_idx[idx]:])
        else:
            word_split.append(word[array_idx[idx]:array_idx[idx+1]])

    if len(word_split) > 1:
        split_word = "-".join(word_split)
    else:
        split_word = word
    return split_word
    
def get_split(input, delimiter):
    """按照原始split去划分词, 同时保留split用的delimiter在下一个元素中

    Args:
        input (_type_): _description_
        delimiter (_type_): _description_

    Returns:
        _type_: _description_
    """
    arr = input.split(delimiter)
    for idx, ele in enumerate(arr):
        if idx != 0:
            arr[idx] = delimiter+ele
    return arr


def get_noun_meaning(input_string):
    if "动物园" in input_string:
        print(1)
    # 使用 ';' 和"\n" 进行分割字符串

    substrings = input_string.split("\n")
    types = ['n.', 'adj.', 'adv.', 'pron.', 'v.', 'prep.', 'num.', 'vi.', 'vt.', 'int.', 'aux.', 'pron.', 'conj.', 'abbr.', 'aux.']
    for t in types:
        substrings = [get_split(s,t) for s in substrings]
        substrings = [item for sublist in substrings for item in sublist]

    
    # 遍历子串，找到包含 "n." 的子串
    for substring in substrings:
        if "v." in substring or "vt." in substring or "vi." in substring:
                return substring
    return input_string


if __name__ == "__main__":
    # 读取xlsx文件
    df = pd.read_excel('word_list.xlsx')
    print("单词总数:", df.shape[0])
    # 保留名词
    # exist_n = df.iloc[:,3].str.contains('n\.')& (~df.iloc[:, 3].str.contains('pron\.'))
    exist_n = (df.iloc[:,3].str.contains('v\.')&(~df.iloc[:, 3].str.contains('adv\.'))) | df.iloc[:,3].str.contains('vi\.') | df.iloc[:,3].str.contains('vt\.')
    result = df.iloc[exist_n.values, [0,3]]
    print("筛选后单词数:", result.shape[0])
    # 只去名词含义

    result.iloc[:,1] = result.iloc[:,1].apply(get_noun_meaning)
    result["划分"] = result.iloc[:,0].apply(divide_into_syllables)
    result['例句'] = result.apply(generate_sentence, axis=1)
    result = result.reset_index(drop=True)
    # 打印结果
    print(result)
    result.to_csv('/remote-home/xujunhao/en_ai_learn/output_v_2.csv', index="序号")
    print("======弄好了======")