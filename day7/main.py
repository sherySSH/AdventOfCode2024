import os
from dataclasses import dataclass
from typing import List, Callable

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



def search_tree_a(total : int, numbers : list, mode : str):
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

    If we get the correct total after applying the operations then we return
    correct result and if we do not get correct answer then we simply return
    the left most branch of the tree which is just the addition of all numbers

                                ^
                               / \
                              +   *
                             /     \
                 <num_i,num_j>       <num_i,num_j>
                    / \                 / \
                   +   *               +   *
                  /     \             /     \
             <ni,nj>   <ni,nj>   <ni,nj>   <ni,nj>
              / \        / \       / \       / \
             +   *      +   *     +   *     +   *
            /     \    /     \   /     \   /     \
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
    result = search_tree_a(total, numbers, mode='multiply')
    if result != total:
        # create left branch
        result = search_tree_a(total, numbers, mode='addition')
    
    return result


def search_tree_b(total : int, numbers : list, mode : str):

    """
    In this case we have three possible operators:
    1) Multiply
    2) Add
    3) Concatenation

    There instead of creating a binary tree we need to induce a search
    tree where each node at max may have three branches. Right one will
    be multiply, middle branch will be add and left branch will be concat
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

    elif mode == 'concat':

        numbers = list(reversed(numbers))
        num_i = numbers.pop()
        num_j = numbers.pop()
        num_k = int( str(num_i) + str(num_j) )
        numbers.append( num_k )
        numbers = list(reversed(numbers))

    else:
        pass

    # create right branch
    result = search_tree_b(total, numbers, mode='multiply')
    if result != total:
        # create mid branch
        result = search_tree_b(total, numbers, mode='addition')
        if result != total:
            # create left branch
            result = search_tree_b(total, numbers, mode='concat')
    
    return result


def sum_correct_calibrations(equations : List[Equation], search_tree : Callable):
    sum = 0
    for equation in equations:
        result = search_tree(equation.total , equation.numbers, mode='root')
        if result == equation.total:
            sum += result

    return sum



if __name__ == "__main__":
    content = read_file("input.txt")
    equations : List[Equation] = preprocessing(content)

    sum = sum_correct_calibrations(equations, search_tree=search_tree_a)
    print("Part a:", sum)

    sum = sum_correct_calibrations(equations, search_tree=search_tree_b)
    print("Part b:", sum)