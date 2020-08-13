'''
7-segment LED display utilities
'''

char_to_bin_map = {
    '0': 0b0111111,
    '1': 0b0000110,
    '2': 0b1011011,
    '3': 0b1001111,
    '4': 0b1100110,
    '5': 0b1101101,
    '6': 0b1111101,
    #'6': 0b1111100,  # Alternative, without tail
    '7': 0b0000111,
    #'7': 0b0100111,  # Alternative, with tail
    '8': 0b1111111,
    '9': 0b1101111,
    #'9': 0b1100111,  # Alternative, without tail
    ' ': 0b0000000,
    '_': 0b0001000,
    '=': 0b1001000,
    '-': 0b1000000,
    '¯': 0b0000001,
    '"': 0b0100010,
    "'": 0b0100000,  # Ambiguous with "`"
    '`': 0b0000010,  # Ambiguous with "'"
    '‘': 0b1100000,  # Open single quote
    '’': 0b0000011,  # Close single quote
    '^': 0b0100011,  # This is a bit weird
    '°': 0b1100011,
    '[': 0b0111001,  # Ambiguous with 'C'
    ']': 0b0001111,
    '(': 0b0111001,  # Ambiguous with '['
    ')': 0b0001111,  # Ambiguous with ']'
    '/': 0b1010010,  # This is a bit weird
    '\\': 0b1100100,  # This is a bit weird
    '?': 0b1010011,  # This is a bit weird
    '@': 0b0111011,
    #'@': 0b0011111,  # Alternative
    'A': 0b1110111,
    'a': 0b1011111,
    'b': 0b1111100,
    'C': 0b0111001,
    'c': 0b1011000,
    'd': 0b1011110,
    'E': 0b1111001,
    'e': 0b1111011,
    'F': 0b1110001,
    'G': 0b0111101,
    'H': 0b1110110,
    'h': 0b1110100,
    'I': 0b0110000,
    'i': 0b0010000,
    'J': 0b0011110,
    'K': 0b1110101,  # This is a weird char
    'L': 0b0111000,
    'M': 0b0010101,  # This is a weird char
    'n': 0b1010100,
    'o': 0b1011100,
    'O': 0b0111111,  # Ambiguous with '0'
    'P': 0b1110011,
    'q': 0b1100111,
    'r': 0b1010000,
    'S': 0b1101101,  # Ambiguous with '5'
    #'S': 0b1101100,  # Alternative (and weird)
    't': 0b1111000,
    'u': 0b0011100,
    'V': 0b0111110,  # This looks like 'U'
    'W': 0b0011101,  # This is a weird char
    'x': 0b0010100,  # This is a weird char
    'y': 0b1101110,
    'Z': 0b1011011,  # Ambiguous with '2'
    #'Z': 0b0011011,  # Alternative (and weird)
}

def char_to_bin(char):
    tries = [char, char.upper(), char.lower(), ' ']
    for guess in tries:
        byte = char_to_bin_map.get(guess, None)
        if byte is not None:
            return byte
    return 0  # It should never get to this line.
