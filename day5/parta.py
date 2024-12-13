import os

def read_file(path : str):
    with open(path, 'r') as f:
        content = f.read()
    return content

# convert string data to a structure
def processing(content : str):
    lines = content.split("\n")
    data = { "rules" : [] , "updates" : []}
    is_rule = True
    is_update = False
    for line in lines:
        if line == '':
            is_rule = False
            is_update = True
        
        if is_rule:
            rule = line.split("|")
            data["rules"].append( (rule[0] , rule[1]) )
        elif is_update and line != '':
            data["updates"].append( line.split("," ))

    return data

def validate_update_sequence(update, rules):
    for i in range(len(update) - 2):
        for j in range(i+1, len(update) - 1):
            is_valid = validate_sorting(rules, update[i], update[j])
            if not is_valid:
                return False
    return True

def validate_sorting(rules, x : str , y : str):
    rule = find_rule(rules, x ,y)
    if x == rule[0] and y == rule[1]:
        return True
    else:
        return False


def find_rule(rules : list, x : str, y : str):
    for rule in rules:
        if x in rule and y in rule:
            return rule
        


def sum_middle_page_number(update_list : list, rules : list):
    # sum of middle page number in valid updates
    sum = 0
    for update in update_list:
        is_valid = validate_update_sequence(update, rules)
        if is_valid:
            mid = (len(update) - 1) // 2
            sum += int(update[mid])
    return sum


def sort_invalid_update(update : list, rules : list):
    for i in range(len(update)):
        for j in range(len(update) - 1):
            is_valid_order = validate_sorting(rules, update[j], update[j+1])
            if not is_valid_order:
                temp = update[j]
                update[j] = update[j+1]
                update[j+1] = temp
    return update

def correct_invalid_updates(update_list : list, rules :list):
    corrected_updates = []
    for update in update_list:
        is_valid = validate_update_sequence(update, rules)
        if not is_valid:
            corrected_update = sort_invalid_update(update, rules)
            corrected_updates.append(corrected_update)
    return corrected_updates
                

if __name__ == "__main__":
    content = read_file("input.txt")
    data = processing(content)
    sum = sum_middle_page_number(data["updates"], data["rules"])
    print("Part a :", sum)

    corrected_updates = correct_invalid_updates(data["updates"], data["rules"])
    sum = sum_middle_page_number(corrected_updates, data["rules"])
    print("Part b: ", sum)
