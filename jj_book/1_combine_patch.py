from pathlib import Path

# 设置要合并的文件夹路径
folder_path = Path('/remote-home/xujunhao/en_ai_learn/jj_book/patch')
# 设置合并后文件的保存路径
output_file_path = Path('/remote-home/xujunhao/en_ai_learn/jj_book/merged_file.txt')

def merge_txt_files(folder_path, output_file_path):
    with output_file_path.open('w', encoding='utf-8') as outfile:
        for file_path in sorted(folder_path.glob('*.txt')):
            with file_path.open('r', encoding='utf-8') as infile:
                # 读取内容，替换字符后写入新文件
                content = infile.read().replace('千', '于')
                outfile.write(content + '\n')  # 在文件末尾添加换行符

    print(f"All txt files in '{folder_path}' have been merged into '{output_file_path}', with '千' replaced by '于'.")

# 调用函数执行合并
merge_txt_files(folder_path, output_file_path)
