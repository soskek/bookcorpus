import sys
from nltk.tokenize import word_tokenize


for l in sys.stdin:
    if l.strip():
        # print(' '.join(word_tokenize(l.strip()) + ["EOS"]))
        print(' '.join(word_tokenize(l.strip())))
    else:
        print('')
