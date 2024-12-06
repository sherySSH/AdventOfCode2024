import os
from collections import Counter

def read_file(fpath : str) -> list:
    with open(fpath) as f:
        content : list = f.readlines()
    return content

def preprocessing(data : list) -> list:
    col1 = []
    col2 = []
    for sample in data:
        row = sample.split("   ")
        col1.append(int(row[0]))
        col2.append(int(row[1].replace("\n","")))

    col1 = sorted(col1)
    col2 = sorted(col2)
    return [col1,col2]

def sum_diff(columns : list):
    sum = 0
    for x,y in zip(*columns):
        diff = abs(x - y)
        sum += diff
    return sum

def get_similarity(unq_left_list, right_list_count):
    similarity = {}
    total = 0
    for key in unq_left_list:
        if key in right_list_count:
            count = right_list_count[key]
            total += key*count
    return total

if __name__ == "__main__":
    content = read_file("input.txt")
    columns = preprocessing(content)
    sum = sum_diff(columns)
    print("Part a:", sum)

    counter_right_list = Counter(columns[1])
    unique_left_list = list(set(columns[0])) 
    total = get_similarity(unique_left_list, counter_right_list)
    print("Part b:", total)