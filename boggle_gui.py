import tkinter as tki
from tkmacosx import Button

import datetime

LETTER_HOVER_COlOR = "gray"  # choose colors
REGULAR_COLOR = "white"
LETTER_ACTIVE_COlOR = "slateblue"
LETTER_STYLE = {"font": ("Courier", 30), "borderwidth": 1, "relief": tki.RAISED, "bg": REGULAR_COLOR,
                "activebackground": LETTER_ACTIVE_COlOR}
FILE_NAME = 'boggle_dict.txt'


class BoggleGame(tki.Tk):

    def __init__(self, *args, **kwargs):
        tki.Tk.__init__(self, *args, **kwargs)
        self.title("BoogleGame")
        container = tki.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Startscreen, Board, PlayAgain):
            screen_name = F.__name__
            frame = F(container, self)
            self.frames[screen_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Startscreen")
        self.current_coord = ()
        self._board_letters = []
        self._letters = {}
        self.letters_displsy = ""
        self._path = []
        self.words_left = {}
        self.seconds_left = 10
        self.score = 0
        self.found_words = []
        self.found_words_counter = 0
        self._letters_2 = {}
        self.words_left_labels = {}
        self.game_played_counter = 0


    def get_current_cord(self):
        return self.current_coord

    def set_board(self, board):
        self._board_letters = board

    def set_words_left(self, dict):
        self.words_left = dict

    def set_found_words(self, found_words_list):
        self.found_words = found_words_list

    def set_score(self, score):
        self.score = score

    def set_display(self):
        self.frames["Board"].display_label["text"] = self.letters_displsy
        for coord in self._path:
            self._letters_2[coord]['bg'] = "slateblue"
        self.frames["Board"].display_score["text"] = "Score:" + str(self.score)
        if not self._path:
            for letter in self._letters_2:
                self._letters_2[letter]['bg'] = REGULAR_COLOR

    def get_path(self):
        return self._path

    def create_found_words(self):
        for word in self.found_words[self.found_words_counter - 1:]:
            label = tki.Label(self.frames["Board"].found_words_frame, font=("Courier", 15),
                              bg=REGULAR_COLOR, width=15, text=word)
            label.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

    def update_words_left(self):
        for value in self.words_left_labels.values():
            value[0]['text'] = self.words_left[value[1]]


    def create_words_left(self):
        for i, key in enumerate(self.words_left):
            x = self.make_Frames_for_left_words("i+3", "50", 0, i)
            words_left_label = tki.Label(x, font=("Courier", 30),
                                         bg=REGULAR_COLOR, text=str(key) + ":")
            words_left_label.pack(side=tki.LEFT, fill=tki.BOTH)
            words_left_label__ = tki.Label(x, font=("Courier", 30),
                                           bg=REGULAR_COLOR, width=5, relief="ridge", text=str(self.words_left[key]))
            self.words_left_labels[i] = (words_left_label__,key)
            words_left_label__.pack(side=tki.LEFT, fill=tki.BOTH)

    def make_Frames_for_left_words(self, length, words_left, row, col, rowspan=1, columnspan=1):
        words_left_frame = tki.Frame(self.frames["Board"].words_left_frame, bg=REGULAR_COLOR,
                                     highlightbackground=REGULAR_COLOR,
                                     highlightthickness=5)
        words_left_frame.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=tki.NSEW)

    def create_board(self):
        for i in range(4):
            tki.Grid.columnconfigure(self.frames["Board"].lower_frame, i, weight=1)

        for i in range(4):
            tki.Grid.rowconfigure(self.frames["Board"].lower_frame, i, weight=1)

        for row in range(4):
            for col in range(4):
                self.make_letter(self._board_letters[row][col], row, col)

    def callback(self, row, col):
        self.current_coord = (row, col)
        if self.current_coord in self._path:
            pass
        else:
            self._path.append((row, col))
            self.letters_displsy += self._letters[(row, col)]
            self.set_display()

    def make_letter(self, letter_char, row, col, rowspan=1, columnspan=1):
        letter = Button(self.frames["Board"].lower_frame, text=letter_char, **LETTER_STYLE,
                        command=lambda: self.callback(row, col))
        self._letters_2[(row, col)] = letter
        letter.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=tki.NSEW)
        self._letters[(row, col)] = letter_char

        return letter

    def timer_countdown(self):
        """update label based on the time left"""
        self.frames["Board"].display_time['text'] = self.convert_seconds_left_to_time()
        if self.seconds_left:
            self.seconds_left -= 1
            self.frames["Board"].display_time.after(1000, self.timer_countdown)
        if self.seconds_left == 0:
             # self.seconds_left = 180
             self.frames["PlayAgain"].play_again_frame['text'] = f'Time is up! you ended up with {self.score} points'
             self.frames["PlayAgain"].tkraise()


    def convert_seconds_left_to_time(self):
        return datetime.timedelta(seconds=self.seconds_left)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()
        if container == "Board":
            frame.tkraise()
            self.timer_countdown()
            if self.game_played_counter == 0:
                self.create_words_left()
                self.create_found_words()
                self.game_played_counter += 1
        else:
            pass

    def run(self):
        self.mainloop()




class Startscreen(tki.Frame):

    def __init__(self, parent, controller):
        tki.Frame.__init__(self, parent)
        self._controller = controller
        self._start_frame = tki.Label(self, bg="white", highlightbackground=REGULAR_COLOR, highlightthickness=5,
                                      text="Click start to start playing!", font=("Courier", 20))
        self._start_frame.pack(side=tki.TOP, fill=tki.BOTH, pady=100, padx=10)
        self._start_button = tki.Button(self, bg=REGULAR_COLOR, highlightbackground=REGULAR_COLOR, highlightthickness=5,
                                        font=("Courier", 15), text="Start", padx=30, pady=8,
                                        command=lambda: controller.show_frame("Board"))
        self._start_button.pack(side=tki.TOP)


class Board(tki.Frame):

    def __init__(self, parent, controller):
        tki.Frame.__init__(self, parent)
        self.outer_frame = tki.Frame(self, bg=REGULAR_COLOR, highlightbackground=REGULAR_COLOR, highlightthickness=5)
        self.outer_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self.display_label = tki.Label(self.outer_frame, font=("Courier", 30),
                                       bg=REGULAR_COLOR, width=23, relief="ridge")
        self.display_label.pack(side=tki.TOP, fill=tki.BOTH)
        self.display_score = tki.Label(self.outer_frame, font=("Courier", 30),
                                       bg=REGULAR_COLOR, width=23, relief="ridge")
        self.display_score.pack(side=tki.TOP, fill=tki.BOTH)

        self.display_time = tki.Label(self.outer_frame, font=("Courier", 30),
                                      bg=REGULAR_COLOR, width=10, relief="ridge")
        self.display_time.pack(side=tki.TOP, fill=tki.BOTH)

        self.words_left_frame = tki.Frame(self, bg=REGULAR_COLOR, highlightbackground=REGULAR_COLOR,
                                          highlightthickness=5)
        self.words_left_frame.pack(side=tki.BOTTOM, fill=tki.BOTH, expand=True)
        self.found_words_frame = tki.Frame(self, bg=REGULAR_COLOR, highlightbackground=REGULAR_COLOR,
                                           highlightthickness=5)
        self.found_words_frame.pack(side=tki.RIGHT, fill=tki.BOTH, expand=True)
        self.found_words_label = tki.Label(self.found_words_frame, font=("Courier", 30),
                                           bg=REGULAR_COLOR, width=23, relief="ridge", text="Found words:")
        self.found_words_label.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self.lower_frame = tki.Frame(self.outer_frame)
        self.lower_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self.reset_and_check = tki.Frame(self, bg=REGULAR_COLOR, highlightbackground=REGULAR_COLOR,
                                         highlightthickness=5)
        self.reset_and_check.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

class PlayAgain(tki.Frame):

    def __init__(self,parent, controller):
        tki.Frame.__init__(self,parent)
        self._controller = controller
        self.play_again_frame = tki.Label(self, bg="white", highlightbackground=REGULAR_COLOR, highlightthickness=5,
                                       font=("Courier", 20))
        self.play_again_frame.pack(side=tki.TOP, fill=tki.BOTH, pady=100, padx=10)

