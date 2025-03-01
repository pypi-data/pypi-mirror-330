import random


class passGenPy:
    def generatePassword(
        length=8, letters=True, uppercase=True, numbers=True, symbols=True
    ):
        uppercase_letters = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ]
        lowercase_letters = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
        ]
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        symbols = [
            "!",
            "@",
            "#",
            "$",
            "%",
            "^",
            "&",
            "*",
            "(",
            ")",
            "_",
            "+",
            "-",
            "=",
            "[",
            "]",
            "{",
            "}",
            "|",
            ";",
            ":",
            "'",
            '"',
            ",",
            ".",
            "<",
            ">",
            "/",
            "?",
            "\\",
        ]

        letter_list = []

        if letters:
            letter_list.extend(lowercase_letters)
            if uppercase:
                letter_list.extend(uppercase_letters)

        if numbers:
            letter_list.extend(numbers)

        if symbols:
            letter_list.extend(symbols)

        password = ""

        for i in range(length):
            random_letter = random.choice(letter_list)
            password += random_letter

        return password
