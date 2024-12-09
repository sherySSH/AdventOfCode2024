import os
import re

def read_file(fpath : str) -> str:
    with open(fpath) as f:
        content : str = f.read()
    return content

def parse_muls(content : str):
    #find all muls
    regex = re.compile("mul\(\d{1,3},\d{1,3}\)")
    mul_list = regex.findall(content)
    
    factors = []
    for mul in mul_list:
        # do some string processing and extract numbers
        mul = mul.replace("mul(","").replace(")","")
        # type case number from str to int
        factors.append(tuple(mul.split(",")))
    
    # product-sum
    sum = 0
    for factor in factors:
        sum += int(factor[0]) * int(factor[1])

    return sum


def parse_conditional_muls(content : str):

    # match do() or match mul(ddd,ddd) or match don't()
    all_regex = re.compile("(do\(\))|(mul\(\d{1,3},\d{1,3}\))|(don't\(\))")
    all_list = list(all_regex.finditer(content))

    
    enabled_muls = []
    sum = 0
    # reverse traversal of matched elements
    for element in reversed(all_list):
        group = element.group()
        # if while reverse traversal we encounter do() instruction then we immediately product-sum muls that we have found so far
        if group == 'do()':
            for enabled_mul in enabled_muls:
                mul = enabled_mul.replace("mul(","").replace(")","")
                factors = mul.split(",")
                sum += int(factors[0]) * int(factors[1])
            enabled_muls = []
        # if we encounter don't() then we simply drop the muls that we encountered so far
        elif group == 'don\'t()':
            enabled_muls = []
        else:
            # if we do not encounter do()/dont'() then we must have gotten mul obviously, there are just 3 choices after matching regex
            enabled_muls.append(group)

    return sum

if __name__ == "__main__":
    content = read_file("input.txt")
    sum = parse_muls(content)
    print("Part a", sum)

    content = "do()"+content
    sum = parse_conditional_muls(content)
    print("Part b", sum)
