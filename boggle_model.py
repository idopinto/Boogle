import ex12_utils, boggle_board_randomizer
from typing import *

FILE_NAME = 'boggle_dict.txt'


class BoggleModel:
    __current_coord: Tuple[int, int]  # is the last coord that was clicked
    __current_display: str  # is the current sequence e.g 'BE' or 'BED' or 'BEDA'
    __previous_coords: List[Tuple[int, int]]  # saves all the previous coords in a a list so the player won't click them again
    __already_found: List[str]  # list of all the words the player found
    __word_dict: Dict
    __board: List[List[str]]

    def __init__(self):
        self.restart_game()

    def get_display(self):
        pass

    def get_letter_from_coord(self):
        pass

    def restart_game(self):
        self.__current_coord = tuple()
        self.__current_display = ''
        self.__previous_coords = list()
        self.__already_found = list()
        self.__word_dict = ex12_utils.load_words_dict(FILE_NAME)
        self.__board = boggle_board_randomizer.randomize_board()

    def get_board(self):
        return self.__board


x = BoggleModel()
lst = x.get_board()
for line in lst:
    print(line)
