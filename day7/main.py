import os
from dataclasses import dataclass
from typing import List

@dataclass
class Equation:
    total : int
    numbers : List[int]




def read_file(path : str):
    with open(path, 'r') as f:
        content = f.read()
    return content

def preprocessing(content : str):
    equations : List[Equation] = []
    lines = content.split("\n")
    for line in lines:
        equation = line.split(": ")
        equation = Equation(
            total=int(equation[0]),
            numbers=[int(number) for number in equation[1].split(" ")]
        )
        equations.append(equation)
    return equations 



def search_tree(total : int, numbers : list, mode : str):
    """
    Inducing a binary tree, where right edge is multiply operation
    and left edge is a addition operation conceptually. Tree induction
    is done through recursion. Since we have to create two branches
    therefore search_tree has been called twice recursively.

    But left branch is explored only if we have not found the result
    in the right branch. Therefore, this algorithm is greedy in the sense
    that it will stop as soon as it found the solution which is one of
    the possible correct order of operations. Therefore induced tree can
    be imbalanced.
    """

    if len(numbers) == 1:
        return numbers[0]
    
    elif mode == 'multiply':
        
        numbers = list(reversed(numbers))
        num_i = numbers.pop()
        num_j = numbers.pop()
        numbers.append(num_i * num_j)
        numbers = list(reversed(numbers))

    elif mode == 'addition':

        numbers = list(reversed(numbers))
        num_i = numbers.pop()
        num_j = numbers.pop()
        numbers.append(num_i + num_j)
        numbers = list(reversed(numbers))
    else:
        pass

    # create right branch
    result = search_tree(total, numbers, mode='multiply')
    if result != total:
        # create left branch
        result = search_tree(total, numbers, mode='addition')
    
    return result


def sum_correct_calibrations(equations : List[Equation]):
    sum = 0
    for equation in equations:
        result = search_tree(equation.total , equation.numbers, mode='root')
        if result == equation.total:
            sum += result

    return sum
if __name__ == "__main__":
    content = read_file("input.txt")
    equations : List[Equation] = preprocessing(content)
    # result = search_tree(7290, [6,8,6,15], mode='root')
    # print(result)
    sum = sum_correct_calibrations(equations)
    print("Part a:", sum)