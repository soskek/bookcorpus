import sys
from blingfire import text_to_words


for l in sys.stdin:
    if l.strip():
        print(text_to_words(l.strip()))
    else:
        print('')
