from ex12_utils import *
import boggle_board_randomizer
from typing import *

FILE_NAME = 'boggle_dict.txt'


class BoggleModel:
    __current_coord: Tuple[int, int]  # is the last coord that was clicked
    __current_display: str  # is the current sequence e.g 'BE' or 'BED' or 'BEDA'
    __current_path: List[
        Tuple[int, int]]  # saves all the previous coords in a a list so the player won't click them again
    __already_found: List[str]  # list of all the words the player found
    __word_dict: Dict
    __board: List[List[str]]
    __score: int
    __n_length_dict: Dict

    def __init__(self):
        self.restart_game()

    def slice_path(self):
        if self.__current_coord in self.__current_path:
            self.__current_path = self.__current_path[:self.__current_path.index(self.__current_coord) + 1]

    def match_word(self):
        n = len(self.__current_display)
        if self.__current_display in self.__word_dict.keys() and self.__word_dict[self.__current_display] is False:
            return

        # if (self.__current_display, self.__current_path) in find_length_n_words(n, self.__board, self.__word_dict):
        if is_valid_path(self.__board, self.__current_path, self.__word_dict) == self.__current_display:
            self.__word_dict[self.__current_display] = False
            self.update_score(n ** 2)
            self.__already_found.append(self.__current_display)
            self.update_n_length_dict(n)
            self.__current_display = ''
            self.reset_path()
            return
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # ~~~~~~~~~~~~~~~~RESET_METHODS~~~~~~~~~~~~~~~#
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def reset_path(self):
        self.__current_path = list()

    def restart_game(self):
        self.__current_coord = tuple()
        self.__current_display = ''
        self.__current_path = list()
        self.__already_found = list()
        self.__word_dict = load_words_dict(FILE_NAME)
        self.__board = boggle_board_randomizer.randomize_board() #[['A', 'B','A', 'N'], ['D', 'O','N', 'D'], ['QU', 'I','T', 'O'], ['QU', 'I','T', 'N']]
        self.__score = 0
        self.__n_length_dict = self.set_n_length_dict()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # ~~~~~~~~~~~~~~~~~SETTERS~~~~~~~~~~~~~~~~~~~~#
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def set_n_length_dict(self):
        n_length_dict = dict()
        for i in range(MIN_PATH, 6):
            x = len(find_length_n_words(i, self.__board, self.__word_dict))
            # if x > 0:
            if i < 8:
                n_length_dict[i] = x
        return n_length_dict

    def set_current_coord(self, coord):
        self.__current_coord = coord

    def set_display(self):
        self.__current_display += self.get_letter_from_coord()
        self.update_path(self.__current_coord)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # ~~~~~~~~~~~~~~~~~GETTERS~~~~~~~~~~~~~~~~~~~~#
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def get_score(self):
        return self.__score

    def get_board(self):
        return self.__board

    def get_n_length_dict(self):
        return self.__n_length_dict

    def get_letter_from_coord(self):
        return self.__board[self.__current_coord[0]][self.__current_coord[1]]

    def get_path(self):
        return self.__current_path

    def get_display(self):
        return self.__current_display

    def get_already_found(self):
        return self.__already_found

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # ~~~~~~~~~~~~~~~~UPDATE_METHODS~~~~~~~~~~~~~~#
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def update_score(self, n):
        self.__score += n

    def update_n_length_dict(self, n):
        if self.__n_length_dict[n] >= 1:
            self.__n_length_dict[n] -= 1
            # if self.__n_length_dict[n] == 0:
            #     del self.__n_length_dict[n]

    def update_path(self, coord):
        self.__current_path.append(coord)

    def set_path(self, path):
        self.__current_path = path

    def set_current_display(self, display):
        self.__current_display = display



# x = BoggleModel()
# lst = x.get_board()
# for line in lst:
#     print(line)
# print(x.set_n_length_dict())
# x.set_current_coord((0, 2))
# x.set_display()
# x.set_current_coord((1, 3))
# x.set_display()
# # x.set_current_coord((2,3))
# # # x.set_display()
# x.set_current_coord((1, 2))
# x.set_display()
# x.set_current_coord((2, 2))
# x.set_display()
# x.set_current_coord((3, 3))
# x.set_display()
# x.set_current_coord((3, 2))
# x.set_display()
# print(x.get_path())
# print(x.get_display())
# x.match_word()
# print(x.get_score())
# # x.slice_path()
# # print(x.get_path())
# print(x.get_n_length_dict())
