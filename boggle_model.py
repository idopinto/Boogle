import ex12_utils, boggle_board_randomizer
from typing import *


class BoggleModel:
    __current_coord: Tuple[int,int]  # is the last coord that was clicked
    __current_display: str  # is the current sequence e.g 'BE' or 'BED' or 'BEDA'
    __previous_coords: List[Tuple[int,int]]  # saves all the previous coords in a a list so the player won't click them again
    __already_found: List[str] # list of all the words the player found
    __word_dict: Dict


    def __init__(self):
        self.restart_game()

    def get_display(self):
        pass

    def get_letter_from_coord(self):
        pass

    def restart_game(self):
        pass



