CORNER_CHAR_COUNT = 2
PADDING_RIGHT = 3
PADDING_LEFT = 3


def print_border(title: str, *args: str):
    cols = max(len(arg) for arg in args + (title,)) + PADDING_RIGHT
    # borders around song
    print()
    print_title(title, cols)
    print_emptlyline_with_border(cols)
    for arg in args:
        print_word(arg, cols)
    print_emptlyline_with_border(cols)
    print_corners(cols)
    print()
    return cols


def print_title(title: str, cols: int):
    title_length = len(title)
    content = "+" + "-" * (PADDING_LEFT) + title + "-" * (cols - title_length) + "+"
    print(content)
    return len(content)


def print_word(word: str, cols: int):
    word_length = len(word)
    content = f"|{' ' * (PADDING_LEFT) }{word}{' ' * (cols - word_length)}|"
    print(content)
    return len(content)


def print_corners(cols: int):
    content = "+" + "-" * (cols + PADDING_LEFT) + "+"
    print(content)
    return len(content)


def print_emptlyline_with_border(cols: int):
    content = f"|{' ' * (cols + PADDING_LEFT)}|"
    print(content)
    return len(content)
