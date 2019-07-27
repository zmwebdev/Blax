#!/usr/bin/env python3
import configparser
import os
import sys
CURDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(CURDIR, os.pardir, 'bert'))
import re
from tokenization import BasicTokenizer
import argparse
import glob
import nltk
from nltk.tokenize import sent_tokenize
nltk.download("punkt", download_dir=".")

parser = argparse.ArgumentParser(description='sentence split')
parser.add_argument('--text_dir', required=True, type=str, help='Path to the directory containing the text files')
parser.add_argument('--do_lower_case', action='store_true', help='Boolean for lower case')

args = parser.parse_args()

TEXTDIR = args.text_dir


def _get_text_file(text_dir=TEXTDIR):
    file_list = glob.glob(f'{text_dir}/**/*.txt')
    files = ",".join(file_list)
    return files


def s_split():
    files = _get_text_file()
    basic_tokenizer = BasicTokenizer(do_lower_case=args.do_lower_case)
    for file in files.split(","):
        with open(file+".sent_splited", 'wt', encoding='utf-8', errors='ignore') as o:
            with open(file, 'rt', encoding='utf-8', errors='ignore') as f:
                for p in f:
                    #Do lower case if required
                    if len(p.strip())==0:
                        continue
                    doc_sentences = sent_tokenize(p)
                    #Output segmented sentences
                    for sent in doc_sentences:
                        o.write(' '.join(basic_tokenizer.tokenize(sent)) + "\n")
                    o.write('\n')

def main():
    s_split()

if __name__ == "__main__":
    main()
