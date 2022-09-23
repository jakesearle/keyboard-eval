### Random thoughts:
## Automated improvement 
# Swapping values (more "expensive" to swap from qwerty across hands than it is to swap between a finger)
# Same finger penalty
# Hand balance metric
# "Locked" keys (unswappable)
# Pre-compute letter-frequencies and bigrams
# [X] Slightly different values for different fingers (middle, pointer, then ring, then pinky)

import json
from keymap import Keymap
from document import Document
from urllib.request import urlopen
from bs4 import BeautifulSoup


# This whole thing is super subjective. But I have some notes on it:
# - The keyboard I used while evaulting this was the Reviung41
# - Started by assigning the homerow keys their values
# - Filled in each finger's "up" and "down" positions by just doing simple x1, x2,..., multipliers.
#   I used x1.5 on QWERTY's "C" spot because it was somewhere between a 2.0 and 3.0 key
# - For the key in QWERTY's "T" spot, I took the average of the "R" and "G" spots and rounded down
position_scores = [
    [3.0, 2.4, 2.0, 3.3, 3.5,    3.5, 3.3, 2.0, 2.4, 3.0],
    [1.5, 1.2, 1.0, 1.1, 4.4,    4.4, 1.1, 1.0, 1.2, 1.5],
    [4.5, 4.8, 2.5, 2.2, 5.5,    5.5, 2.2, 2.5, 4.8, 4.5]
]


def main():
    build_key_scores()
    layouts = None
    with open('layouts.json', 'r') as infile:
        dictionary = json.load(infile)
        layouts = [Keymap(name, data) for name, data in dictionary.items()]

    # doc = Document("./texts/the-picture-of-dorian-gray.txt")
    doc = Document("./texts/1000-most-common.txt")
    scores = []
    for layout in layouts:
        score = layout.eval_against_char_frequencies(doc.char_frequencies)
        scores.append((layout.name, score / doc.total_chars))
    print('\n'.join([f"{s[0]}: {s[1]:.2f}" for s in sorted(scores, key=lambda x: x[1], reverse=True)]))

# Typing sucks
def build_key_scores():
    keyboard_data = None
    with open('layouts.json', 'r') as infile:
        keyboard_data = json.load(infile)

    for name, layout in keyboard_data.items():
        scores = {}
        for key_row, score_row in zip(layout['keys'], position_scores):
            for key, score in zip(key_row, score_row):
                scores[key] = score
        layout['scores'] = scores
    with open('layouts.json', 'w') as outfile:
        outfile.write(json.dumps(keyboard_data, indent=4))


def scrape_finnish_words():
    html = urlopen(
        'https://1000mostcommonwords.com/1000-most-common-finnish-words/')
    soup = BeautifulSoup(html.read(), features="html.parser")
    soup.prettify()
    tds = soup.select("table tr td:nth-of-type(2)")
    for td in tds:
        print(td.get_text())
    with open('./texts/fi/1000-most-common.txt', 'w+') as outfile:
        outfile.write('\n'.join([td.get_text() for td in tds[1:]]))


if __name__ == '__main__':
    main()
