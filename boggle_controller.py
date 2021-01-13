from boggle_gui import *
from boggle_model import *

class BoggleController:
    def __init__(self):
        self._gui = BoggleGame()
        self._model = BoggleModel()
        x = self._model.get_board()
        self._gui.set_board(x)
        self._gui.create_board()
        #self._gui.create_words_left()
        self._gui.create_found_words()

    def set_game(self):
        self._gui.set_board(self._model.get_board())



    def run(self):
        self._gui.run()





if __name__ == "__main__":
    BoggleController().run()