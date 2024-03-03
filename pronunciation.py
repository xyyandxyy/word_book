
def remove_adjacent_duplicates(arr, word):
    result = []
    i = 0
    while i < len(arr):
        result.append(arr[i])
        while i + 1 < len(arr) and arr[i] + 1 == arr[i + 1]:
            i += 1
        i += 1
    return result

def divide_into_syllables(word):
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
                word_split.append(word)
                return word_split
            word_split.append(word[:array_idx[idx+1]])
        elif idx == len(array_idx)-1:
            word_split.append(word[array_idx[idx]:])
        else:
            word_split.append(word[array_idx[idx]:array_idx[idx+1]])
    return word_split
    

word = ["pronunciation", "baseline", "learn", "play", "dinner", "lucky", "debug", "Bravery", "Friendship", "Courage", "Responsibility", "adjacent"]
for w in word:
    syllables = divide_into_syllables(w)
    print(syllables)
