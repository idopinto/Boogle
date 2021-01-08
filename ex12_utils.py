def load_words_dict(file_path):
    """This function gets a filepath of file with records and returns it as a list of records."""
    with open(file_path) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


def is_valid_path(board, path, words):
    pass


def find_length_n_words(n, board, words):
    pass
