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
# . mul... do
# . mul... dont
# do mul... do
# do mul... dont
# dont mul... do
# dont mul... dont

def parse_conditional_muls(content : str):
    do_regex = re.compile("(do\(\))")
    dont_regex = re.compile("(don't\(\))")
    mul_regex = re.compile("mul\(\d{1,3},\d{1,3}\)")

    
    mul_list = do_regex.finditer(content)
    print(list(mul_list))

    mul_list = dont_regex.finditer(content)
    print(list(mul_list))

    mul_list = mul_regex.finditer(content)
    print(list(mul_list))

    mul_list = [mul[1] for mul in mul_list]
    factors = []
    for mul in mul_list:
        mul = mul.replace("mul(","").replace(")","")
        factors.append(tuple(mul.split(",")))
    
    sum = 0
    for factor in factors:
        sum += int(factor[0]) * int(factor[1])

    return sum

if __name__ == "__main__":
    content = read_file("input.txt")
    sum = parse_muls(content)
    print("Part a", sum)

    content = "do()"+content
    sum = parse_conditional_muls(content)
    print("Part b", sum)
