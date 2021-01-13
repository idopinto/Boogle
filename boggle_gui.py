import tkinter as tki
from tkmacosx import Button
# import boggle_model,boggle_controller
import boggle_board_randomizer
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
        self._current_widget = None

        self._frames = {}
        for F in (Startscreen, Board):
            screen_name = F.__name__
            frame = F(container, self)
            self._frames[screen_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Startscreen")
        self._board_letters = boggle_board_randomizer.randomize_board()
        self._letters = {}
        self._letters_displsy = ""
        self._path = []
        self.words_left = {3: 100, 4: 70, 5: 80, 6: 50, 7: 3}
        self.seconds_left = 180
        self.score = 0
        self.found_words = []
        self._letters_2 = {}

    def set_words_left(self, dict):
        self.words_left = dict

    def set_found_words(self, found_words_list):
        self.found_words = found_words_list

    def set_score(self, score):
        self.score += score

    def set_display(self):
        self._frames["Board"].display_label["text"] = self._letters_displsy
        for coord in self._path:
            self._letters_2[coord]['bg'] = "slateblue"
        self._frames["Board"].display_score["text"] = "Score:" + str(self.score)
        if not self._path:
            for letter in self._letters_2:
                self._letters_2[letter]['bg'] = REGULAR_COLOR

    def get_path(self):
        return self._path

    def reset_path(self):
        self._path = []

    def create_found_words(self):
        for word in self.found_words:
            label = tki.Label(self._frames["Board"].found_words_frame, font=("Courier", 15),
                              bg=REGULAR_COLOR, width=15, text=word)
            label.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

    def create_words_left(self):
        for i in range(0, 5):
            x = self.make_Frames_for_left_words("i+3", "50", 0, i)
            words_left_label = tki.Label(x, font=("Courier", 30),
                                         bg=REGULAR_COLOR, text=str(i + 3) + ":")
            words_left_label.pack(side=tki.LEFT, fill=tki.BOTH)
            words_left_label__ = tki.Label(x, font=("Courier", 30),
                                           bg=REGULAR_COLOR, width=5, relief="ridge", text=str(self.words_left[i + 3]))
            words_left_label__.pack(side=tki.LEFT, fill=tki.BOTH)

    def make_Frames_for_left_words(self, length, words_left, row, col, rowspan=1, columnspan=1):
        words_left_frame = tki.Frame(self._frames["Board"].words_left_frame, bg=REGULAR_COLOR,
                                     highlightbackground=REGULAR_COLOR,
                                     highlightthickness=5)
        words_left_frame.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=tki.NSEW)

    def create_board(self):
        for i in range(4):
            tki.Grid.columnconfigure(self._frames["Board"].lower_frame, i, weight=1)

        for i in range(4):
            tki.Grid.rowconfigure(self._frames["Board"].lower_frame, i, weight=1)

        for row in range(4):
            for col in range(4):
                self.make_letter(self._board_letters[row][col], row, col)

    def callback(self, row, col):
        self._path = []
        self._letters_displsy = ""
        self.set_display()
        self._path.append((row, col))
        self._letters_displsy += self._letters[(row, col)]
        self.set_display()

    def make_letter(self, letter_char, row, col, rowspan=1, columnspan=1):
        letter = Button(self._frames["Board"].lower_frame, text=letter_char, **LETTER_STYLE,
                        command=lambda: self.callback(row, col))
        self._letters_2[(row, col)] = letter
        letter.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=tki.NSEW)
        self._letters[(row, col)] = letter_char

        self.current_widget = None

        def start_path(event):
            widget = event.widget.winfo_containing(event.x_root, event.y_root)
            if self.current_widget != widget:
                if self.current_widget:
                    self.current_widget.event_generate("<<B1-ButtonRelease>>")
                self.current_widget = widget
                self.current_widget.event_generate("<<B1-Enter>>")

        def on_enter(event):
            self._path.append((row, col))
            # letter['bg'] = "slateblue"
            self._letters_displsy += self._letters[(row, col)]

            self.set_display()

        def on_leave(event):
            letter['bg'] = REGULAR_COLOR
            # self._letters_displsy = self._letters_displsy[:-1]
            # self.set_display()

        def on_release(event):
            self._path = []
            self.set_display()

        self._frames["Board"].lower_frame.bind_all("<B1-Motion>", start_path)
        letter.bind("<<B1-Enter>>", on_enter)
        # letter.bind("<<B1-Leave>>", on_leave)
        # letter.bind("<<B1-ButtonRelease>>", on_release)

        return letter

    def timer_countdown(self):
        """update label based on the time left"""
        self._frames["Board"].display_time['text'] = self.convert_seconds_left_to_time()
        if self.seconds_left:
            self.seconds_left -= 1
            self._frames["Board"].display_time.after(1000, self.timer_countdown)
        if self.seconds_left == 0:
            self.show_frame("Startscreen")

    def convert_seconds_left_to_time(self):
        return datetime.timedelta(seconds=self.seconds_left)

    def show_frame(self, container):
        frame = self._frames[container]
        frame.tkraise()
        if container == "Board":
            self.run()

    def run(self):
        self.create_board()
        self.set_display()
        self.timer_countdown()
        self.create_words_left()
        self.create_found_words()


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


class Drag_and_Drop:
    def add_dragable(self, widget):
        widget.bind("<ButtonPress-1>", self.on_start)
        widget.bind("<B1-Motion>", self.on_drag)
        widget.bind("<ButtonRelease-1>", self.on_drop)
        widget.configure(cursur="hand1")

    def on_start(self, event):
        pass

    def on_drag(self, event):
        pass

    def on_drop(self, event):
        x, y = event.widget.winfo_pointerxy()
        target = event.widget.winfo_pointerxy(x, y)
        try:
            target.configure()
        except:
            pass


class Timer:
    pass


x = BoggleGame()
x.mainloop()
