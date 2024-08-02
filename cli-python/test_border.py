import unittest
from border import (
    print_title,
    print_word,
    print_corners,
    print_emptlyline_with_border,
    print_border,
)


test_data = [
    (
        "Sky",
        "Blue Horizon, Green artist, Extra artist",
        "Optional Data 1",
        "More Data",
    ),
    ("Whispers in the Dark", "Midnight Echo", "Additional Info"),
    ("Eclipse", "Solar Flare"),
    ("Lost in the Stars", "Galactic Journey", "Extra Info"),
    ("Harmony", "Symphonic Waves", "Another Extra", "And Another"),
    ("Dance of the Fireflies", "Nocturnal Symphony", "More Extra Info"),
    ("Breeze", "Coastal Dreams", "Some Extra Data"),
    ("Heartbeat", "Electric Pulse"),
    ("Mystic River", "Whispering Willows", "Optional Extra"),
    ("Echoes of Silence", "Quiet Storm", "More Data Here"),
]


class TestStringMethods(unittest.TestCase):

    def test_print_border(self):
        title = "NOW LISTENING"
        CORNER_CHAR_COUNT = 2
        PADDING_LEFT = 3

        for data in test_data:
            with self.subTest(song=data[0], artist=data[1]):
                cols = print_border(title, *data)
                print_title_len = print_title(title, cols)

                for word in data:
                    print_word_len = print_word(word, cols)
                    self.assertEqual(
                        print_word_len - CORNER_CHAR_COUNT - PADDING_LEFT, cols
                    )

                print_emplyline_len = print_emptlyline_with_border(cols)
                print_corners_len = print_corners(cols)

                self.assertEqual(
                    print_title_len - CORNER_CHAR_COUNT - PADDING_LEFT, cols
                )
                self.assertEqual(
                    print_emplyline_len - CORNER_CHAR_COUNT - PADDING_LEFT, cols
                )
                self.assertEqual(
                    print_corners_len - CORNER_CHAR_COUNT - PADDING_LEFT, cols
                )


if __name__ == "__main__":
    unittest.main()
