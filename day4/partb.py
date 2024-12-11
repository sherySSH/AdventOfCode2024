from dataclasses import dataclass

# This program utilizes the Breadth-First-Search approach for solving the Part A 


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

def search_breadth(grid, position : Position) -> list:
    center_letter = grid[position.y][position.x]

    top_right_node = grid[position.y-1][position.x+1]
    bottom_right_node = grid[position.y+1][position.x+1]
    bottom_left_node = grid[position.y+1][position.x-1]
    top_left_node = grid[position.y-1][position.x-1]

    # we create tuple in clock-wise direction starting from top-right-node value
    return center_letter, (top_right_node, bottom_right_node, bottom_left_node, top_left_node)

def search_pattern(grid, center_letter, diagonal_letters : set):
    pattern_count = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            backward_diagonal_letters = []
            forward_diagonal_letters = []
            
            if  (y-1) >= 0 and (y+1) < len(grid) and (x-1) >= 0 and (x+1) < len(grid[y]):
                #finding relevant children of current root node (or search node)
                searched_center_letter, breadth_nodes = search_breadth(grid, Position(x=x,y=y))
            # if some corner of search goes outside grid size then abandon current position and move on
            else:
                continue

            if searched_center_letter == center_letter:
                
                for i in range(len(diagonal_letters)):
                    # at even index we should get M or S
                    letter = breadth_nodes[2*i]
                    backward_diagonal_letters.append(letter)
                    # at odd index we should get M or S
                    letter = breadth_nodes[2*i + 1]
                    forward_diagonal_letters.append(letter)
                if set(backward_diagonal_letters) == diagonal_letters and set(forward_diagonal_letters) == diagonal_letters:
                    pattern_count += 1
    return pattern_count

if __name__ == "__main__":
    grid = read_file("input.txt")
    pattern_count = search_pattern(grid, 'A', {'M','S'})
    print("Pattern Count:", pattern_count)