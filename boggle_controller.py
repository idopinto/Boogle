from boggle_gui import *
from boggle_model import *

class BoggleController:
    def __init__(self):
        self._gui = BoggleGame()
        self._model = BoggleModel()
        x = self._model.get_board()
        self._gui.set_board(x)
        self._gui.create_board()
        y = self._model.get_n_length_dict()
        reset = Button(self._gui.frames["Board"].reset_and_check, text="Reset", **LETTER_STYLE, command=self.reset)
        check = Button(self._gui.frames["Board"].reset_and_check, text="Check", **LETTER_STYLE, command=self.check)
        reset.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=tki.NSEW)
        check.grid(row=0, column=1, rowspan=1, columnspan=1, sticky=tki.NSEW)
        self._gui.set_words_left(y)
        self._gui.create_words_left()
        self._gui.set_display()
        self._play_again_button = tki.Button(self._gui.frames["PlayAgain"], bg=REGULAR_COLOR, highlightbackground=REGULAR_COLOR, highlightthickness=5,
                                        font=("Courier", 15), text="Play again", padx=30, pady=8,
                                        command=self.restart)
        self._play_again_button.pack(side=tki.TOP)



    def check(self):
        x = self._gui.get_path()
        self._model.set_path(x)
        self._model.set_current_display(self._gui.letters_displsy)
        self._model.match_word()
        y = self._model.get_score()
        a = self._gui.score
        if a != y:
            self._gui.found_words_counter += 1
            self._gui.set_score(y)
            self._gui.set_display()
            d = self._model.get_n_length_dict()
            self._gui.set_words_left(d)
            self._gui.set_display()
            z = self._model.get_already_found()
            self._gui.set_found_words(z)
            self._gui.create_found_words()
            self._gui.update_words_left()
            self.reset()
        else:
            self.reset()



    def reset(self):
        self._gui._path = []
        self._gui.letters_displsy = ''
        self._gui.set_display()



    def run(self):
        self._gui.run()



    def restart(self):
        self._model.restart_game()
        self._gui.seconds_left = 180
        self._gui.set_board( self._model.get_board())
        self._gui.create_board()
        self._gui.set_words_left(self._model.get_n_length_dict())
        reset = Button(self._gui.frames["Board"].reset_and_check, text="Reset", **LETTER_STYLE, command=self.reset)
        check = Button(self._gui.frames["Board"].reset_and_check, text="Check", **LETTER_STYLE, command=self.check)
        reset.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=tki.NSEW)
        check.grid(row=0, column=1, rowspan=1, columnspan=1, sticky=tki.NSEW)
        self._gui.show_frame("Board")
        self._gui.create_words_left()
        self._gui.update_words_left()
        self._gui.found_words = self._model.get_already_found()
        self._gui.create_found_words()
        self._gui.score = self._model.get_score()
        self._gui.set_display()



if __name__ == "__main__":
    BoggleController().run()