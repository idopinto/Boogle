import tkinter as tki
import pygame
import datetime


LETTER_HOVER_COlOR = "gray"  # choose colors
REGULAR_COLOR = "white"
LETTER_ACTIVE_COlOR = "slateblue"
LETTER_STYLE = {"font": ("Courier", 30), "borderwidth": 1, "relief": tki.RAISED, "bg": REGULAR_COLOR,
                "activebackground": LETTER_ACTIVE_COlOR}
FILE_NAME = 'boggle_dict.txt'
BOARD_SIZE = 4



class BoggleGame(tki.Tk):
    """This Class is a Tk object which represents the game. this class is build to hold the gui functions
    and methods to create the graphics and update it. The game is build in a form of 3 layers of 3 big frame objects
    which it gets as args. The boggle game objects contains them all.
    the first layer is the start screen object, the second is the board object and the last is the play again object."""
    def __init__(self, *args, **kwargs):
        tki.Tk.__init__(self, *args, **kwargs)
        self.title("BoggleGame")
        container = tki.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Startscreen, Board, PlayAgain): # creating layers with all frames
            screen_name = F.__name__
            frame = F(container, self)
            self.frames[screen_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Startscreen")
        self.current_coord = ()
        self._board_letters = []
        self._letters_chars = {}
        self.letters_display = ""
        self._path = []
        self.words_left = {}
        self.words_left_frames = []
        self.words_left_labels = {}
        self.seconds_left = 180
        self.score = 0
        self.found_words = []
        self.found_words_counter = 0
        self._letters_buttons = {}
        self.words_left_labels = {}
        self.game_played_counter = 0
        self.found_words_labels = []
    def show_frame(self, container):
        """This method is one of the most imporant methods of the game, for it is controling the frame to 
        present the player at each time. The method gets the frame to show.
        when the board layer is called, that is when the game begins. """
        frame = self.frames[container]
        frame.tkraise()
        if container == "Board":
            pygame.mixer.init()
            pirates = pygame.mixer.Sound("Sounds/pirates_of_the_caribbean.mp3")
            pirates.set_volume(0.1)
            pygame.mixer.find_channel(True).play(pirates)
            frame.tkraise()
            self.timer_countdown()
            if self.game_played_counter == 0:
                self.game_played_counter += 1
            else:
                self.destroy_words_labels()    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # ~~~~~~SETTERS/GETTERS_METHODS~~~~~~~~~~~~~~~#
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
    def set_board(self, board):
        """this function sets the board"""
        self._board_letters = board

    def set_words_left(self, dict):
        """this sets the words left"""
        self.words_left = dict

    def set_found_words(self, found_words_list):
        """this function set the words that were already found"""
        self.found_words = found_words_list

    def set_score(self, score):
        """this function set the score"""
        self.score = score

    def set_display(self):
        """the function set the GUI main display"""
        self.frames["Board"].display_label["text"] = self.letters_display
        for coord in self._path:
            self._letters_buttons[coord]['bg'] = "slateblue"
        self.frames["Board"].display_score["text"] = "Score:" + str(self.score)
        if not self._path:
            for letter in self._letters_buttons:
                self._letters_buttons[letter]['bg'] = REGULAR_COLOR

    def get_path(self):
        """this function return the current path"""
        return self._path

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # ~~~~~~~~~~~~~~~~RESET_METHODS~~~~~~~~~~~~~~~#
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    def create_found_words(self):
        """this method creates the labels of the found words for GUI"""
        for word in self.found_words[self.found_words_counter - 1:]:
            label = tki.Label(self.frames["Board"].found_words_frame, font=("Courier", 15),
                              bg=REGULAR_COLOR, width=15, text=word)
            self.found_words_labels.append(label)
            label.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

    def create_words_left(self):
        """this method creates the words left labels for GUI"""
        for i, key in enumerate(self.words_left):
            x = self.make_Frames_for_left_words(0, i)
            self.words_left_frames.append(x)
            words_left_label = tki.Label(x, font=("Courier", 30),
                                         bg=REGULAR_COLOR, text=str(key) + ":")
            words_left_label.pack(side=tki.LEFT, fill=tki.BOTH)
            words_left_label__ = tki.Label(x, font=("Courier", 30),
                                           bg=REGULAR_COLOR, width=5, relief="ridge", text=str(self.words_left[key]))
            self.words_left_labels[i] = (words_left_label__, key)
            words_left_label__.pack(side=tki.LEFT, fill=tki.BOTH)

    def make_Frames_for_left_words(self, row, col, rowspan=1, columnspan=1):
        """this method makes frames for left words labels"""
        words_left_frame = tki.Frame(self.frames["Board"].words_left_frame, bg=REGULAR_COLOR,
                                     highlightbackground=REGULAR_COLOR,
                                     highlightthickness=5)
        words_left_frame.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=tki.NSEW)
        return words_left_frame

    def create_board(self):
        """this function creates the board of the game. when called, also creates the letters
        buttons by calling the make letter function."""
        for i in range(BOARD_SIZE):
            tki.Grid.columnconfigure(self.frames["Board"].lower_frame, i, weight=1)

        for i in range(BOARD_SIZE):
            tki.Grid.rowconfigure(self.frames["Board"].lower_frame, i, weight=1)

        # create the buttons
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.make_letter(self._board_letters[row][col], row, col)

    def callback(self, row, col):
        """this method is the command of every button letter on the board. it gets the corrdinations of the 
        button and checks if the coords alredy in the path. if not, the method adds the coords to the path and also
        adds the display the letter on the button."""
        self.current_coord = (row, col)
        if self.current_coord in self._path:
            pass
        else:
            self._path.append((row, col))
            self.letters_display += self._letters_chars[(row, col)]
            self.set_display()

    def make_letter(self, letter_char, row, col, rowspan=1, columnspan=1):
      """This function creates the button of the letter on the borad. the fucntion gets the letter(string) and the 
      coords in the board to sets the button with the letter to."""
      letter = tki.Button(self.frames["Board"].lower_frame, text=letter_char, **LETTER_STYLE, command=lambda: self.callback(row, col))
      self._letters_buttons[(row, col)] = letter
      letter.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=tki.NSEW) # creates the grid of the buttons
      self._letters_chars[(row, col)] = letter_char

      return letter


    def update_words_left(self):
        """this method updates the words left labels"""
        for value in self.words_left_labels.values():
            value[0]['text'] = self.words_left[value[1]]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # ~~~~~~~~~~~~~~~~TIMER~~~~~~~~~~~~~~~~~~~~~~~#
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    def timer_countdown(self):
        """update label based on the time left"""
        self.frames["Board"].display_time['text'] = self.convert_seconds_left_to_time()
        if self.seconds_left:
            self.seconds_left -= 1
            self.frames["Board"].display_time.after(1000, self.timer_countdown)
        if self.seconds_left == 0:
            self.destroy_words_left()
            self.frames["PlayAgain"].play_again_frame['text'] = f'Time is up! you ended up with {self.score} points'
            self.frames["PlayAgain"].tkraise()

    def convert_seconds_left_to_time(self):
        """this function convert seconds left to minutes"""
        return datetime.timedelta(seconds=self.seconds_left)


    def destroy_words_left(self):
       """This method destroys the words left frames when the time is up
         and a new game is called."""
       for label in self.words_left_labels.values():
           label[0].destroy()
       for frame in self.words_left_frames:
           frame.destroy()
       self.words_left_labels = {}

    def destroy_words_labels(self):
        """This method destroys the words left labels when the time is up
         and a new game is called."""
        for label in self.found_words_labels:
            label.destroy()
        self.found_words_counter = 0

    def run(self):
      """This method runs the game. when called the mainloop method is called."""
      self.mainloop()


class Startscreen(tki.Frame):
     """This class is a frame object. This frame is the start screen frame.
        The start screen frame is the upper frame and will raise when the game is launched.
        The constructor of the frame gets the controller (the game object) and
         also holds the start button which starts the game by calling the show frame method of the game. """
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
    """This class is a frame object. This frame is the main frame which represents the game board, score etc.
        The board frame is the middle frame and will raise when the game is launched and the start button was pressed.
        The constructor of the board object sets the frames and labels of in the frame like the board,score, found_words etc.
        Because this frame is the main frame of the game, it does not holds any buttons and mainly controlled from the 
        outside because of the many changes while playing the game. """
    
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
    """This class is a frame object. This frame is the play again frame.
        The play again frame is the lowest frame and will raise only when the game ends."""
    
    def __init__(self, parent, controller):
        tki.Frame.__init__(self, parent)
        self._controller = controller
        self.play_again_frame = tki.Label(self, bg="white", highlightbackground=REGULAR_COLOR, highlightthickness=5,
                                          font=("Courier", 20))
        self.play_again_frame.pack(side=tki.TOP, fill=tki.BOTH, pady=100, padx=10)
