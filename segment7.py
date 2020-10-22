'''
7-segment LED display utilities

For some inspiration, see also:
* http://en.fakoo.de/siekoo.html
* https://en.wikichip.org/wiki/seven-segment_display/representing_letters
* https://en.wikipedia.org/wiki/Seven-segment_display
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
    '🯰': 0b0111111,
    '🯱': 0b0000110,
    '🯲': 0b1011011,
    '🯳': 0b1001111,
    '🯴': 0b1100110,
    '🯵': 0b1101101,
    '🯶': 0b1111101,
    '🯷': 0b0100111,
    '🯸': 0b1111111,
    '🯹': 0b1101111,
    ' ': 0b0000000,
    '_': 0b0001000,
    '=': 0b1001000,
    '⁐': 0b0001001,  # I'd want a better character here, a mix of underline and overline.
    'ニ': 0b0001001,  # I'd want a better character here, a mix of underline and overline.
    '≡': 0b1001001,
    '-': 0b1000000,
    '¯': 0b0000001,
    '‾': 0b0000001,
    ':': 0b1000001,
    ';': 0b1000101,
    ',': 0b1000100,
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
    '|': 0b0110000,  # Ambiguous with "I"
    '‖': 0b0110110,
    '⊦': 0b1110000,
    '⊢': 0b1110000,
    '⊣': 0b1000110,
    '⌈': 0b0110001,
    '⌉': 0b0000111,
    '⌊': 0b0111000,
    '⌋': 0b0001110,
    '⎾': 0b0110001,
    '⏋': 0b0000111,
    '⎿': 0b0111000,
    '⏌': 0b0001110,
    '⌜': 0b0100001,
    '⌝': 0b0000011,
    '⌞': 0b0011000,
    '⌟': 0b0001100,
    '⌌': 0b1010000,
    '⌍': 0b1000100,
    '⌎': 0b1100000,
    '⌏': 0b1000010,
    '⎡': 0b0110001,
    '⎢': 0b0110000,
    '⎣': 0b0111000,
    '⎤': 0b0000111,
    '⎥': 0b0000110,
    '⎦': 0b0001110,
    '⊏': 0b1100001,
    '⊑': 0b1101001,
    '⊐': 0b1000011,
    '⊒': 0b1001011,
    '⊓': 0b0100011,
    '⊔': 0b1100010,
    '⋂': 0b0110111,
    '⋃': 0b0111110,  # This looks like 'U' and 'V'
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
    'I': 0b0110000,  # Ambiguous with "|"
    'i': 0b0010000,  # Dotless
    #'i': 0b0010001,  # Dotted
    'J': 0b0011110,
    'K': 0b1110101,  # This is a weird char
    'L': 0b0111000,
    'M': 0b0010101,  # This is a weird char
    #'M': 0b1010101,  # This is a weird char
    'n': 0b1010100,
    'o': 0b1011100,
    'O': 0b0111111,  # Ambiguous with '0'
    'P': 0b1110011,
    'q': 0b1100111,
    'r': 0b1010000,
    #'S': 0b1101101,  # Ambiguous with '5'
    'S': 0b0101101,  # Alternative (and weird)
    #'S': 0b1101100,  # Alternative (and weird)
    't': 0b1111000,
    'u': 0b0011100,
    'U': 0b0111110,
    #'V': 0b0111110,  # This looks like 'U'
    'V': 0b0101010,  # This is a weird char
    'W': 0b0011101,  # This is a weird char
    #'W': 0b1101010,  # This is a weird char
    'x': 0b1001001,  # This is a weird char, looks like Greek Xi
    #'x': 0b0010100,  # This is a weird char
    'y': 0b1101110,
    #'Z': 0b1011011,  # Ambiguous with '2'
    'Z': 0b0011011,  # Alternative (and weird)
}

def char_to_bin(char):
    tries = [char, char.upper(), char.lower(), ' ']
    for guess in tries:
        byte = char_to_bin_map.get(guess, None)
        if byte is not None:
            return byte
    return 0  # It should never get to this line.
