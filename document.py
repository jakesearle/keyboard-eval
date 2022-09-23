import collections

# This is for werid characters
aliases = {
    '\u201c': '"',  # Left double quotation mark
    '\u201d': '"',  # Right double quotation mark
    '\u2018': '\'', # Left single quotation mark
    '\u2019': '\'', # Right single quotation mark
    '\ufeff': ' ',  # Zero-width no-break space
    '\u2014': '--', # Em dash
}

class Document:

    def __init__(self, filename):
        self.filename = filename

        self.text = self.compute_sanitized_text()

        self.char_frequencies = self.compute_char_frequencies()
        if any([not k.isascii() for k in self.char_frequencies.keys()]):
            print("Error! Unknown Unicode in text! Please fix!")
            self.print_dict_non_ascii(self.char_frequencies)
        self.bigrams = self.compute_bigrams()
        self.total_chars = sum(self.char_frequencies.values())

    # Set all characters to lowercase, change out weird characters for aliases (e.g. fancy unicode double-quotes)
    def compute_sanitized_text(self):
        text = None
        with open(self.filename, 'r') as infile:
            text = infile.read()
        
        return ''.join([self.get_sanitized_char(char) for char in text])
        
    def get_sanitized_char(self, c):
        c = c.lower()
        if 'a' <= c <= 'z':
            return c
        if c in aliases:
            return aliases[c]
        if c.isspace():
            return ' '
        return c

    def compute_char_frequencies(self):
        return {char: v for char, v in collections.Counter(self.text).items() if not char.isspace()}
    
    def compute_bigrams(self):
        all_bigrams = []
        for word in self.text.split():
            word_bigrams = [(char1, char2) for char1, char2 in zip(word[:-1], word[1:])]
            all_bigrams.extend(word_bigrams)
        return collections.Counter(all_bigrams)
    
    def print_dict_non_ascii(self, d):
        non_ascii = {k: v for k, v in d.items() if not k.isascii()}
        sorted_frequencies = sorted(non_ascii.items(), key=lambda x: x[1], reverse=True)
        print('\n'.join([f"{k} ({k.encode('unicode_escape')}): {v}" for k, v in sorted_frequencies]))