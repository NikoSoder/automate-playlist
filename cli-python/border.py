def print_border(name, artists):
    title = "NOW LISTENING"
    merged_artists = ", ".join(artists)
    PADDING_RIGHT = 5
    cols = max(len(name), len(merged_artists), len(title)) + PADDING_RIGHT
    # borders around song
    print()
    print_corners(cols)
    print_emptlyline_with_border(cols)
    print_word(title, cols)
    print_emptlyline_with_border(cols)
    print_word(name, cols)
    print_word(merged_artists, cols)
    print_emptlyline_with_border(cols)
    print_corners(cols)
    print()


def print_word(word, cols):
    word_length = len(word)
    print(f"| {word}{' ' * (cols - word_length - 2)} |")


def print_corners(cols):
    print("+" + "-" * (cols) + "+")


def print_emptlyline_with_border(cols):
    print(f"|{' ' * (cols)}|")
