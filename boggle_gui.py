import tkinter as tki
# import boggle_model,boggle_controller
import boggle_board_randomizer
import datetime
LETTER_HOVER_COlOR = "red"  # choose colors
REGULAR_COLOR = "lightgray"
LETTER_ACTIVE_COlOR = "slateblue"
LETTER_STYLE = {"font": ("Courier", 30), "borderwidth": 1, "relief": tki.RAISED, "bg": REGULAR_COLOR,
                "activebackground": LETTER_ACTIVE_COlOR}
FILE_NAME = 'boggle_dict.txt'


class BoggleBoard:

    def __init__(self):
        root = tki.Tk()
        root.title("BoggleGame")
        root.resizable(False, False)
        self._main_window = root

        self._outer_frame = tki.Frame(root, bg=REGULAR_COLOR, highlightbackground=REGULAR_COLOR, highlightthickness=5)
        self._outer_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self._display_label = tki.Label(self._outer_frame, font=("Courier", 30),
                                        bg=REGULAR_COLOR, width=23, relief="ridge")
        self._display_label.pack(side=tki.TOP, fill=tki.BOTH)

        self._display_time = tki.Label(self._outer_frame,font=("Courier", 30),
                                        bg=REGULAR_COLOR, width=10, relief="ridge")
        self._seconds_left = 180
        self._display_time.pack(side=tki.TOP, fill=tki.BOTH)
        self._lower_frame = tki.Frame(self._outer_frame)
        self._lower_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)
        self._board_letters = boggle_board_randomizer.randomize_board()
        self._letters = {}
        self._path = []

    def run(self):
        self._main_window.mainloop()

    def set_display(self):
        self._display_label["text"] = self._path

    def get_path(self):
        return self._path

    def create_board(self):
        for i in range(4):
            tki.Grid.columnconfigure(self._lower_frame, i, weight=1)

        for i in range(4):
            tki.Grid.rowconfigure(self._lower_frame, i, weight=1)

        for row in range(4):
            for col in range(4):
                self.make_letter(self._board_letters[row][col], row, col)

    def callback(self):
        self._path.append((0,0))
        self.set_display()

    def make_letter(self, letter_char, row, col, rowspan=1, columnspan=1):
        letter = tki.Button(self._lower_frame, text=letter_char, **LETTER_STYLE, command= self.callback)
        letter.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=tki.NSEW)
        self._letters[letter_char] = (row,col)

        def _on_enter(event):
            letter['background'] = LETTER_HOVER_COlOR
            #self.callback()

        def _on_leave(event):
            letter['background'] = REGULAR_COLOR

        letter.bind("<Enter>", _on_enter)
        letter.bind("<Leave>", _on_leave)

        return letter

    def timer_countdown(self):
        """update label based on the time left"""
        self._display_time['text'] = self.convert_seconds_left_to_time()
        if self._seconds_left:
            self._seconds_left -= 1
            self._display_time.after(1000,self.timer_countdown)
        else:
            return "Gameover"

    def convert_seconds_left_to_time(self):
        return datetime.timedelta(seconds=self._seconds_left)




class Timer:
    pass


x = BoggleBoard()
x.set_display()
x.create_board()
x.timer_countdown()
x.run()
