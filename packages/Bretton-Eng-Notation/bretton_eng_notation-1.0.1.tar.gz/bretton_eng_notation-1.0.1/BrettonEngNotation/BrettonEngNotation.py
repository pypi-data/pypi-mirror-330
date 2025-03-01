import numpy as np


def eng_notation(a):
    if a == 0:
        return 0
    number_of_10 = np.floor(np.log10(np.abs(a)))

    suffix_letter = {
        8: "Y",
        7: "Z",
        6: "E",
        5: "P",
        4: "T",
        3: "G",
        2: "M",
        1: "k",
        0: "",
        -1: "m",
        -2: "µ",
        -3: "n",
        -4: "p",
        -5: "f",
        -6: "a",
        -7: "z",
        -8: "y",
    }

    suffix = np.floor(np.log10(np.abs(a)) / 3)
    exponent = int(np.floor(number_of_10 / 3) * 3)
    prefix = a / (10**exponent)

    formatted_prefix = "{:.3f}".format(prefix).rstrip("0").rstrip(".")

    suffix_output = suffix_letter.get(suffix, "Value out of range")

    output = str(formatted_prefix) + str(" ") + str(suffix_output)
    return output
    # print(formatted_prefix, suffix_output)


def eng_notation_help():
    # mackenzie is the best
    print(
        """
    Name        Symbol      Magnitude
    =================================
    Yotta       Y           10^24
    Zetta       Z           10^21
    Exa         E           10^18
    Peta        P           10^15
    Tera        T           10^12
    Giga        G           10^9
    Mega        M           10^6
    Kilo        k           10^3
    Milli       m           10^-3
    Micro       µ           10^-6
    Nano        n           10^-9
    Pico        p           10^-12
    Femto       f           10^-15
    Atto        a           10^-18
    Zepto       z           10^-21
    Yocto       y           10^-24
    """
    )


if __name__ == "__main__":
    # Test with values that cover a range of magnitudes
    eng_notation(0.0001)  # Expected output: 100.0 µ
    eng_notation(0.001)  # Expected output: 1.0 m
    eng_notation(0.01)  # Expected output: 10.0 m
    eng_notation(0.1)  # Expected output: 100.0 m
    eng_notation(0)  # Expected output: 0
    eng_notation(1)  # Expected output: 1.0
    eng_notation(10)  # Expected output: 10.0
    eng_notation(100)  # Expected output: 100.0
    eng_notation(500 / 3.2)  # Test with division to get a non-integer result
    print(
        "P_s =", eng_notation(542387)
    )  # A larger number to test the function with bigger magnitudes
    eng_notation(1e3 * 1e24)  # Test with a very large number

    # Display the engineering notation key
    eng_notation_help()
