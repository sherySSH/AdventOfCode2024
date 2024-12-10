from dataclasses import dataclass

@dataclass
class Position:
    x : int
    y : int

def read_file(fpath : str) -> list:
    with open(fpath) as f:
        content : str = f.read()

    content = content.split("\n")
    content = [list(line) for line in content]
    return content

def search_right(grid : list, position : tuple, expected_word : str, searched_word : str):

    searched_letter = grid[position.y][position.x]
    expected_letter = expected_word[len(searched_word)] 
    searched_word = searched_word + searched_letter

    position.x = position.x + 1
    
    # if search goes outside the grid size then immediately return zero
    if position.x >= len(grid[position.y]):
        return 0

    if searched_letter == expected_letter and expected_word == searched_word:
        return 1
    elif searched_letter == expected_letter and expected_word != searched_word:
        return search_right(grid, position, expected_word, searched_word)
    else:
        return 0
    
def search_left(grid : list, position : tuple, expected_word : str, searched_word : str):

    searched_letter = grid[position.y][position.x]
    expected_letter = expected_word[len(searched_word)]
    searched_word = searched_word + searched_letter

    position.x = position.x - 1

    # if search goes outside the grid size then immediately return zero
    if position.x < 0:
        return 0


    if searched_letter == expected_letter and expected_word == searched_word:
        return 1
    elif searched_letter == expected_letter and expected_word != searched_word:
        return search_left(grid, position, expected_word, searched_word)
    else:
        return 0
    

def search_top(grid : list, position : tuple, expected_word : str, searched_word : str):

    searched_letter = grid[position.y][position.x]
    expected_letter = expected_word[len(searched_word)]
    searched_word = searched_word + searched_letter

    position.y = position.y - 1

    # if search goes outside the grid size then immediately return zero
    if position.y < 0:
        return 0

    if searched_letter == expected_letter and expected_word == searched_word:
        return 1
    elif searched_letter == expected_letter and expected_word != searched_word:
        return search_top(grid, position, expected_word, searched_word)
    else:
        return 0
    
def search_bottom(grid : list, position : tuple, expected_word : str, searched_word : str):

    searched_letter = grid[position.y][position.x]
    expected_letter = expected_word[len(searched_word)]
    searched_word = searched_word + searched_letter

    position.y = position.y + 1

    # if search goes outside the grid size then immediately return zero
    if position.y >= len(grid):
        return 0

    if searched_letter == expected_letter and expected_word == searched_word:
        return 1
    elif searched_letter == expected_letter and expected_word != searched_word:
        return search_bottom(grid, position, expected_word, searched_word)
    else:
        return 0

def search_top_right(grid : list, position : tuple, expected_word : str, searched_word : str):

    searched_letter = grid[position.y][position.x]
    expected_letter = expected_word[len(searched_word)]
    searched_word = searched_word + searched_letter

    position.x = position.x + 1
    position.y = position.y - 1

    # if search goes outside the grid size then immediately return zero
    if position.y < 0 or position.x >= len(grid[position.y]):
        return 0

    if searched_letter == expected_letter and expected_word == searched_word:
        return 1
    elif searched_letter == expected_letter and expected_word != searched_word:
        return search_top_right(grid, position, expected_word, searched_word)
    else:
        return 0
    

def search_top_left(grid : list, position : tuple, expected_word : str, searched_word : str):

    searched_letter = grid[position.y][position.x]
    expected_letter = expected_word[len(searched_word)]
    searched_word = searched_word + searched_letter

    position.x = position.x - 1
    position.y = position.y - 1

    # if search goes outside the grid size then immediately return zero
    if position.y < 0 or position.x < 0:
        return 0

    if searched_letter == expected_letter and expected_word == searched_word:
        return 1
    elif searched_letter == expected_letter and expected_word != searched_word:
        return search_top_left(grid, position, expected_word, searched_word)
    else:
        return 0
    

def search_bottom_right(grid : list, position : tuple, expected_word : str, searched_word : str):

    searched_letter = grid[position.y][position.x]
    expected_letter = expected_word[len(searched_word)]
    searched_word = searched_word + searched_letter

    position.x = position.x + 1
    position.y = position.y + 1

    # if search goes outside the grid size then immediately return zero
    if position.y >= len(grid) or position.x >= len(grid[position.y]):
        return 0

    if searched_letter == expected_letter and expected_word == searched_word:
        return 1
    elif searched_letter == expected_letter and expected_word != searched_word:
        return search_bottom_right(grid, position, expected_word, searched_word)
    else:
        return 0
    

def search_bottom_left(grid : list, position : tuple, expected_word : str, searched_word : str):

    searched_letter = grid[position.y][position.x]
    expected_letter = expected_word[len(searched_word)]
    searched_word = searched_word + searched_letter

    position.x = position.x - 1
    position.y = position.y + 1

    # if search goes outside the grid size then immediately return zero
    if position.y >= len(grid) or position.x < 0:
        return 0

    if searched_letter == expected_letter and expected_word == searched_word:
        return 1
    elif searched_letter == expected_letter and expected_word != searched_word:
        return search_bottom_left(grid, position, expected_word, searched_word)
    else:
        return 0

def search_word(grid, word):
    word_count = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):

            word_count += search_right(grid, Position(x=x, y=y), word, '')
            word_count += search_left(grid, Position(x=x, y=y), word, '')
            word_count += search_top(grid, Position(x=x, y=y), word, '')
            word_count += search_bottom(grid, Position(x=x, y=y), word, '')
            word_count += search_top_right(grid, Position(x=x, y=y), word, '')
            word_count += search_top_left(grid, Position(x=x, y=y), word, '')
            word_count += search_bottom_right(grid, Position(x=x, y=y), word, '')
            word_count += search_bottom_left(grid, Position(x=x, y=y), word, '')
    
    return word_count

def search_words(grid, word_list):
    word_count_dict = {}
    for word in word_list:
        word_count = search_word(grid, word)
        word_count_dict[word] = word_count
    return word_count_dict

if __name__ == "__main__":

    grid = read_file("input.txt")
    result = search_right(grid, Position(x=6, y=0), 'XMAS', '')
    print(result)
    result = search_left(grid, Position(x=43, y=0), 'XMAS', '')
    print(result)
    result = search_top(grid, Position(x=30, y=138), 'XMAS', '')
    print(result)
    result = search_bottom(grid, Position(x=76, y=117), 'XMAS', '')
    print(result)

    word_list = ['XMAS']

    word_count_dict = search_words(grid, word_list)
    print(word_count_dict)