def print_border(title: str, *args: str):
    PADDING_RIGHT = 5
    cols = max(len(arg) for arg in args + (title,)) + PADDING_RIGHT
    # borders around song
    print()
    print_title_middle(title, cols)
    print_emptlyline_with_border(cols)
    for arg in args:
        print_word(arg, cols)
    print_emptlyline_with_border(cols)
    print_corners(cols)
    print()


def print_title_middle(title: str, cols: int):
    # NOTE: a lot of magic numbers...
    title_length = len(title)
    padding = round((cols - title_length) / 2) + 1
    extra_padding = (cols - title_length) % 2
    print("+" + "-" * (padding) + title + "-" * (padding + extra_padding) + "+")


def print_word(word: str, cols: int):
    word_length = len(word)
    print(f"| {word}{' ' * (cols - word_length)} |")


def print_corners(cols: int):
    print("+" + "-" * (cols) + "-" + "-" + "+")


def print_emptlyline_with_border(cols: int):
    print(f"| {' ' * (cols)} |")
