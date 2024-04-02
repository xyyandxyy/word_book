if __name__ == "__main__":
    with open('/remote-home/xujunhao/en_ai_learn/jj_book/merged_file.txt', 'r') as file:
        for idx, line in enumerate(file):
            result = line
            if "■" in line:
                result = "## "+line
            with open('/remote-home/xujunhao/en_ai_learn/jj_book/output.md', 'a', encoding='utf-8') as f:
                f.write(result)

print("好了")