# Homemade BookCorpus

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

**Clawling could be difficult due to some issues of the website. Also, please consider another option such as using publicly available files at your own risk.**

For example,
- [a file by Shawn Presser](https://twitter.com/theshawwn/status/1301852133319294976): It was crawled in September 2020, and each book was separately stored as a text file. Looks nice! Thank you [@shawwn](https://github.com/shawwn)!
- [a file by Igor Brigadir](https://twitter.com/IgorBrigadir/status/1095075607178870786): While it could be similar to the original BookCorpus, all books seemed concatenated. And, I don't know the detail. Please see [some discussion](https://github.com/soskek/bookcorpus/issues/24#issuecomment-556024973) about the dataset or ask the distributer.
- [a dataset class by huggingface/datasets](https://huggingface.co/datasets/bookcorpus): This internally accesses the file above (by Igor) but easy to use in some cases.

And, [a paper by Jack Bandy and Nicholas Vincent](https://openreview.net/forum?id=Qd_eU1wvJeu) is also valuable for understanding how "BookCorpus" and its replicates include several deficiencies.


@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

-----------------

These are scripts to reproduce BookCorpus by yourself.

[BookCorpus](http://yknzhu.wixsite.com/mbweb) is a popular large-scale text corpus, espetially for unsupervised learning of sentence encoders/decoders. However, BookCorpus is no longer distributed...

This repository includes a crawler collecting data from [smashwords.com](https://www.smashwords.com/books/category/1/downloads/0/free/medium/0), which is the original source of BookCorpus.
Collected sentences may partially **differ** but the number of them will be larger or almost the same. If you use the new corpus in your work, please specify that it is a replica.

## How to use

Prepare URLs of available books. However, this repository already has a list as `url_list.jsonl` which was a snapshot I (@soskek) collected on Jan 19-20, 2019. You can use it if you'd like.

```
python -u download_list.py > url_list.jsonl &
```

Download their files. Downloading is performed for `txt` files if possible. Otherwise, this tries to extract text from `epub`. The additional argument `--trash-bad-count` filters out `epub` files whose word count is largely different from its official stat (because it may imply some failure).

```
python download_files.py --list url_list.jsonl --out out_txts --trash-bad-count
```

The results are saved into the directory of `--out` (here, `out_txts`).


### Postprocessing

Make concatenated text with sentence-per-line format.

```
python make_sentlines.py out_txts > all.txt
```

If you want to tokenize them into segmented words by Microsoft's [BlingFire](https://github.com/Microsoft/BlingFire), run the below. You can use another choices for this by yourself.

```
python make_sentlines.py out_txts | python tokenize_sentlines.py > all.tokenized.txt
```

## Disclaimer

For example, you can refer to terms of [smashwords.com](https://www.smashwords.com/about/tos).
Please use the code responsibly and adhere to respective copyright and related laws. I am not responsible for any plagiarism or legal implication that rises as a result of this repository.

## Requirement

- python3 is recommended
- beautifulsoup4
- progressbar2
- blingfire
- html2text
- lxml

```
pip install -r requirements.txt
```


## Note on Errors

- It is expected some error messages are shown, e.g., `Failed: epub and txt`, `File is not a zip file` or `Failed to open`. But, the number of failures will be much less than one of successes. Don't worry.

## Acknowledgement

`epub2txt.py` is derived and modified from https://github.com/kevinxiong/epub2txt/blob/master/epub2txt.py


## Citation

If you found this code useful, please cite it with the URL.

```
@misc{soskkobayashi2018bookcorpus,
    author = {Sosuke Kobayashi},
    title = {Homemade BookCorpus},
    howpublished = {\url{https://github.com/BIGBALLON/cifar-10-cnn}},
    year = {2018}
}
```


Also, the original papers which made the original BookCorpus are as follows:

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
