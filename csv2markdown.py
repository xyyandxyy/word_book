import pandas as pd

df = pd.read_csv('/remote-home/xujunhao/en_ai_learn/verb_book_v0.csv')  # 以你的DataFrame来源替换这里
df = df.iloc[:,1:]

df.insert(0, '序号', df.index)

# 定义一个函数，将DataFrame的一部分转换为Markdown表格
def df_to_markdown(df):
    markdown = df.to_markdown(index=False)  # 转换为Markdown，不包含索引
    return markdown

# 将DataFrame分割成多个部分，每个最大为20行
parts = [df[i:i + 20] for i in range(0, len(df), 20)]

# 初始化Markdown字符串
markdown_output = ""

# 遍历每个部分，转换为Markdown并添加到输出字符串
for i, part in enumerate(parts):
    markdown_output += f"# 背动词的第 {i + 1}天\n\n"  # 添加一级标题
    markdown_output += df_to_markdown(part) + "\n\n"  # 添加Markdown表格



with open('output.md', 'w', encoding='utf-8') as f:
    f.write(markdown_output)

print("好了")