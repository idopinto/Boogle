def load_words_dict(file_path):
    """This function gets a filepath of file with records and returns it as a list of records."""
    with open(file_path) as data_file:
        word_dict = dict()
        for line in data_file:
            word = line.strip().split()
            word_dict[word[0]] = True
        print(word_dict["AAHED"])
        return word_dict


print(load_words_dict("boggle_dict.txt"))
def is_valid_path(board, path, words):
    pass


def find_length_n_words(n, board, words):
    pass
