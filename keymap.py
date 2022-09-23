class Keymap:


    def __init__(self, name, data):
        self.name = name
        for k, v in data.items():
            setattr(self, k, v)

    def eval_against_char_frequencies(self, char_frequencies):
        total = 0.0
        for char, val in char_frequencies.items():
            total += self.eval_single_char(char) * val
        return total
    
    def eval_single_char(self, char):
        if char in self.scores.keys():
            return self.scores[char]
        return 7.0
