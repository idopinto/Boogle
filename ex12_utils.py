import boggle_board_randomizer
import itertools
import math

SIZE_BOARD = 4

BOARD_COORDINATE = [(i, j) for i in range(SIZE_BOARD) for j in range(SIZE_BOARD)]


def load_words_dict(file_path):
    """This function gets a filepath of file with records and returns it as a list of records."""
    with open(file_path) as data_file:
        word_dict = dict()
        for line in data_file:
            word = line.strip().split()
            word_dict[word[0]] = True
        return word_dict


#
# print(load_words_dict("boggle_dict.txt"))
# print(BOARD_COORDINATE)


def is_legal_coord(row, col):
    return 0 <= row < SIZE_BOARD and 0 <= col < SIZE_BOARD


def check_next_coord(current_coord, next_coord):
    return math.fabs(current_coord[0] - next_coord[0]) <= 1 and math.fabs(current_coord[1] - next_coord[1]) <= 1


def is_valid_path(board, path, words):
    if len(path) < 3:
        return None
    word = ''
    for cur in range(len(path) - 1):
        if not is_legal_coord(path[cur][0], path[cur][1]) or not check_next_coord(path[cur], path[cur + 1]):
            return None
        word += board[path[cur][0]][path[cur][1]]
    word += board[path[-1][0]][path[-1][1]]
    if word in words.keys() and words[word]:
        return word
    else:
        return None


def find_length_n_words(n, board, words):
    # if not 3 <= n <= 16:
    #     return None
    if not isinstance(n, int) or n < 3 or n > 16:
        raise ValueError("Invalid length")

    length_n_words = {word: cond for (word, cond) in words.items() if len(word) == n}
    n_length_paths_combinations = list(itertools.combinations(BOARD_COORDINATE, n))

        # for path in n_length_paths_combinations:
        #     print(path)
    result_lst = list()
    for possible_path in n_length_paths_combinations:
        possible_word = is_valid_path(board, possible_path, length_n_words)
        if possible_word is not None and length_n_words[possible_word]:
            length_n_words[possible_word] = False
            result_lst.append((possible_word,[possible_path]))
    return result_lst
    # except ValueError:
    #     print("Invalid length")

    #
    # for word in length_n_words:
    #     print(word)


board = boggle_board_randomizer.randomize_board()
# print(is_valid_path(board,[()]))
my_dict = load_words_dict("boggle_dict.txt")
# print(load_words_dict("boggle_dict.txt"))
#
board1= [['A','A','B',"C"],['E','S','D','E'],['Z','QU','A','P'],['A','B','S','D']]
for line in board1:
    print(line)
#print(is_valid_path(board,[(4,2),(4,3),(4,4)],my_dict))

print(find_length_n_words('22', board1, my_dict))
# print(is_valid_path(board1,[(0, 2),(1, 3),(1, 2),(2,2),(3,2)],my_dict))
# print(is_valid_path(board1,[(0, 2),(1, 3),(1, 2),(2,2),(3,2)],my_dict))
