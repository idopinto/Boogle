import boggle_board_randomizer
import itertools
import math

FILE_NAME = 'boggle_dict.txt'

SIZE_BOARD = 4
MIN_PATH = 3
MAX_PATH = 16
BOARD_COORDINATES = [(i, j) for i in range(SIZE_BOARD) for j in range(SIZE_BOARD)]


def load_words_dict(file_path):
    """This function gets a filepath of file with records and returns it as a list of records."""
    with open(file_path) as data_file:
        word_dict = dict()
        for line in data_file:
            word = line.strip()
            if not word:
                word_dict[""] = True
            else:
                word_dict[word] = True
        return word_dict


def is_legal_coord(row, col):
    return 0 <= row < SIZE_BOARD and 0 <= col < SIZE_BOARD


def check_next_coord(current_coord, next_coord):
    if current_coord == next_coord:
        return False
    if is_legal_coord(next_coord[0], next_coord[1]):
        return math.fabs(current_coord[0] - next_coord[0]) <= 1 and math.fabs(current_coord[1] - next_coord[1]) <= 1
    return False


def is_valid_path(board, path, words):
    if not path:
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
    paths_list = []
    for i in range(SIZE_BOARD):
        for j in range(SIZE_BOARD):
            helper_find_length_n_words(n, board, [(i, j)], paths_list)
    result_lst = []
    for possible_path in paths_list:
        possible_word = is_valid_path(board, possible_path, words)
        if possible_word is not None:
            possible_path = [x for x in possible_path]
            result_lst.append((possible_word, possible_path))
    return result_lst
    # print(paths_list)


def helper_find_length_n_words(n, board, current_path, paths_list):
    if len(current_path) == n:
        paths_list.append(current_path)
        return
    row, col = current_path[-1]
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if is_legal_coord(i, j) and check_next_coord((row, col), (i, j)) and (i, j) not in current_path:
                helper_find_length_n_words(n, board, current_path + [(i, j)], paths_list)


def find_length_n_words2(n, board, words):
    if not isinstance(n, int) or n <= 0:  # MIN_PATH or n > MAX_PATH:
        return []
    n_length_paths_combinations = list(itertools.permutations(BOARD_COORDINATES, n))
    result_lst = list()
    for possible_path in n_length_paths_combinations:
        possible_word = is_valid_path(board, possible_path, words)
        if possible_word is not None:
            possible_path = [x for x in possible_path]
            result_lst.append((possible_word, possible_path))
    return result_lst


# n_length_paths_combinations = list(itertools.permutations(BOARD_COORDINATES, 3))
# print(n_length_paths_combinations)
# print("this ends here")
board = [['A', 'B', 'A', 'N'], ['D', 'O', 'N', 'D'], ['QU', 'I', 'T', 'O'], ['QU', 'I', 'T', 'N']]
word_dict = load_words_dict(FILE_NAME)
print(find_length_n_words(7, board, word_dict))
