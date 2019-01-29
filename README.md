# Homemade BookCorpus

You can reproduce BookCorpus by yourself.

[BookCorpus](http://yknzhu.wixsite.com/mbweb) is a popular large-scale text corpus, espetially for unsupervised learning of sentence encoders/decoders. However, BookCorpus is no longer distributed...

This repository includes a crawler collecting data from [smashwords.com](https://www.smashwords.com/books/category/1/downloads/0/free/medium/0), which is the original source of BookCorpus.
Collected sentences may partially differ but the number of them will be larger or almost the same.


## How to use

Prepare URLs of available books. However, this repository already has a list as `url_list.jsonl` which was a snapshot I (@soskek) collected on Jan 19-20, 2019. You can use it if you'd like.

```
python -u download_list.py > url_list.jsonl &
```

Download their files. Downloading is performed for `txt` files if possible. Otherwise, this tries to extract text from `epub`. The additional argument `--trash-bad-count` filters out `epub` files whose word count is largely different from its official stat (because it may imply some failure).

```
python download_files.py --list url_list.jsonl --out out_txts --trash-bad-count
```

Make concatenated text with sentence-per-line format.

```
python make_sentlines.py out_txts > all.txt
```

If you want to tokenize them into segmented words by nltk, run the below. You can use another choices for this by yourself.

```
python make_sentlines.py out_txts | python tokenize_sentlines.py > all.tokenized.txt
```

## Requirement

- python3 is recommended
- beautifulsoup4
- progressbar2
- nltk
  - And, download tokenizers by `python -c "import nltk;nltk.download('punkt')"`
- html2text

To install the requirements, run the following with pip on python3:
```
pip install -r requirements.txt
python -c "import nltk;nltk.download('punkt')"
```


## Note

- It is expected some error messages like `Failed: epub and txt` are sometimes displayed. This code does not adapt to some of books in the smashwords.com (e.g. `You set the price!` books).

## Acknowledgement

`epub2txt.py` is derived and modified from https://github.com/kevinxiong/epub2txt/blob/master/epub2txt.py


## Citation

Yukun Zhu, Ryan Kiros, Richard Zemel, Ruslan Salakhutdinov, Raquel Urtasun, Antonio Torralba, Sanja Fidler. **"[Aligning Books and Movies: Towards Story-like Visual Explanations by Watching Movies and Reading Books.](https://arxiv.org/abs/1506.06724)"** arXiv preprint arXiv:1506.06724, [ICCV 2015](https://www.cv-foundation.org/openaccess/content_iccv_2015/papers/Zhu_Aligning_Books_and_ICCV_2015_paper.pdf).

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

Ryan Kiros, Yukun Zhu, Ruslan Salakhutdinov, Richard S. Zemel, Antonio Torralba, Raquel Urtasun, and Sanja Fidler. **"[Skip-Thought Vectors.](https://arxiv.org/abs/1506.06726)"** arXiv preprint arXiv:1506.06726, [NIPS 2015](https://papers.nips.cc/paper/5950-skip-thought-vectors.pdf).

```
@article{kiros2015skip,
    title={Skip-Thought Vectors},
    author={Kiros, Ryan and Zhu, Yukun and Salakhutdinov, Ruslan and Zemel, Richard S and Torralba, Antonio and Urtasun, Raquel and Fidler, Sanja},
    journal={arXiv preprint arXiv:1506.06726},
    year={2015}
}
```
