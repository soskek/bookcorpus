#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import urllib
try:
    from urllib import unquote
except:
    from urllib.parse import unquote
import zipfile

import xml.parsers.expat
import html2text
from glob import glob


class ContainerParser():
    def __init__(self, xmlcontent=None):
        self.rootfile = ""
        self.xml = xmlcontent

    def startElement(self, name, attributes):
        if name == "rootfile":
            self.buffer = ""
            self.rootfile = attributes["full-path"]

    def parseContainer(self):
        parser = xml.parsers.expat.ParserCreate()
        parser.StartElementHandler = self.startElement
        parser.Parse(self.xml, 1)
        return self.rootfile


class BookParser():
    def __init__(self, xmlcontent=None):
        self.xml = xmlcontent
        self.title = ""
        self.author = ""
        self.inTitle = 0
        self.inAuthor = 0
        self.ncx = ""

    def startElement(self, name, attributes):
        if name == "dc:title":
            self.buffer = ""
            self.inTitle = 1
        elif name == "dc:creator":
            self.buffer = ""
            self.inAuthor = 1
        elif name == "item":
            if attributes["id"] == "ncx" or attributes["id"] == "toc" or attributes["id"] == "ncxtoc":
                self.ncx = attributes["href"]

    def characters(self, data):
        if self.inTitle:
            self.buffer += data
        elif self.inAuthor:
            self.buffer += data

    def endElement(self, name):
        if name == "dc:title":
            self.inTitle = 0
            self.title = self.buffer
            self.buffer = ""
        elif name == "dc:creator":
            self.inAuthor = 0
            self.author = self.buffer
            self.buffer = ""

    def parseBook(self):
        parser = xml.parsers.expat.ParserCreate()
        parser.StartElementHandler = self.startElement
        parser.EndElementHandler = self.endElement
        parser.CharacterDataHandler = self.characters
        parser.Parse(self.xml, 1)
        return self.title, self.author, self.ncx


class NavPoint():
    def __init__(self, id=None, playorder=None, level=0, content=None, text=None):
        self.id = id
        self.content = content
        self.playorder = playorder
        self.level = level
        self.text = text


class TocParser():
    def __init__(self, xmlcontent=None):
        self.xml = xmlcontent
        self.currentNP = None
        self.stack = []
        self.inText = 0
        self.toc = []

    def startElement(self, name, attributes):
        if name == "navPoint":
            level = len(self.stack)
            self.currentNP = NavPoint(
                attributes["id"], attributes["playOrder"], level)
            self.stack.append(self.currentNP)
            self.toc.append(self.currentNP)
        elif name == "content":
            self.currentNP.content = unquote(attributes["src"])
        elif name == "text":
            self.buffer = ""
            self.inText = 1

    def characters(self, data):
        if self.inText:
            self.buffer += data

    def endElement(self, name):
        if name == "navPoint":
            self.currentNP = self.stack.pop()
        elif name == "text":
            if self.inText and self.currentNP:
                self.currentNP.text = self.buffer
            self.inText = 0

    def parseToc(self):
        parser = xml.parsers.expat.ParserCreate()
        parser.StartElementHandler = self.startElement
        parser.EndElementHandler = self.endElement
        parser.CharacterDataHandler = self.characters
        parser.Parse(self.xml, 1)
        return self.toc


class epub2txt():
    def __init__(self, epubfile=None):
        self.epub = epubfile

    def convert(self):
        # print "Processing %s ..." % self.epub
        file = zipfile.ZipFile(self.epub, "r")
        rootfile = ContainerParser(
            file.read("META-INF/container.xml")).parseContainer()
        title, author, ncx = BookParser(file.read(rootfile)).parseBook()
        ops = "/".join(rootfile.split("/")[:-1])
        if ops != "":
            ops = ops+"/"
        toc = TocParser(file.read(ops + ncx)).parseToc()

        # fo = open("%s_%s.txt" % (title, author), "w")
        content = []
        for t in toc:
            html = file.read(ops + t.content.split("#")[0])
            text = html2text.html2text(html.decode("utf-8"))
            # fo.write("*"*(t.level+1) + " " + t.text.encode("utf-8")+"\n")
            # fo.write(t.text.encode("utf-8")+"{{{%d\n" % (t.level+1))
            # fo.write(text.encode("utf-8")+"\n")
            content.append("*" * (t.level+1) + " " +
                           t.text + "\n")
            content.append(t.text + "{{{%d\n" % (t.level+1))
            content.append(text + "\n")
        # fo.close()
        file.close()
        return ''.join(content)


if __name__ == "__main__":
    if sys.argv[1]:
        filenames = glob(sys.argv[1])
        for filename in filenames:
            txt = epub2txt(filename).convert()
            print(txt)
