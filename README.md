# Homemade BookCorpus

[BookCorpus](http://yknzhu.wixsite.com/mbweb) is a popular text corpus, espetially for unsupervised learning of sentence encoders/decoders. But, usage of BookCorpus is limited.

This is an unofficial repository for collecting data from [smashwords.com](https://www.smashwords.com/books/category/1/downloads/0/free/medium/0), which is an original source.


## How to use

Prepare downloaded URLs.

```
python -u download_list.py > url_list.jsonl &
```

Download their files. Download `txt` if possible. Otherwise, try to extract text from `epub`. `--trash-bad-count` filters out `epub` files whose word count is largely different from its official stat.

```
python download_files.py --list url_list.jsonl --out out_txts --trash-bad-count
```

Make concatenated text with sentence-per-line format.

And, tokenize them into segmented words.

```
python make_sentlines.py out_txts | python tokenize_sentlines.py > all.tokenized.txt
tr A-Z a-z < all.tokenized.txt > all.tokenized.txt.low
```

## Requirement

- python3 is recommended
- beautifulsoup4
- progressbar2
- nltk
  - And, download tokenizers by `python -c "import nltk;nltk.download('punkt')"`


## Acknowledgement

`epub2txt.py` is derived and modified from https://github.com/kevinxiong/epub2txt/blob/master/epub2txt.py


## Citation

```
@InProceedings{Zhu_2015_ICCV,
    title = {Aligning Books and Movies: Towards Story-Like Visual Explanations by Watching Movies and Reading Books},
    author = {Zhu, Yukun and Kiros, Ryan and Zemel, Rich and Salakhutdinov, Ruslan and Urtasun, Raquel and Torralba, Antonio and Fidler, Sanja},
    booktitle = {The IEEE International Conference on Computer Vision (ICCV)},
    month = {December},
    year = {2015}
}
```

```
@inproceedings{moviebook,
    title = {Aligning Books and Movies: Towards Story-like Visual Explanations by Watching Movies and Reading Books},
    author = {Yukun Zhu and Ryan Kiros and Richard Zemel and Ruslan Salakhutdinov and Raquel Urtasun and Antonio Torralba and Sanja Fidler},
    booktitle = {arXiv preprint arXiv:1506.06724},
    year = {2015}
}
```
