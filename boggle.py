from boggle_gui import *
from boggle_model import *


class BoggleController:
    """This Class is the controller of the boggle. it represent the controller of the game which
    connects the model and the gui. A BoggleController is familiar with the model and the gui."""

    def __init__(self):
        """The constructor of the BoggleController holds the gui and the model. the constructor calls
        methods from the model and than sets data returned to the gui to start a clear new game. """
        self._gui = BoggleGame()
        self._model = BoggleModel()
        x = self._model.get_board()
        self._gui.set_board(x)
        self._gui.create_board()
        y = self._model.get_n_length_dict()
        self._gui.set_words_left(y)
        self._gui.create_words_left()
        self._gui.set_display()  # sets display after building the main screen
        reset = tki.Button(self._gui.frames["Board"].reset_and_check, text="Reset", **LETTER_STYLE,
                       command=self.reset)  # creates the reset button.
        check = tki.Button(self._gui.frames["Board"].reset_and_check, text="Check", **LETTER_STYLE,
                       command=self.check)  # creates the check word button.
        reset.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=tki.NSEW)
        check.grid(row=0, column=1, rowspan=1, columnspan=1, sticky=tki.NSEW)
        play_again_button = tki.Button(self._gui.frames["PlayAgain"], bg=REGULAR_COLOR,
                                       highlightbackground=REGULAR_COLOR, highlightthickness=5,
                                       font=("Courier", 15), text="Play again", padx=30, pady=8,
                                       command=self.restart)  # creates the play again button.
        play_again_button.pack(side=tki.TOP)

    def check(self):
        """This function is the command of the check button. When the player presses the check
        button, this function checks if the current word displayed on the screen is a word in the dictionary and
        also if it's the first time the player has found this word. if all True, the function also updates the
        score. The function uses the gui data, calls the model functions to create the new data and sets it to gui.
        """
        x = self._gui.get_path()  # path of current word displayed
        self._model.set_path(x)  # sets the path from gui to the model
        self._model.set_current_display(self._gui.letters_display)
        self._model.match_word()  # checks if the path is legal and if the word existed and never found before. if yes, also update the model score.
        curr_score = self._gui.score
        new_score = self._model.get_score()
        if curr_score != new_score:  # word is okay
            pygame.mixer.music.load("Sounds/correct.mp3")
            pygame.mixer.music.play()
            self._gui.found_words_counter += 1
            self._gui.set_score(new_score)
            self._gui.set_display()
            d = self._model.get_n_length_dict()
            self._gui.set_words_left(d)  # updates the dict of words left
            self._gui.set_display()
            z = self._model.get_already_found()
            self._gui.set_found_words(z)  # sets the already found words to the gui
            self._gui.create_found_words()
            self._gui.update_words_left()
            self.reset()
        else:  # the word is not okay
            pygame.mixer.music.load("Sounds/wrong.mp3")
            pygame.mixer.music.play()
            self.reset()

    def reset(self):
        """This function is the command of the reset button. When the player presses the reset
        button, this function clears the screen, means clear the current path and display".
        """
        self._gui._path = []
        self._gui.letters_display = ''
        self._gui.set_display()

    def run(self):
        """this method runs the game. it calls the run method of the gui."""
        self._gui.run()

    def restart(self):
        """This method, when called, restarts the game. It calls
        methods from the model and than sets data returned to the gui to start a clear new game,
        similar to the constructor."""
        self._model.restart_game()
        self._gui.seconds_left = 180
        self._gui.set_board(self._model.get_board())
        self._gui.create_board()
        self._gui.set_words_left(self._model.get_n_length_dict())
        reset = tki.Button(self._gui.frames["Board"].reset_and_check, text="Reset", **LETTER_STYLE, command=self.reset)
        check = tki.Button(self._gui.frames["Board"].reset_and_check, text="Check", **LETTER_STYLE, command=self.check)
        reset.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=tki.NSEW)
        check.grid(row=0, column=1, rowspan=1, columnspan=1, sticky=tki.NSEW)
        self._gui.show_frame("Board") # calls the show frame with frame Board to start the main gui methods.
        self._gui.create_words_left()
        self._gui.update_words_left()
        self._gui.found_words = self._model.get_already_found()
        self._gui.create_found_words()
        self._gui.score = self._model.get_score()
        self._gui.set_display()


if __name__ == "__main__":
    BoggleController().run()