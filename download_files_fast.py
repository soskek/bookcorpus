#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import time


import epub2txt
import os
from progressbar import ProgressBar
from glob import glob
import sys
import json


parser = argparse.ArgumentParser()
parser.add_argument('--out-dir', '--out', type=str, required=True)
parser.add_argument('--list-path', '--list', type=str, required=True)
parser.add_argument('--trash-bad-count', action='store_true', default=False)
args = parser.parse_args()

import signal

global is_sigint_up
is_sigint_up = False

def handler(signal_num,frame):
    print("\nYou Pressed Ctrl+C.")
    is_sigint_up = True

signal.signal(signal.SIGINT, handler)


def write_txt(txt, out_path, num_words=None):
    # occasionally, some epubs text are decoded with errors
    # e.g. repeated bib lines
    # filter out them by comparing number of words
    counted_num_words = len(txt.split())
    if not txt.strip():
        pass
    elif num_words is None or \
            (num_words * 0.5 < counted_num_words < num_words * 1.5):
        with open(out_path, "w") as txt_out:  # convert epub2txt and save
            txt_out.write(txt)
    print("write_txt:" + out_path)

import threading

class DownloadThread (threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self._queue = queue
        try:
            from cookielib import CookieJar
            cj = CookieJar()
            import urllib2
            self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            import urllib
            self.urlretrieve = urllib.urlretrieve
        except ImportError:
            import http.cookiejar
            cj = http.cookiejar.CookieJar()
            import urllib
            self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
            self.urlretrieve = urllib.request.urlretrieve

    def run(self):
        out_dir = args.out_dir
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        done_files = set([os.path.split(path)[-1] for path in glob(os.path.join(out_dir, '*.txt'))])
        while not self._queue.empty():
            if is_sigint_up is True:
                return

            line = self._queue.get()
            if not line.strip():
                continue
            out_path = ''
            try:
                data = json.loads(line.strip())
                _, book_id = os.path.split(data['page'])
                _, file_name = os.path.split(data['epub'])

                out_file_name = '{}__{}'.format(book_id, file_name.replace('.epub', '.txt'))
                out_path = os.path.join(out_dir, out_file_name)
                if out_file_name in done_files:
                    continue
                if data['txt']:
                    # try to download .txt file
                    response = self.opener.open(data['txt'])
                    txt = response.read().decode('utf-8', 'ignore')
                    write_txt(txt, out_path, None)
                else:
                    # revenge by converting .epub to .txt
                    tmp_path = os.path.join(out_dir, file_name)
                    self.urlretrieve(data['epub'], tmp_path)  # download epub
                    txt = epub2txt.epub2txt(tmp_path).convert()
                    if args.trash_bad_count:
                        if 'num_words' in data:
                            write_txt(txt, out_path, data['num_words'])
                    else:
                        write_txt(txt, out_path, None)
            except Exception as e:
                sys.stderr.write(str(e) + '\n')
                if os.path.exists(out_path):
                    os.remove(out_path)
            # remove .epub
            try:
                os.remove(tmp_path)
            except:
                pass


def main():
    dataset = []
    filelist_path = args.list_path

    out_dir = args.out_dir
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    lines = list(open(filelist_path).readlines())

    done_files = set([os.path.split(path)[-1]
                      for path in glob(os.path.join(out_dir, '*.txt'))])
    sys.stderr.write('{} files already had been saved in {}.\n'.format(
        len(done_files), out_dir))

    import queue
    queue = queue.Queue()
    for i, line in enumerate(ProgressBar()(lines)):
        queue.put(line)
    download_threads = []
    for _ in range(10):
        download_threads.append(DownloadThread(queue))
    print("start download....")
    for i in range(10):
        download_threads[i].start()

if __name__ == '__main__':
    main()
