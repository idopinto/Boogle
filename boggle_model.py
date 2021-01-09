import ex12_utils, boggle_board_randomizer
from typing import *


class BoggleModel:
    __current_letter: str  # is the last letter that was clicked e.g 'B'
    __current_display: str  # is the current sequence e.g 'BE' or 'BED' or 'BEDA'
    __previous_coords: List[str]  # saves all the previous coords in a a list so the player won't click them again

    def __init__(self):
        self.restart_game()

    def get_display(self):
        pass

    def get_letter(self):
        pass

    def restart_game(self):
        pass

