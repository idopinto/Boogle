from ex12_utils import *
import boggle_board_randomizer
from typing import *

FILE_NAME = 'boggle_dict.txt'


class BoggleModel:
    """this class is the logical part of the game."""
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
        """this function initializes the game"""
        self.restart_game()

    def match_word(self):
        """this is the main function which check if current display is a vaild name from dictionary, if it is then the
        function update score, n_length_dict, already_found list and reset path and display"""
        n = len(self.__current_display)
        if self.__current_display in self.__word_dict.keys() and self.__word_dict[self.__current_display] is False:
            return
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
        """this function reset path to empty list"""
        self.__current_path = list()

    def restart_game(self):
        """this function initializes the game"""
        self.__current_coord = tuple()
        self.__current_display = ''
        self.__current_path = list()
        self.__already_found = list()
        self.__word_dict = load_words_dict(FILE_NAME)
        self.__board = boggle_board_randomizer.randomize_board()  # [['A', 'B','A', 'N'], ['D', 'O','N', 'D'], ['QU', 'I','T', 'O'], ['QU', 'I','T', 'N']]
        self.__score = 0
        self.__n_length_dict = self.set_n_length_dict()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # ~~~~~~~~~~~~~~~~~SETTERS~~~~~~~~~~~~~~~~~~~~#
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    def set_n_length_dict(self):
        """this function set the dictionary which represents how many words there are in the game with specific lengths
        such as {n: num of words with n length word}"""
        n_length_dict = dict()
        for i in range(MIN_PATH, 8):
            x = len(find_length_n_words(i, self.__board, self.__word_dict))
            if i < 9:
                n_length_dict[i] = x
        return n_length_dict

    def set_current_coord(self, coord):
        """this function get coord and set the current coord variable"""
        self.__current_coord = coord


    def set_path(self, path):
        """this function set the current path"""
        self.__current_path = path

    def set_current_display(self, display):
        """this function set the current display"""
        self.__current_display = display

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # ~~~~~~~~~~~~~~~~~GETTERS~~~~~~~~~~~~~~~~~~~~#
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def get_score(self):
        """this function return score"""
        return self.__score

    def get_board(self):
        """this function return the board"""
        return self.__board

    def get_n_length_dict(self):
        """this function return the n_length_dict"""
        return self.__n_length_dict

    def get_path(self):
        """this function returns the current path"""
        return self.__current_path

    def get_display(self):
        """This function returns the current display """
        return self.__current_display

    def get_already_found(self):
        """this function return list of all the words that already found """
        return self.__already_found

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # ~~~~~~~~~~~~~~~~UPDATE_METHODS~~~~~~~~~~~~~~#
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def update_score(self, n):
        """this function updates the score"""
        self.__score += n

    def update_n_length_dict(self, n):
        """this function update """
        if self.__n_length_dict[n] >= 1:
            self.__n_length_dict[n] -= 1

    def update_path(self, coord):
        """this function updates the current path"""
        self.__current_path.append(coord)


