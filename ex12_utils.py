from math import fabs

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
    """this function gets row and col and return whether the coordinate is legal"""
    return 0 <= row < SIZE_BOARD and 0 <= col < SIZE_BOARD


def check_next_coord(current_coord, next_coord):
    """this function gets two coordinates and return if they can be in possible path. """
    if current_coord == next_coord:
        return False
    if is_legal_coord(next_coord[0], next_coord[1]):
        return fabs(current_coord[0] - next_coord[0]) <= 1 and fabs(current_coord[1] - next_coord[1]) <= 1
    return False


def is_valid_path(board, path, words):
    """this function gets the game board, possible path and dictionary of words.
    if the path is valid then return the word, None otherwise"""
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
    """ this function get the game board and dictionary of words
    return list of tuples of all the words in n length and their paths"""
    if not isinstance(n, int) or n > MAX_PATH or n <= 0:  # MIN_PATH or n > MAX_PATH:
        return []
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


def helper_find_length_n_words(n, board, current_path, paths_list):
    """this function is helper. creates list of possible paths"""
    if len(current_path) == n:
        paths_list.append(current_path)
        return
    row, col = current_path[-1]
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if is_legal_coord(i, j) and check_next_coord((row, col), (i, j)) and (i, j) not in current_path:
                helper_find_length_n_words(n, board, current_path + [(i, j)], paths_list)
