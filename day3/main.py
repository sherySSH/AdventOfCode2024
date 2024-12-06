import os
import re

def read_file(fpath : str) -> str:
    with open(fpath) as f:
        content : str = f.read()
    return content

def parse_muls(content : str):
    regex = re.compile("mul\(\d{1,3},\d{1,3}\)")
    mul_list = regex.findall(content)
    factors = []
    for mul in mul_list:
        mul = mul.replace("mul(","").replace(")","")
        factors.append(tuple(mul.split(",")))
    
    sum = 0
    for factor in factors:
        sum += int(factor[0]) * int(factor[1])

    return sum


def parse_conditional_muls(content : str):
    do_regex = re.compile("(do\(\))")
    dont_regex = re.compile("(don't\(\))")
    mul_regex = re.compile("mul\(\d{1,3},\d{1,3}\)")

    
    do_iter = do_regex.finditer(content)
    dont_iter = dont_regex.finditer(content)
    mul_iter = mul_regex.finditer(content)
    print(list(dont_iter))
    valid_range_list = []
    for do in list(do_iter):
        do_span = do.span()
        for dont in list(dont_iter):
            dont_span = dont.span()
            if do_span[1] < dont_span[0]:
                valid_range_list.append((do_span[1] , dont_span[0]))
                break
    
    sum = 0
    print(valid_range_list)
    for valid_range in valid_range_list:
        for mul in list(mul_iter):
            mul_span = mul.span()
            if valid_range[0] < mul_span[0] and valid_range[1] > mul_span[1]:
                print(mul)

    # mul_list = [mul[1] for mul in mul_list]
    # factors = []
    # for mul in mul_list:
    #     mul = mul.replace("mul(","").replace(")","")
    #     factors.append(tuple(mul.split(",")))
    
    # sum = 0
    # for factor in factors:
    #     sum += int(factor[0]) * int(factor[1])

    return sum

if __name__ == "__main__":
    content = read_file("input.txt")
    sum = parse_muls(content)
    print("Part a", sum)

    content = "do()"+content
    sum = parse_conditional_muls(content)
    print("Part b", sum)
