def get_split(input, delimiter):
    arr = input.split(delimiter)
    for idx, ele in enumerate(arr):
        if idx != 0:
            arr[idx] = delimiter+ele
    return arr

input = "abcbd"
arr = get_split(input, "b")
print(arr)